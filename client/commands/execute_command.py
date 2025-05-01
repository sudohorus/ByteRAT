# Função que envia comandos diretamente para o CMD
# Início: 01/05/2025 | Última atualização: 01/05/2025

import platform
import subprocess
import urllib.request
import json
import ctypes
import os

def execute_command(command):
    try:
        if platform.system() == "Windows":
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        stdout, stderr = process.communicate()
        if stdout:
            return stdout.decode('utf-8', errors='replace')
        elif stderr:
            return stderr.decode('utf-8', errors='replace')
        return "[+] non output."
    except Exception as e:
        return f"Erro ao executar comando: {str(e)}"
