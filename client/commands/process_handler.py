# Módulo para gerenciamento de processos (listar e finalizar)
# Início: 11/05/2025 | Última atualização: 11/05/2025

import os
import platform
import psutil
import time
from datetime import datetime

def list_processes():
    try:
        system_info = platform.system()
        if system_info == "Windows":
            system_name = f"Windows {platform.release()}"
        else:
            system_name = system_info
            
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        memory_used = memory.used / (1024 * 1024 * 1024)
        memory_total = memory.total / (1024 * 1024 * 1024)
        memory_percent = memory.percent
        
        result = f"Sistema: {system_name} | CPU: {cpu_percent}% | Memória: {memory_used:.2f}GB/{memory_total:.2f}GB ({memory_percent}%)\n\n"
        result += f"{'PID':<7} {'CPU%':<6} {'Mem%':<6} {'Nome':<25} {'Status':<10} {'Usuário':<15} {'Iniciado em'}\n"
        result += f"{'-'*7} {'-'*6} {'-'*6} {'-'*25} {'-'*10} {'-'*15} {'-'*19}\n"
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'cpu_percent', 'memory_percent', 'create_time']):
            try:
                process_info = proc.info
                
                pid = process_info.get('pid', 0)
                if pid is None:
                    pid = 0

                try:
                    name = proc.name()
                    if name is None:
                        name = "N/A"
                    elif len(name) > 25:
                        name = name[:22] + "..."
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    name = process_info.get('name')
                    if not name:
                        name = "N/A"
                    elif len(name) > 25:
                        name = name[:22] + "..."
            
                try:
                    username = process_info.get('username')
                    if not username:
                        username = "N/A"
                    elif len(username) > 15:
                        username = username[:12] + "..."
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    username = "N/A"
                
                status = process_info.get('status')
                if not status:
                    status = "N/A"
            
                cpu = process_info.get('cpu_percent')
                if cpu is None:
                    cpu = 0.0
                    
                mem = process_info.get('memory_percent')
                if mem is None:
                    mem = 0.0
                
                try:
                    create_time_value = process_info.get('create_time')
                    if create_time_value:
                        create_time = datetime.fromtimestamp(create_time_value).strftime('%d/%m/%Y %H:%M:%S')
                    else:
                        create_time = "N/A"
                except:
                    create_time = "N/A"
                
                processes.append({
                    'pid': pid,
                    'name': name,
                    'username': username,
                    'status': status,
                    'cpu': cpu,
                    'mem': mem,
                    'create_time': create_time
                })
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        processes.sort(key=lambda x: x['cpu'] if isinstance(x['cpu'], (int, float)) else 0, reverse=True)
        
        max_processes = min(100, len(processes))
        for i in range(max_processes):
            proc = processes[i]
            result += f"{proc['pid']:<7} {proc['cpu']:<6.1f} {proc['mem']:<6.1f} {proc['name']:<25} {proc['status']:<10} {proc['username']:<15} {proc['create_time']}\n"
        
        result += f"\nTotal de processos: {len(processes)} (exibindo os primeiros {max_processes})"
        
        return result
        
    except Exception as e:
        return f"[!] erro ao listar processos: {str(e)}"

def kill_process(pid_or_name):
    try:
        if pid_or_name.isdigit():
            pid = int(pid_or_name)
            try:
                process = psutil.Process(pid)
                process_name = process.name()
                process.terminate() 
                
                gone, alive = psutil.wait_procs([process], timeout=3)
                if process in alive:
                    process.kill()
                
                return f"[!] processo finalizado com sucesso: PID {pid} ({process_name})"
            except psutil.NoSuchProcess:
                return f"[!] processo não encontrado: PID {pid}"
            except psutil.AccessDenied:
                return f"[!] acesso negado ao tentar finalizar o processo: PID {pid}"
        else:
            count = 0
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if pid_or_name.lower() in proc.info['name'].lower():
                        proc.terminate()
                        gone, alive = psutil.wait_procs([proc], timeout=3)
                        if proc in alive:
                            proc.kill()
                        count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                    
            if count > 0:
                return f"[+] finalizados {count} processo(s) com o nome '{pid_or_name}'"
            else:
                return f"[+] nenhum processo encontrado com o nome '{pid_or_name}'"
    
    except Exception as e:
        return f"[!] erro ao tentar finalizar processo: {str(e)}"