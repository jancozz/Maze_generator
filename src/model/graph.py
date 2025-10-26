class Graph:
    """
    Representa directamente el laberinto como un grafo no dirigido.
    Cada nodo (x, y) es una celda del laberinto, y las aristas indican pasajes.
    """

    def __init__(self, width, height):
        """
        Inicializa un grafo vacío para representar el laberinto.
        """
        self.width = width
        self.height = height
        self.adjacency = {}     # Diccionario vació para almacenar conexiones
        self.entry = None
        self.exit = None

    def add_node(self, node):
        """
        Agrega un nodo (celda) al grafo si no existe.

        Un nodo es simplemente una tupla (x, y) que representa
        una coordenada en el laberinto.
        """
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
        """
        Retorna la lista de nodos vecinos (celdas conectadas) de un nodo dado.
        """
        return self.adjacency.get(node, [])

    def nodes(self):
        """
        Retorna una lista con todos los nodos (celdas) del grafo.
        """
        return list(self.adjacency.keys())
