# Módulo para gravação de áudio do microfone
# Início: 11/05/2025 | Última atualização: 11/05/2025

import os
import wave
import time
import tempfile
import threading
from datetime import datetime

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    print("[!] erro: PyAudio. tentando instalar...")
    try:
        import pip
        pip.main(['install', 'pyaudio'])
        import pyaudio
        PYAUDIO_AVAILABLE = True
    except:
        print("[!] falha ao instalar pyaudio.")
        PYAUDIO_AVAILABLE = False

def record_audio(duration=10):

    duration = min(60, max(1, duration))
    
    p = None
    stream = None
    
    try:
        p = pyaudio.PyAudio()
        
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_filename = os.path.join(tempfile.gettempdir(), f"audio_{timestamp}.wav")
        
        input_device_index = None
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info.get('maxInputChannels') > 0:
                input_device_index = i
                print(f"[+] usando dispositivo de áudio: {device_info.get('name')}")
                break
                
        if input_device_index is None:
            if p:
                p.terminate()
            return None, "[!] nenhum dispositivo de entrada de áudio encontrado"
        
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=input_device_index,
            frames_per_buffer=CHUNK
        )
        
        print(f"[+] iniciando gravação por {duration} segundos...")
        
        frames = []
        for i in range(0, int(RATE / CHUNK * duration)):
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
            except Exception as e:
                print(f"[!] erro durante leitura do stream: {str(e)}")
                if p:
                    p.terminate()
                return None, f"[!] erro durante a gravação: {str(e)}"
        
        print("[*] gravação finalizada")
        
        if stream:
            stream.stop_stream()
            stream.close()
        
        if p:
            p.terminate()
        
        try:
            wf = wave.open(temp_filename, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            print(f"[*] áudio salvo em: {temp_filename}")
            return temp_filename, None
            
        except Exception as e:
            return None, f"[!] erro ao salvar arquivo de áudio: {str(e)}"
        
    except Exception as e:
        if stream:
            try:
                stream.stop_stream()
                stream.close()
            except:
                pass
                
        if p:
            try:
                p.terminate()
            except:
                pass
                
        return None, f"[!] erro ao gravar áudio: {str(e)}"