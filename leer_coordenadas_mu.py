import dxcam
import pygetwindow
from screeninfo import get_monitors
from PIL import Image
from datetime import datetime
from skimage.metrics import structural_similarity as ssim
import os
import time
import pytesseract
import numpy as np


def obtener_monitor_para_ventana(ventana_mu):
    for nro_monitor, monitor_info  in enumerate(get_monitors()):
        
        if (
            ventana_mu.left >= monitor_info.x and 
            ventana_mu.top >= monitor_info.y and
            ventana_mu.left + ventana_mu.width  <=  monitor_info.x +  monitor_info.width  and 
            ventana_mu.top + ventana_mu.height <= monitor_info.y + monitor_info.height
        ):
            print(f"[[[[Monitor {nro_monitor}]]]]")
            print(f"x: {ventana_mu.left - monitor_info.x}, y: {ventana_mu.top - monitor_info.y}")
            return nro_monitor, ventana_mu.left - monitor_info.x, ventana_mu.top - monitor_info.y, ventana_mu.width, ventana_mu.height


NOMBRE_VENTANA = "MU"
FOLDER_CAPTURES = r"D:\workspace-phyton\captures"

############# MAIN #############
ventanas = [v for v in pygetwindow.getWindowsWithTitle(NOMBRE_VENTANA) 
            if v.title.strip() == NOMBRE_VENTANA]

print(f"Ventanas de '{NOMBRE_VENTANA}':") # Ventanas encontradas
for i, v in enumerate(ventanas):
    print(f"[{i}] '{v.title}' - Posición: ({v.left}, {v.top}) Tamaño: {v.width}x{v.height}")

index_ventana = int(input("\n🧭 Ventana N°: "))
ventana_mu = ventanas[index_ventana]

nro_monitor, x, y, width, height = obtener_monitor_para_ventana(ventana_mu)

camera = dxcam.create(output_idx=nro_monitor) # Monitor N°
coordenadas = (x+160, y+30, x+210, y+63)
#region = (x, y, x + width, y + height)
contador = 1

while True:
    frame = camera.grab(region=coordenadas)
    if frame is not None:
        img = Image.fromarray(frame)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"captura_{contador}_{timestamp}.png"
        
        path = os.path.join(FOLDER_CAPTURES, filename)
        img.save(path)
        print(f"📸 Captura: {contador}")
        contador += 1

        custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789,'
        texto = pytesseract.image_to_string(Image.open(path), config=custom_config)
        texto_limpio = texto.strip().replace("\n", "")
        print(f"✅ Texto leido {texto_limpio}.")
        coordenada_x, coordenada_y = map(int, texto.split(","))

        # 80 > coordenada_x > 40 and 211 > coordenada_y > 171
        # 40,190  60,211
        # 60,171  80,193
        if 40 < coordenada_x < 80 and 171 < coordenada_y < 211:
            print(f"❌ Estas en safe ❌")
    else:
        print("⚠️ Error al capturar imagen.")
    time.sleep(3)