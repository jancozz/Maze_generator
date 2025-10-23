class Graph:
    """
    Representa el laberinto como un grafo no dirigido.
    Cada celda (x, y) es un nodo, y las conexiones sin paredes son aristas.
    """

    def __init__(self):
        self.adjacency = {}  # { nodo: [vecinos] }

    def add_node(self, node):
        """Agrega un nodo si no existe."""
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
        """Devuelve los vecinos conectados de un nodo."""
        return self.adjacency.get(node, [])

    def nodes(self):
        """Devuelve todos los nodos del grafo."""
        return list(self.adjacency.keys())

    def __repr__(self):
        return f"Graph({len(self.adjacency)} nodos)"
