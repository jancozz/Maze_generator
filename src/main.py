from customtkinter import *
from controller.maze_controller import MazeController

def main():
    """
    Crea la ventana, la centra en pantalla y lanza el controlador.
    """
    root = CTk()
    root.title("Generador y Solucionador de Laberintos")
    root.geometry(
        f"{750}x{810}+{int(root.winfo_screenwidth() / 2 - 375)}+{int(root.winfo_screenheight() / 2 - 405)}")
    app = MazeController(root)
    root.mainloop()

if __name__ == "__main__":
    main()