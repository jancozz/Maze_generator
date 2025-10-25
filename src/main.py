import customtkinter as ctk
import sys
import os

#Agregar la carpeta src al path para que funcione en ejecutable
if getattr(sys, 'frozen', False):
    # Si es ejecutable
    application_path = sys._MEIPASS
else:
    # Si es desarrollo
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

from controller.maze_controller import MazeController

def main():
    """Función principal que inicia la aplicación."""
    # Configurar tema de customtkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Crear ventana principal
    root = ctk.CTk()
    root.title("Generador y Solucionador de Laberintos")
    root.geometry(
        f"{730}x{880}+{int(root.winfo_screenwidth() / 2 - 365)}+{int(root.winfo_screenheight() / 2 - 480)}")
    root.resizable(False, False)

    # Crear controlador (esto inicializa toda la aplicación)
    controller = MazeController(root)

    # Iniciar loop de eventos
    root.mainloop()


if __name__ == "__main__":
    main()