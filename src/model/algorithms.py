import random

class DisjointSet:
    """
    Estructura de conjuntos disjuntos para Kruskal.
    Permite unir celdas y verificar si están conectadas sin formar ciclos.
    """

    def __init__(self, width, height):
        """
        Inicializa cada celda como su propio conjunto.
        """
        self.parent = {(x, y): (x, y) for x in range(width) for y in range(height)}

    def find(self, cell):
        """
        Encuentra el representante del conjunto al que pertenece la celda.
        Aplica compresión de caminos.
        """
        if self.parent[cell] != cell:
            self.parent[cell] = self.find(self.parent[cell])
        return self.parent[cell]

    def union(self, cell1, cell2):
        """
        Une dos conjuntos si no están conectados.
        Retorna True si se realizó la unión.
        """
        root1 = self.find(cell1)
        root2 = self.find(cell2)
        if root1 != root2:
            self.parent[root2] = root1
            return True
        return False

def get_border_cells(maze):
    """
    Devuelve una lista de todas las celdas en el borde del laberinto.
    """
    border = []
    w, h = maze.width, maze.height
    for x in range(w):
        border.append((x, 0))
        border.append((x, h - 1))
    for y in range(h):
        border.append((0, y))
        border.append((w - 1, y))
    return border

def open_border_wall(maze, cell):
    """
    Abre la pared correspondiente si la celda está en el borde.
    """
    x, y = cell
    if x == 0:
        maze.grid[x][y].walls['W'] = False
    elif x == maze.width - 1:
        maze.grid[x][y].walls['E'] = False
    elif y == 0:
        maze.grid[x][y].walls['N'] = False
    elif y == maze.height - 1:
        maze.grid[x][y].walls['S'] = False

def assign_entry_exit(maze):
    """
    Asigna entrada y salida aleatorias con preferencia de izquierda a derecha.
    """
    border_cells = get_border_cells(maze)
    entry_candidates = [(0, y) for y in range(maze.height)]
    exit_candidates = [(maze.width - 1, y) for y in range(maze.height)]

    entry = random.choice(entry_candidates)
    exit = random.choice(exit_candidates)

    # Evitar que entrada y salida sean iguales
    while exit == entry:
        exit = random.choice(border_cells)

    open_border_wall(maze, entry)
    open_border_wall(maze, exit)

    maze.entry = entry
    maze.exit = exit

def generate_maze_dfs(maze):
    """
    Genera un laberinto usando DFS recursivo.
    Elimina paredes entre celdas visitadas y define entrada/salida.
    """
    width, height = maze.width, maze.height
    visited = [[False for _ in range(height)] for _ in range(width)]

    def dfs(x, y):
        visited[x][y] = True
        directions = ['N', 'S', 'E', 'W']
        random.shuffle(directions)

        for direction in directions:
            dx, dy = 0, 0
            if direction == 'N':
                dy = -1
            elif direction == 'S':
                dy = 1
            elif direction == 'E':
                dx = 1
            elif direction == 'W':
                dx = -1

            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and not visited[nx][ny]:
                # Eliminar pared entre (x,y) y (nx,ny)
                maze.grid[x][y].walls[direction] = False
                opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
                maze.grid[nx][ny].walls[opposite[direction]] = False
                dfs(nx, ny)

    # Comenzar desde una celda aleatoria
    start_x = random.randint(0, width - 1)
    start_y = random.randint(0, height - 1)
    dfs(start_x, start_y)

    assign_entry_exit(maze)

def generate_maze_kruskal(maze):
    """
    Genera un laberinto usando el algoritmo de Kruskal.
    Une celdas aleatoriamente sin formar ciclos.
    """
    width, height = maze.width, maze.height
    ds = DisjointSet(width, height)
    edges = []

    for x in range(width):
        for y in range(height):
            if x < width - 1:
                edges.append(((x, y), (x + 1, y), 'E'))
            if y < height - 1:
                edges.append(((x, y), (x, y + 1), 'S'))

    random.shuffle(edges)

    for cell1, cell2, direction in edges:
        if ds.union(cell1, cell2):
            x1, y1 = cell1
            x2, y2 = cell2
            maze.grid[x1][y1].walls[direction] = False
            if direction == 'E':
                maze.grid[x2][y2].walls['W'] = False
            elif direction == 'S':
                maze.grid[x2][y2].walls['N'] = False

    assign_entry_exit(maze)

def solve_maze_bfs(maze, start, end):
    """
    Resuelve el laberinto usando BFS.
    Devuelve una lista de coordenadas que forman el camino desde start hasta end.
    """
    queue = [start]
    visited = set()
    came_from = {}
    visited.add(start)

    while queue:
        current = queue.pop(0)
        if current == end:
            break
        x, y = current
        cell = maze.grid[x][y]
        for neighbor in maze.get_neighbors(cell):
            nx, ny = neighbor.x, neighbor.y
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                came_from[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    # Reconstruir camino
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return []
    path.append(start)
    path.reverse()
    return path
