class Cell:
    """
    Representa una celda individual dentro del laberinto.
    """
    def __init__(self, x, y):
        """
        Inicializa la celda con coordenadas y paredes activas.
        """
        self.x = x
        self.y = y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
