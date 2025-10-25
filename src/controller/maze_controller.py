from tkinter import messagebox
from model.graph import Graph
from model.algorithms import (
    generate_maze_dfs,
    solve_maze_astar
)
from view.maze_view import MazeView


class MazeController:
    """Controlador principal que conecta la vista con la lógica del laberinto."""

    def __init__(self, root):
        self.graph = None
        self.view = MazeView(root, self)

    def generate_maze(self, width, height):
        """Genera un nuevo laberinto."""
        self.graph = Graph(width, height)

        self.view.update_info(f"Generando laberinto...")

        generate_maze_dfs(self.graph)

        self.view.draw_maze(self.graph)
        self.view.update_info(f"Laberinto generado")

    def solve_maze(self):
        """Resuelve el laberinto"""
        if not self.graph:
            messagebox.showerror("Error", "Primero debes generar un laberinto.")
            return

        start = self.graph.entry
        end = self.graph.exit

        if not start or not end:
            messagebox.showerror("Error", "El laberinto no tiene puntos de entrada o salida.")
            return

        self.view.draw_maze(self.graph)

        self.view.update_info(f"Resolviendo laberinto...")

        path, visited = solve_maze_astar(self.graph, start, end)
        color = "#057032"

        if path:
            self.view.update_info(f"Resolviendo laberinto...")
            self.view.draw_path_animated(path, delay=30, color=color)
        else:
            messagebox.showerror("Error", "No se encontró un camino entre la entrada y la salida.")
            self.view.update_info("No hay solución disponible")
