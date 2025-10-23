from .cell import Cell
from .graph import Graph

class Maze:
    """
    Representa el laberinto y su equivalente en grafo.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.graph = Graph()  # ← aquí guardaremos el grafo
        self.entry = None
        self.exit = None

    def get_neighbors(self, cell):
        """
        Devuelve las celdas vecinas accesibles (sin pared).
        """
        neighbors = []
        x, y = cell.x, cell.y
        directions = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
        for dir, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not cell.walls[dir]:
                    neighbors.append(self.grid[nx][ny])
        return neighbors

    def build_graph(self):
        """
        Construye un grafo basado en las paredes abiertas del laberinto.
        """
        for x in range(self.width):
            for y in range(self.height):
                node = (x, y)
                self.graph.add_node(node)
                cell = self.grid[x][y]
                for neighbor in self.get_neighbors(cell):
                    self.graph.add_edge(node, (neighbor.x, neighbor.y))
