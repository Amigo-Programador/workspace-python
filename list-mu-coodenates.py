import pygetwindow as gw

# Filtrar solo ventanas con título "MU"
ventanas_mu = [v for v in gw.getWindowsWithTitle("MU") if v.title.strip()]

if ventanas_mu:
    print(f"\n🔍 Se encontraron {len(ventanas_mu)} ventanas con el título 'MU':\n")
    for i, ventana in enumerate(ventanas_mu):
        print(f"[{i}] '{ventana.title}' - Posición: ({ventana.left}, {ventana.top}) Tamaño: {ventana.width}x{ventana.height}")
else:
    print("❌ No se encontraron ventanas con el título 'MU'")
