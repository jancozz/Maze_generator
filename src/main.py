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
    window_width = 685
    window_height = 820

    # Obtener dimensiones de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcular posición centrada
    x_position = int((screen_width - window_width) / 2)
    y_position = int((screen_height - window_height) * 0.25)

    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Crear controlador (esto inicializa toda la aplicación)
    controller = MazeController(root)

    # Iniciar loop de eventos
    root.mainloop()


if __name__ == "__main__":
    main()
