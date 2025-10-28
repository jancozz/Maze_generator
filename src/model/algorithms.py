import random


class DisjointSet:
    """Estructura de conjuntos disjuntos para el algoritmo de Kruskal."""

    def __init__(self, width, height):
        """Inicializa la estructura con todos los nodos como conjuntos independientes."""
        self.parent = {(x, y): (x, y) for x in range(width) for y in range(height)}
        self.rank = {(x, y): 0 for x in range(width) for y in range(height)}

    def find(self, node):
        """Encuentra la raíz del conjunto con compresión de caminos."""
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        """Une dos conjuntos por rango, retorna True si se unieron."""
        root1 = self.find(node1)
        root2 = self.find(node2)
        if root1 != root2:
            if self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            elif self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1
            return True
        return False


def assign_entry_exit(graph):
    """Asigna entrada y salida aleatorias en bordes izquierdo y derecho."""
    entry_candidates = [(0, y) for y in range(graph.height)]
    exit_candidates = [(graph.width - 1, y) for y in range(graph.height)]

    graph.entry = random.choice(entry_candidates)
    graph.exit = random.choice(exit_candidates)


def generate_maze_dfs(graph, passages_ratio):
    """Genera un laberinto usando DFS recursivo."""
    width, height = graph.width, graph.height
    visited = set()
    directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]

    def dfs(x, y):
        """Explora recursivamente desde la posición actual."""
        visited.add((x, y))
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                graph.add_edge((x, y), (nx, ny))
                dfs(nx, ny)

    start = (random.randint(0, width - 1), random.randint(0, height - 1))
    dfs(*start)

    add_extra_passages(graph, ratio=passages_ratio)
    assign_entry_exit(graph)


def generate_maze_kruskal(graph, passages_ratio):
    """Genera un laberinto usando el algoritmo de Kruskal."""
    width, height = graph.width, graph.height
    ds = DisjointSet(width, height)
    edges = []

    # Generar todas las aristas posibles
    for x in range(width):
        for y in range(height):
            if x < width - 1:
                edges.append(((x, y), (x + 1, y)))
            if y < height - 1:
                edges.append(((x, y), (x, y + 1)))

    random.shuffle(edges)

    # Construir árbol de expansión mínima
    for a, b in edges:
        if ds.union(a, b):
            graph.add_edge(a, b)

    add_extra_passages(graph, ratio=passages_ratio)
    assign_entry_exit(graph)


def add_extra_passages(graph, ratio):
    """Agrega pasajes adicionales para aumentar la conectividad."""
    count = int(graph.width * graph.height * ratio)
    for _ in range(count):
        x = random.randint(0, graph.width - 2)
        y = random.randint(0, graph.height - 2)
        if random.choice([True, False]):
            neighbor = (x + 1, y)
        else:
            neighbor = (x, y + 1)
        graph.add_edge((x, y), neighbor)


def solve_maze_bfs(graph, start, end):
    """Resuelve el laberinto usando BFS sin deque."""
    queue = [start]
    visited = {start}
    came_from = {}
    index = 0

    while index < len(queue):
        current = queue[index]
        index += 1

        if current == end:
            break

        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

    # Reconstrucción del camino
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return [], visited
    path.append(start)
    path.reverse()
    return path, visited


def solve_maze_astar(graph, start, end):
    """Resuelve el laberinto usando A* sin heapq."""

    def heuristic(a, b):
        """Calcula la distancia Manhattan entre dos nodos."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_list = [(heuristic(start, end), start)]

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    visited = set()

    while open_list:
        # Buscar el nodo con menor f_score
        open_list.sort(key=lambda x: x[0])
        _, current = open_list.pop(0)

        if current in visited:
            continue

        visited.add(current)

        if current == end:
            break

        for neighbor in graph.neighbors(current):
            if neighbor in visited:
                continue

            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, end)

                open_list.append((f_score[neighbor], neighbor))

    # Reconstrucción del camino
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return [], visited
    path.append(start)
    path.reverse()
    return path, visited
