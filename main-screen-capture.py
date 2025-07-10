import dxcam
import pygetwindow

NOMBRE_VENTANA = "MU"  # Cambia por el nombre exacto de la ventana

def obtener_monitor_para_ventana(ventana_coordenadas):
    print(f" > Entro al metodo ")
    for i in range(1):  # Soporte para hasta 5 monitores
        print(f" >> for {i}")
        try:            
            print(f" >>> try {i}")
            monitor = dxcam.output_details(i)
            print(f" >>> output_details {i}")
            mon_left = monitor["left"]
            mon_top = monitor["top"]
            mon_right = mon_left + monitor["width"]
            mon_bottom = mon_top + monitor["height"]

            if (
                ventana_coordenadas.left >= mon_left and
                ventana_coordenadas.top >= mon_top and
                ventana_coordenadas.left + ventana_coordenadas.width <= mon_right and
                ventana_coordenadas.top + ventana_coordenadas.height <= mon_bottom
            ):
                return i, monitor
        except:
            continue
    return None, None

# Buscar ventanas con nombre exacto
ventanas = [v for v in pygetwindow.getWindowsWithTitle(NOMBRE_VENTANA)
            if v.title.strip() == NOMBRE_VENTANA]

############# MAIN #############

print(f"Ventanas de '{NOMBRE_VENTANA}':") # Ventanas encontradas
for i, v in enumerate(ventanas):
    print(f"[{i}] '{v.title}' - Posición: ({v.left}, {v.top}) Tamaño: {v.width}x{v.height}")

# Pedir selección
try:
    index_ventana = int(input("\n🧭 Ventana N°: "))
    ventana = ventanas[index_ventana]
except (ValueError, IndexError):
    print("❌ Selección inválida.")
    exit()

# Obtener el monitor y mostrar información
nro_monitor, monitor_info = obtener_monitor_para_ventana(ventana)

if nro_monitor is None:
    print("❌ No se pudo identificar el monitor que contiene la ventana.")
