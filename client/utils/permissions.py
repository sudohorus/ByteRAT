# Sistema de permissões. Verifica se os usuários estão autorizados a executar comandos
# Início: 01/05/2025 | Última atualização: 01/05/2025

from discord.ext import commands
from config import AUTHORIZED_IDS

def is_authorized():
    async def predicate(ctx):
        return ctx.author.id in AUTHORIZED_IDS or ctx.author.guild_permissions.administrator
    return commands.check(predicate)

def is_in_session_channel():
    async def predicate(ctx):
        return ctx.channel.id == ctx.bot.session_info.get("channel_id")
    return commands.check(predicate)