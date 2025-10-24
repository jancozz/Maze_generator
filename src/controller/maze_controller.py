from tkinter import messagebox
from src.model.graph import Graph
from src.model.algorithms import (
    generate_maze_dfs, generate_maze_kruskal,
    solve_maze_bfs, solve_maze_astar
)
from src.view.maze_view import MazeView


class MazeController:
    """
    Controlador principal que conecta la vista con la lógica del laberinto.
    Gestiona la generación y resolución del laberinto.
    """

    def __init__(self, root):
        self.graph = None
        self.view = MazeView(root, self)

    def generate_maze(self, width, height, algorithm):
        """Genera un nuevo laberinto (DFS o Kruskal)."""
        self.graph = Graph(width, height)

        algorithm = algorithm.lower()
        if algorithm == "dfs":
            generate_maze_dfs(self.graph)
        elif algorithm == "kruskal":
            generate_maze_kruskal(self.graph)
        else:
            messagebox.showerror("Error", f"Algoritmo '{algorithm}' no soportado.")
            return

        self.view.draw_maze(self.graph)

    def solve_maze(self, algorithm):
        """Resuelve el laberinto con BFS o A*."""
        if not self.graph:
            messagebox.showerror("Error", "Primero debes generar un laberinto.")
            return

        start = self.graph.entry
        end = self.graph.exit
        if not start or not end:
            messagebox.showerror("Error", "El laberinto no tiene puntos de entrada o salida.")
            return

        algorithm = algorithm.lower()
        if algorithm == "astar":
            path, visited = solve_maze_astar(self.graph, start, end)
            color = "#057032"
        elif algorithm == "bfs":
            path, visited = solve_maze_bfs(self.graph, start, end)
            color = "#6909C8"
        else:
            messagebox.showerror("Error", f"Algoritmo de resolución no soportado: {algorithm}")
            return

        if path:
            self.view.draw_path_animated(path, delay=20, visited=visited, color=color)
        else:
            messagebox.showerror("Error", "No se encontró un camino entre la entrada y la salida.")
