# Função para capturar screenshots
# Início: 01/05/2025 | Última atualização: 01/05/2025

import os
import time
import base64
from io import BytesIO
from datetime import datetime

try:
    from PIL import ImageGrab
except ImportError:
    os.system("pip install pillow --quiet")
    from PIL import ImageGrab

def take_screenshot():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        
        temp_dir = os.path.join(os.environ.get('TEMP', os.path.join(os.environ.get('TMP', '/tmp'))), "sshots")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        filepath = os.path.join(temp_dir, filename)
        
        screenshot = ImageGrab.grab()
        screenshot.save(filepath, "PNG")
        
        return filepath, None
    except Exception as e:
        return None, str(e)

def take_screenshot_base64():
    try:
        screenshot = ImageGrab.grab()
        
        buffer = BytesIO()
        screenshot.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return img_str, None
    except Exception as e:
        return None, str(e)
