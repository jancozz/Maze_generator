class Graph:
    """Representa un laberinto como grafo no dirigido.

    Cada nodo (x, y) representa una celda del laberinto, y las aristas
    indican pasajes entre celdas adyacentes.
    """

    def __init__(self, width, height):
        """Inicializa un grafo vacío con dimensiones especificadas."""
        self.width = width
        self.height = height
        self.adjacency = {}
        self.entry = None
        self.exit = None

    def add_node(self, node):
        """Agrega un nodo al grafo si no existe."""
        if node not in self.adjacency:
            self.adjacency[node] = []

    def add_edge(self, node1, node2):
        """Agrega una arista bidireccional entre dos nodos."""
        self.add_node(node1)
        self.add_node(node2)
        if node2 not in self.adjacency[node1]:
            self.adjacency[node1].append(node2)
        if node1 not in self.adjacency[node2]:
            self.adjacency[node2].append(node1)

    def neighbors(self, node):
        """Retorna la lista de nodos vecinos."""
        return self.adjacency.get(node, [])

    def nodes(self):
        """Retorna todos los nodos del grafo."""
        return list(self.adjacency.keys())

    def __repr__(self):
        """Representación en string del grafo."""
        return f"Graph({self.width}x{self.height}, {len(self.adjacency)} nodos)"