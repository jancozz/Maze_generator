import customtkinter as ctk

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
        f"{685}x{835}+{int(root.winfo_screenwidth() / 2 - 365)}+{int(root.winfo_screenheight() / 2 - 510)}")

    # Crear controlador (esto inicializa toda la aplicación)
    controller = MazeController(root)

    # Iniciar loop de eventos
    root.mainloop()


if __name__ == "__main__":
    main()
