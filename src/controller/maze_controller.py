from tkinter import messagebox
import time
from model.graph import Graph
from model.algorithms import (
    generate_maze_dfs, generate_maze_kruskal,
    solve_maze_bfs, solve_maze_astar
)
from view.maze_view import MazeView


class MazeController:
    """Controlador principal que conecta la vista con la lógica del laberinto."""

    def __init__(self, root):
        self.graph = None
        self.view = MazeView(root, self)

    def generate_maze(self, width, height, algorithm):
        """Genera un nuevo laberinto (DFS, Kruskal o Prim)."""
        self.graph = Graph(width, height)
        algorithm = algorithm.upper()

        self.view.update_info(f"Generando laberinto con {algorithm}...")
        start_time = time.time()

        if algorithm == "DFS":
            generate_maze_dfs(self.graph)
        elif algorithm == "KRUSKAL":
            generate_maze_kruskal(self.graph)
        else:
            messagebox.showerror("Error", f"Algoritmo '{algorithm}' no soportado.")
            return

        elapsed = time.time() - start_time
        self.view.draw_maze(self.graph)

        nodes = len(self.graph.nodes())
        edges = sum(len(v) for v in self.graph.adjacency.values()) // 2
        self.view.update_info(f"Laberinto generado con {algorithm} en {elapsed:.3f}s | {nodes} nodos, {edges} aristas")

    def solve_maze(self, algorithm):
        """Resuelve el laberinto con BFS, A* o Dijkstra."""
        if not self.graph:
            messagebox.showerror("Error", "Primero debes generar un laberinto.")
            return

        start = self.graph.entry
        end = self.graph.exit

        if not start or not end:
            messagebox.showerror("Error", "El laberinto no tiene puntos de entrada o salida.")
            return

        algorithm = algorithm.upper()

        if self.view.mode == "maze":
            self.view.draw_maze(self.graph)
        else:
            self.view.draw_graph(self.graph)

        self.view.update_info(f"Resolviendo con {algorithm}...")
        start_time = time.time()

        if algorithm == "ASTAR":
            path, visited = solve_maze_astar(self.graph, start, end)
            color = "#057032"
            algo_name = "A*"
        elif algorithm == "BFS":
            path, visited = solve_maze_bfs(self.graph, start, end)
            color = "#6909C8"
            algo_name = "BFS"
        else:
            messagebox.showerror("Error", f"Algoritmo de resolución no soportado: {algorithm}")
            return

        elapsed = time.time() - start_time

        if path:
            self.view.update_info(f"Resolviendo con {algo_name}...")
            self.view.draw_path_animated(path, delay=30, visited=visited, color=color)
        else:
            messagebox.showerror("Error", "No se encontró un camino entre la entrada y la salida.")
            self.view.update_info("No hay solución disponible")