import sys
import os
import traceback
import PySimpleGUI as sg

# Agregar el directorio actual al path de Python
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Imprimir información de depuración
print("Python Path:", sys.path)
print("Directorio actual:", os.getcwd())
print("Contenido del directorio src:")
try:
    print(os.listdir("src"))
except Exception as e:
    print(f"Error al listar src: {e}")

try:
    from src.gui.main_window import MainWindow
except ImportError as e:
    print(f"Error detallado de importación: {traceback.format_exc()}")
    sg.popup_error(f"Error importando módulos: {str(e)}\n\nAsegúrate de estar ejecutando desde la carpeta raíz del proyecto.")
    sys.exit(1)

def main():
    try:
        ventana_principal = MainWindow()
        ventana_principal.ejecutar()
    except Exception as e:
        sg.popup_error(f"Error crítico: {str(e)}\n\n{traceback.format_exc()}")

if __name__ == "__main__":
    main()