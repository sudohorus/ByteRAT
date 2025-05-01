# Função para capturar imagem de câmeras
# Início: 01/05/2025 | Última atualização: 01/05/2025

import cv2
import os
import tempfile
from datetime import datetime

def take_webcam_photo():
    try:
        cap = cv2.VideoCapture(0) 

        if not cap.isOpened():
            return None, "[!] não foi possível acessar a webcam"
            
        for _ in range(5):
            ret, _ = cap.read()
            if not ret:
                continue
                
        ret, frame = cap.read()
        
        cap.release()
        
        if not ret or frame is None:
            return None, "[!] falha ao capturar imagem da webcam"
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"webcam_{timestamp}.jpg"
        
        temp_dir = tempfile.gettempdir()
        filepath = os.path.join(temp_dir, filename)
        
        cv2.imwrite(filepath, frame)

        if not os.path.exists(filepath):
            return None, "[!] falha ao salvar a imagem capturada"
            
        return filepath, None
        
    except Exception as e:
        return None, str(e)