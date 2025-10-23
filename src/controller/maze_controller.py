from src.model.maze import Maze
from src.model.algorithms import *
from src.view.maze_view import MazeView
from tkinter import messagebox

class MazeController:
    """
    Controlador principal que conecta la vista con la lógica del laberinto.
    Gestiona la generación y resolución del laberinto.
    """
    def __init__(self, root):
        """
        Inicializa el controlador y crea la vista.
        """
        self.maze = None
        self.view = MazeView(root, self)

    def generate_maze(self, width, height, algorithm):
        """
        Genera un nuevo laberinto con el algoritmo especificado.
        """
        self.maze = Maze(width, height)
        if algorithm == "DFS":
            generate_maze_dfs(self.maze)
        elif algorithm == "Kruskal":
            generate_maze_kruskal(self.maze)
        self.view.draw_maze(self.maze)

    def solve_maze(self, algorithm):
        """
        Resuelve el laberinto usando BFS o A* y muestra el camino animado.
        """
        if not self.maze:
            messagebox.showerror("Error", "Primero debes generar un laberinto antes de resolverlo.")
            return

        start = self.maze.entry
        end = self.maze.exit

        # Selección de algoritmo
        if algorithm == "ASTAR":
            path, visited = solve_maze_astar(self.maze, start, end)
            color = "#057032"
        else:
            path, visited = solve_maze_bfs(self.maze, start, end)
            color = "#6909C8"

        if path:
            self.view.draw_path_animated(path, delay=20, visited=visited, color=color)
        else:
            messagebox.showerror("Error", "No se encontró un camino entre la entrada y la salida.")