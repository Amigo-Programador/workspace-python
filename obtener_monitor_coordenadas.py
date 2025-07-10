import dxcam
import pygetwindow
from screeninfo import get_monitors
from PIL import Image
from datetime import datetime
from skimage.metrics import structural_similarity as ssim
import os
import time
import numpy as np

NOMBRE_VENTANA = "MU"  # Cambia por el nombre exacto de la ventana
FOLDER_CAPTURES = r"D:\workspace-phyton\captures"


def comparar_imagenes(img1_path, img2_path, umbral_similitud=0.8):
    # Abrir imágenes y convertir a escala de grises
    img1 = Image.open(img1_path).convert("L")
    img2 = Image.open(img2_path).convert("L")

    # Redimensionar imagen2 al tamaño de imagen1
    img2 = img2.resize(img1.size)

    
    # Convertir a arrays de NumPy
    img1_np = np.array(img1)
    img2_np = np.array(img2)

    # Calcular SSIM
    score, _ = ssim(img1_np, img2_np, full=True)
    print(f"🧪 Similitud: {score * 100:.2f}%")

    # Verificar si la similitud supera el umbral
    if score >= umbral_similitud:
        print("✅ Las imágenes son similares (80% o más)")
        return True
    else:
        print("❌ Las imágenes NO son lo suficientemente similares")
        return False

def obtener_monitor_para_ventana(ventana_mu):
    # -1920, 21
    for nro_monitor, monitor_info  in enumerate(get_monitors()): 
        print(f"[Monitor {nro_monitor}]")
        print(f"   width={monitor_info.width}, height={monitor_info.height}")
        print(f"   x={monitor_info.x}, y={monitor_info.y}")
        
           
        print(f"[MU]")
        print(f"   width={ventana_mu.width} height={ventana_mu.height}")
        print(f"   left={ventana_mu.left}, top={ventana_mu.top}\n")

        if (
            ventana_mu.left >= monitor_info.x and 
            ventana_mu.top >= monitor_info.y and
            ventana_mu.left + ventana_mu.width  <=  monitor_info.x +  monitor_info.width  and 
            ventana_mu.top + ventana_mu.height <= monitor_info.y + monitor_info.height
        ):
            return nro_monitor, ventana_mu.left - monitor_info.x, ventana_mu.top - monitor_info.y, ventana_mu.width, ventana_mu.height
            
            
            

# Buscar ventanas con nombre exacto
ventanas = [v for v in pygetwindow.getWindowsWithTitle(NOMBRE_VENTANA) 
            if v.title.strip() == NOMBRE_VENTANA]

############# MAIN #############
print(f"Ventanas de '{NOMBRE_VENTANA}':") # Ventanas encontradas
for i, v in enumerate(ventanas):
    print(f"[{i}] '{v.title}' - Posición: ({v.left}, {v.top}) Tamaño: {v.width}x{v.height}")

try:
    index_ventana = int(input("\n🧭 Ventana N°: "))
    ventana_mu = ventanas[index_ventana]
except (ValueError, IndexError):
    print("❌ Selección inválida.")
    exit()

# Obtener el monitor y mostrar información
nro_monitor, x, y, width, height = obtener_monitor_para_ventana(ventana_mu)


camera = dxcam.create(output_idx=nro_monitor)
region = (x, y, x + width, y + height)
contador = 1
while True:
    frame = camera.grab(region=region)
    if frame is not None:
        img = Image.fromarray(frame)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"captura_{contador}_{timestamp}.png"
        path = os.path.join(FOLDER_CAPTURES, filename)
        img.save(path)
        print(f"📸 Captura {contador} guardada: {path}")
        contador += 1

        iguales = comparar_imagenes(path, r"D:\workspace-phyton\captures\acheron.png")
        if iguales:
            print("🚀 Se detectó coincidencia")
    else:
        print("⚠️ Error al capturar imagen.")
    time.sleep(5)
