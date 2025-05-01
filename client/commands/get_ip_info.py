# Função para pegar IP e País 
# Início: 01/05/2025 | Última atualização: 01/05/2025

import platform
import subprocess
import urllib.request
import json
import ctypes
import os

def get_ip_info():
    try:
        with urllib.request.urlopen("https://geolocation-db.com/json") as url:
            data = json.loads(url.read().decode())
            return data.get('IPv4'), data.get('country_code')
    except:
        return "Unknown", "xx"