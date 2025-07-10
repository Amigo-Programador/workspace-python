import pygetwindow as gw

print("🔍 Ventanas abiertas actualmente:\n")
for ventana in gw.getWindowsWithTitle(""):
    if ventana.title.strip():  # Solo muestra ventanas con título
        print(f"- {ventana.title}")