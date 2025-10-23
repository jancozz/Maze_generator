import customtkinter as ctk

class MazeView:
    """
    Vista gráfica del laberinto usando customtkinter.
    Dibuja la cuadrícula, botones de control y el camino resuelto.
    """
    def __init__(self, root, controller):
        """
        Inicializa la vista con canvas y controles.
        """
        self.root = root
        self.controller = controller
        self.cell_size = 27
        self.margin = 15

        self.canvas = ctk.CTkCanvas(root, width=705, height=705, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.setup_controls()

    def setup_controls(self):
        """
        Crea los botones de control para generar y resolver el laberinto.
        """
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10)

        button_style = {"width": 150, "height": 32, "corner_radius": 6}

        # --- FILA 1 ---
        btn_dfs = ctk.CTkButton(
            frame, text="Generar (DFS)",
            command=lambda: self.controller.generate_maze(25, 25, "DFS"),
            **button_style
        )
        btn_dfs.grid(row=0, column=0, padx=8, pady=5)

        btn_bfs = ctk.CTkButton(
            frame, text="Resolver (BFS)",
            command=lambda: self.controller.solve_maze(""),
            **button_style
        )
        btn_bfs.grid(row=0, column=1, padx=8, pady=5)

        btn_graph = ctk.CTkButton(
            frame, text="Ver como Grafo",
            command=self.show_graph,
            **button_style
        )
        btn_graph.grid(row=0, column=2, padx=8, pady=5)

        # --- FILA 2 ---
        btn_kruskal = ctk.CTkButton(
            frame, text="Generar (Kruskal)",
            command=lambda: self.controller.generate_maze(25, 25, "Kruskal"),
            **button_style
        )
        btn_kruskal.grid(row=1, column=0, padx=8, pady=5)

        btn_astar = ctk.CTkButton(
            frame, text="Resolver (A*)",
            command=lambda: self.controller.solve_maze("ASTAR"),
            **button_style
        )
        btn_astar.grid(row=1, column=1, padx=8, pady=5)

        btn_maze = ctk.CTkButton(
            frame, text="Ver como Laberinto",
            command=self.show_maze,
            **button_style
        )
        btn_maze.grid(row=1, column=2, padx=8, pady=5)

    def draw_maze(self, maze):
        """
        Dibuja las paredes del laberinto en el canvas.
        """
        self.canvas.delete("all")
        for x in range(maze.width):
            for y in range(maze.height):
                cell = maze.grid[x][y]
                x1 = x * self.cell_size + self.margin
                y1 = y * self.cell_size + self.margin
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                wall_color = "#cccccc"
                if cell.walls['N']:
                    self.canvas.create_line(x1, y1, x2, y1, width=2, fill=wall_color)
                if cell.walls['S']:
                    self.canvas.create_line(x1, y2, x2, y2, width=2, fill=wall_color)
                if cell.walls['E']:
                    self.canvas.create_line(x2, y1, x2, y2, width=2, fill=wall_color)
                if cell.walls['W']:
                    self.canvas.create_line(x1, y1, x1, y2, width=2, fill=wall_color)

        # Flecha de entrada
        ex, ey = maze.entry
        ey_center = ey * self.cell_size + self.margin + self.cell_size // 2
        x_start = ex * self.cell_size + self.margin - 5
        x_end = ex * self.cell_size + self.margin + 10
        self.canvas.create_line(x_start, ey_center, x_end, ey_center, fill="red", width=3, arrow="last")

        # Flecha de salida
        sx, sy = maze.exit
        sy_center = sy * self.cell_size + self.margin + self.cell_size // 2
        x_start = sx * self.cell_size + self.margin + self.cell_size - 5
        x_end = sx * self.cell_size + self.margin + self.cell_size + 10
        self.canvas.create_line(x_start, sy_center, x_end, sy_center, fill="red", width=3, arrow="last")

    def draw_path_animated(self, path, delay, visited=None, color="#057032"):
        """
        Dibuja el camino como una línea animada que crece paso a paso.
        """

        def draw_step(index):
            if index == 0:
                draw_step(index + 1)
                return

            if index >= len(path):
                return

            x1, y1 = path[index - 1]
            x2, y2 = path[index]

            x1 = x1 * self.cell_size + self.margin + self.cell_size // 2
            y1 = y1 * self.cell_size + self.margin + self.cell_size // 2
            x2 = x2 * self.cell_size + self.margin + self.cell_size // 2
            y2 = y2 * self.cell_size + self.margin + self.cell_size // 2

            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=6)
            self.root.after(delay, lambda: draw_step(index + 1))

        draw_step(0)

    def draw_graph(self, graph):
        """
        Dibuja el grafo del laberinto con nodos y aristas.
        """
        self.canvas.delete("all")

        node_radius = 5
        link_color = "#CFCFCF"
        node_color = "#696969"

        for node, neighbors in graph.adjacency.items():
            x1 = node[0] * self.cell_size + self.margin + self.cell_size // 2
            y1 = node[1] * self.cell_size + self.margin + self.cell_size // 2
            for n in neighbors:
                x2 = n[0] * self.cell_size + self.margin + self.cell_size // 2
                y2 = n[1] * self.cell_size + self.margin + self.cell_size // 2
                self.canvas.create_line(x1, y1, x2, y2, fill=link_color, width=1)

        for node in graph.adjacency.keys():
            x = node[0] * self.cell_size + self.margin + self.cell_size // 2
            y = node[1] * self.cell_size + self.margin + self.cell_size // 2
            self.canvas.create_oval(
                x - node_radius, y - node_radius,
                x + node_radius, y + node_radius,
                fill=node_color, outline=""
            )

    def show_graph(self):
        """Cambia a modo visualización de grafo."""
        if self.controller.maze:
            self.mode = "graph"
            self.draw_graph(self.controller.maze.graph)

    def show_maze(self):
        """Cambia a modo visualización de laberinto."""
        if self.controller.maze:
            self.mode = "maze"
            self.draw_maze(self.controller.maze)
