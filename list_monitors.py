import dxcam
from screeninfo import get_monitors

# Obtener detalles de todos los monitores

print("🖥️ Monitores detectados:\n")

for i, monitor in enumerate(get_monitors()):
    print(f"[Monitor {i}]")
    print(f" - Resolución: {monitor.width}x{monitor.height}")
    print(f" - Posición: left={monitor.x}, top={monitor.y}\n")