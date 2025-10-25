class Graph:
    """
    Representa directamente el laberinto como un grafo no dirigido.
    Cada nodo (x, y) es una celda del laberinto, y las aristas indican pasajes.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.adjacency = {}
        self.entry = None
        self.exit = None

    def add_node(self, node):
        if node not in self.adjacency:
            self.adjacency[node] = []

    def add_edge(self, node1, node2):
        """Agrega una arista bidireccional entre node1 y node2."""
        self.add_node(node1)
        self.add_node(node2)
        if node2 not in self.adjacency[node1]:
            self.adjacency[node1].append(node2)
        if node1 not in self.adjacency[node2]:
            self.adjacency[node2].append(node1)

    def neighbors(self, node):
        return self.adjacency.get(node, [])

    def nodes(self):
        return list(self.adjacency.keys())
