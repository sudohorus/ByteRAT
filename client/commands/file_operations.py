# Módulo para operações de arquivos (download/upload)
# Início: 04/05/2025 | Última atualização: 04/05/2025

import os
import asyncio
import discord
from discord.ext import commands
import aiohttp
import shutil
from datetime import datetime

MAX_DISCORD_FILE_SIZE = 8 * 1024 * 1024

async def download_file(url, destination):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return None, f"[!] erro ao baixar arquivo: Status {response.status}"
                
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                
                with open(destination, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                
                return destination, None
    except Exception as e:
        return None, f"[!] erro ao baixar arquivo: {str(e)}"

def list_directory(path="."):
    try:
        if not os.path.exists(path):
            return f"[!] diretório não encontrado: {path}"
        
        if not os.path.isdir(path):
            return f"[!] o caminho especificado não é um diretório: {path}"
        
        items = os.listdir(path)
        if not items:
            return f"[!] diretório vazio: {path}"
        
        total_size = 0
        result = f"Listando conteúdo de: {os.path.abspath(path)}\n\n"
        result += f"{'Tipo':<6} {'Tamanho':<10} {'Modificado em':<20} Nome\n"
        result += f"{'-'*6} {'-'*10} {'-'*20} {'-'*30}\n"
        
        directories = []
        files = []
        
        for item in items:
            item_path = os.path.join(path, item)
            try:
                stats = os.stat(item_path)
                modified_time = datetime.fromtimestamp(stats.st_mtime).strftime('%d/%m/%Y %H:%M:%S')
                
                if os.path.isdir(item_path):
                    directories.append((item, 0, modified_time, "[DIR]"))
                else:
                    size = stats.st_size
                    total_size += size
                    size_str = _format_size(size)
                    files.append((item, size, modified_time, size_str))
            except Exception as e:
                files.append((item, 0, "???", "[ERRO]"))
        
        for name, _, modified_time, type_str in sorted(directories):
            result += f"{type_str:<6} {'<DIR>':<10} {modified_time:<20} {name}\n"
        
        for name, size, modified_time, size_str in sorted(files):
            result += f"{'[FILE]':<6} {size_str:<10} {modified_time:<20} {name}\n"
        
        result += f"\n{len(files)} arquivo(s), {_format_size(total_size)}"
        result += f"\n{len(directories)} pasta(s)"
        
        return result
    except Exception as e:
        return f"[!] erro ao listar diretório: {str(e)}"

def _format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes/(1024*1024):.1f} MB"
    else:
        return f"{size_bytes/(1024*1024*1024):.1f} GB"

def upload_file(filepath):
    try:
        if not os.path.exists(filepath):
            return None, f"[!] arquivo não encontrado: {filepath}"
        
        filesize = os.path.getsize(filepath)
        
        if filesize > MAX_DISCORD_FILE_SIZE:
            temp_dir = os.path.join(os.environ.get('TEMP', '/tmp'), "file_chunks")
            os.makedirs(temp_dir, exist_ok=True)
            
            chunk_size = 7.5 * 1024 * 1024
            chunk_files = []
            
            filename = os.path.basename(filepath)
            with open(filepath, 'rb') as f:
                chunk_index = 1
                while True:
                    chunk_data = f.read(int(chunk_size))
                    if not chunk_data:
                        break
                    
                    chunk_filename = os.path.join(temp_dir, f"{filename}.part{chunk_index}")
                    with open(chunk_filename, 'wb') as chunk_file:
                        chunk_file.write(chunk_data)
                    
                    chunk_files.append(chunk_filename)
                    chunk_index += 1
                    
            return chunk_files, f"[+] arquivo dividido em {len(chunk_files)} partes devido ao tamanho ({_format_size(filesize)})"
        else:
            return [filepath], None
    
    except Exception as e:
        return None, f"[!] erro ao preparar arquivo para upload: {str(e)}"

async def download_file_from_attachment(attachment, destination=None):
    try:
        if not destination:
            destination = attachment.filename
        
        os.makedirs(os.path.dirname(os.path.abspath(destination)), exist_ok=True)

        await attachment.save(destination)
        
        return destination, None
    except Exception as e:
        return None, f"[!] erro ao baixar anexo: {str(e)}"