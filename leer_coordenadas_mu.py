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
import requests
import urllib.parse

NOMBRE_VENTANA = "MU"
FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
FOLDER_CAPTURES = os.path.join(FOLDER_PATH, "captures")
NUMERO_WSP = '51976073414'  # sin '+' pero con código país, por ejemplo Argentina: 54911...
API_KEY = '4541590'  # El token que te da CallMeBot

def get_cordinates_mu_window(ventana_mu):
    for nro_monitor, monitor_info  in enumerate(get_monitors()):
        
        if (
            ventana_mu.left >= monitor_info.x and  ventana_mu.top >= monitor_info.y and
            ventana_mu.left + ventana_mu.width  <=  monitor_info.x +  monitor_info.width  and 
            ventana_mu.top + ventana_mu.height <= monitor_info.y + monitor_info.height
        ):
            print(f"[[[[Monitor {nro_monitor}]]]]")
            print(f"x: {ventana_mu.left - monitor_info.x}, y: {ventana_mu.top - monitor_info.y}")
            return nro_monitor, ventana_mu.left - monitor_info.x, ventana_mu.top - monitor_info.y, ventana_mu.width, ventana_mu.height


def send_whatsapp_message(numero, token, mensaje):
    mensaje_encoded = urllib.parse.quote(mensaje)
    url = f"https://api.callmebot.com/whatsapp.php?phone={numero}&text={mensaje_encoded}&apikey={token}"
    try:
        response = requests.get(url)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if response.status_code == 200:
            print(f"\n📩 Mensaje enviado por WhatsApp. {timestamp}")
        else:
            print(f"❌ Error al enviar WhatsApp: {response.status_code} - {response.text} ({timestamp})")
    except Exception as e:
        print(f"⚠️ Error de red al enviar WhatsApp: {e}")

############# MAIN #############
ventanas = [v for v in pygetwindow.getWindowsWithTitle(NOMBRE_VENTANA) 
            if v.title.strip() == NOMBRE_VENTANA]

print(f"Ventanas de '{NOMBRE_VENTANA}':") # Ventanas encontradas
for i, v in enumerate(ventanas):
    print(f"[{i}] '{v.title}' - Posición: ({v.left}, {v.top}) Tamaño: {v.width}x{v.height}")

index_ventana = int(input("\n🧭 Ventana N°: "))
ventana_mu = ventanas[index_ventana]

nro_monitor, x, y, width, height = get_cordinates_mu_window(ventana_mu)
camera = dxcam.create(output_idx=nro_monitor) # Apunta al monitor de la ventana del MU
coordenadas = (x+160, y+30, x+210, y+63) # Coordenadas de la captura de pantalla
contador = 1
first = True
spot_x = 0
spot_y = 0
while True:
    frame = camera.grab(region=coordenadas) # Hace la captura de pantalla
    if frame is not None:
        img = Image.fromarray(frame)
        custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789,'
        timestamp = datetime.now().strftime("%Y-%m-%d_%H#%M#%S")

        try:
            image_text = pytesseract.image_to_string(img, config=custom_config)
            format_text = image_text.strip().replace("\n", "")
            array_text = [p for p in format_text.split(",") if p.strip().isdigit()]
            if len(array_text) >= 2:
                coordinate_x, coordinate_y = map(int, array_text[0:2])
                print(f"✅ Coordenas MU ({coordinate_x},{coordinate_y}) - Time: {timestamp}")
            else:
                raise ValueError("No se encontraron dos números válidos.")
        except ValueError as e:
            mensaje_error_lectura = "Error leyendo coordenadas (Desconexion probablemente‼️)"
            send_whatsapp_message(NUMERO_WSP, API_KEY, mensaje_error_lectura)
            print(f"⚠️ Error leyendo coordenadas: {e}")            
            time.sleep(600)
            continue

        if first:
            spot_x = coordinate_x
            spot_y = coordinate_y
            first = False

        if coordinate_x < spot_x-10 or spot_x+10 < coordinate_x or coordinate_y < spot_y-10 or spot_y+10 < coordinate_y:
            
            filename = f"mu{contador}_{timestamp}.png"        
            path = os.path.join(FOLDER_CAPTURES, filename)

            coordinate_window_mu = (x, y, x+width, y+height)
            frame_window = camera.grab(region=coordinate_window_mu) # Hace la captura de pantalla
            img_window = Image.fromarray(frame_window)
            img_window.save(path)

            mensaje = f"Te mataron en el spot 🕊️ ({coordinate_x},{coordinate_y})"
            send_whatsapp_message(NUMERO_WSP, API_KEY, mensaje)
            print(f"❌ Estas en safe ❌")
            time.sleep(600)
        contador += 1    
    else:
        mensaje_error_captura = "Error captura de pantalla MU (Pobablemente desconexión 🚩)"
        send_whatsapp_message(NUMERO_WSP, API_KEY, mensaje_error_captura)
        print("⚠️ Error al capturar imagen.")
        time.sleep(600)
    time.sleep(60)