# Tratamento de erros. Configura e gerencia os tratadores de erro para o bot
# Início: 01/05/2025 | Última atualização: 01/05/2025

from discord.ext import commands
import traceback
import time

def setup_error_handlers(client):
    
    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        
        if isinstance(error, commands.CheckFailure):
            await ctx.send("```[!] Você não tem permissão para usar este comando```")
            return
        
        print(f"[!] Erro ao executar comando: {str(error)}")
        traceback.print_exc()
        await ctx.send(f"```[!] Erro: {str(error)}```")
    
    @client.event
    async def on_error(event, *args, **kwargs):
        print(f"[!] Erro no evento {event}: {traceback.format_exc()}")
    
    @client.event
    async def on_connect():
        client.session_info["start_time"] = time.time()
        print("[+] Cliente conectado ao Discord")