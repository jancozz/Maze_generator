from .cell import Cell

class Maze:
    """
    Representa la estructura del laberinto como una cuadrícula de celdas.
    """
    def __init__(self, width, height):
        """
        Inicializa el laberinto con una cuadrícula de celdas.
        """
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]

    def get_neighbors(self, cell):
        """
        Devuelve una lista de celdas vecinas accesibles (sin pared).
        """
        neighbors = []
        x, y = cell.x, cell.y
        directions = {
            'N': (0, -1),
            'S': (0, 1),
            'E': (1, 0),
            'W': (-1, 0)
        }

        for dir, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not cell.walls[dir]:
                    neighbors.append(self.grid[nx][ny])
        return neighbors
