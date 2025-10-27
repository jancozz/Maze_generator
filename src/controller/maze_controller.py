from tkinter import messagebox
from model.graph import Graph
from model.algorithms import (
    generate_maze_dfs, generate_maze_kruskal,
    solve_maze_bfs, solve_maze_astar
)
from view.maze_view import MazeView


class MazeController:
    """Controlador que conecta la vista con la lógica del laberinto."""

    def __init__(self, root):
        """Inicializa el controlador con la ventana raíz de Tkinter."""
        self.graph = None
        self.view = MazeView(root, self)

    def generate_maze(self, width, height, algorithm, passages_ratio):
        """Genera un nuevo laberinto usando el algoritmo especificado."""
        self.graph = Graph(width, height)

        self.view.update_info(f"Generando laberinto con {algorithm}...")

        if algorithm == "DFS":
            generate_maze_dfs(self.graph, passages_ratio)
        elif algorithm == "Kruskal":
            generate_maze_kruskal(self.graph, passages_ratio)
        else:
            messagebox.showerror("Error", f"Algoritmo '{algorithm}' no soportado.")
            return

        self.view.draw_maze(self.graph)

        nodes = len(self.graph.nodes())
        edges = sum(len(v) for v in self.graph.adjacency.values()) // 2
        self.view.update_info(
            f"Laberinto generado con {algorithm} | {nodes} nodos, {edges} aristas"
        )

    def solve_maze(self, algorithm):
        """Resuelve el laberinto con el algoritmo especificado."""
        if not self.graph:
            messagebox.showerror("Error", "Primero debes generar un laberinto.")
            return

        start = self.graph.entry
        end = self.graph.exit

        if not start or not end:
            messagebox.showerror(
                "Error", "El laberinto no tiene puntos de entrada o salida."
            )
            return

        if self.view.mode == "maze":
            self.view.draw_maze(self.graph)
        else:
            self.view.draw_graph(self.graph)

        self.view.update_info(f"Resolviendo con {algorithm}...")

        if algorithm == "ASTAR":
            path, visited = solve_maze_astar(self.graph, start, end)
            color = "#057032"
            algo_name = "A*"
        elif algorithm == "BFS":
            path, visited = solve_maze_bfs(self.graph, start, end)
            color = "#6909C8"
            algo_name = "BFS"
        else:
            messagebox.showerror(
                "Error", f"Algoritmo de resolución no soportado: {algorithm}"
            )
            return

        if path:
            self.view.update_info(f"Resolviendo con {algo_name}...")
            self.view.draw_path_animated(path, delay=30, visited=visited, color=color)
        else:
            messagebox.showerror(
                "Error", "No se encontró un camino entre la entrada y la salida."
            )
            self.view.update_info("No hay solución disponible")