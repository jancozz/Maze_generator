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
        self.cell_size = 25
        self.margin = 15
        self.difficulties = {
            "Fácil": {"size": (25, 25), "passages": 0.5},
            "Intermedio": {"size": (35, 25), "passages": 0.30},
            "Difícil": {"size": (45, 30), "passages": 0.15}
        }
        self.current_difficulty = "Fácil"

        # Calcular tamaño inicial de canvas
        initial_size = self.difficulties["Fácil"]["size"]
        self.canvas_size = max(initial_size) * self.cell_size + self.margin * 2
        self.mode = "maze"

        self.info_label = ctk.CTkLabel(
            root,
            text="Genera un laberinto para comenzar",
            font=("Arial", 13)
        )
        self.info_label.pack(pady=5)

        self.canvas = ctk.CTkCanvas(
            root,
            width=self.canvas_size,
            height=self.canvas_size,
            bg="#1e1e1e",
            highlightthickness=0
        )
        self.canvas.pack(pady=(0, 10))

        self.setup_controls()

    def setup_controls(self):
        """Crea los botones de control para generar y resolver el laberinto."""
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10)

        button_style = {"width": 150, "height": 32, "corner_radius": 6}

        difficulty_selector = ctk.CTkSegmentedButton(
            frame,
            values=["Fácil", "Intermedio", "Difícil"],
            command=self.change_difficulty,
            width=360,
            selected_color="gray"
        )
        difficulty_selector.set("Fácil")
        difficulty_selector.grid(row=0, column=0, columnspan=3, padx=8, pady=5)

        # --- FILA 1 ---
        btn_dfs = ctk.CTkButton(
            frame, text="Generar (DFS)",
            command=lambda: self.create_maze("DFS"),
            **button_style
        )
        btn_dfs.grid(row=1, column=0, padx=8, pady=5)

        btn_bfs = ctk.CTkButton(
            frame, text="Resolver (BFS)",
            command=lambda: self.controller.solve_maze("BFS"),
            **button_style
        )
        btn_bfs.grid(row=1, column=1, padx=8, pady=5)

        btn_graph = ctk.CTkButton(
            frame, text="Ver como Grafo",
            command=self.show_graph,
            **button_style
        )
        btn_graph.grid(row=1, column=2, padx=8, pady=5)

        # --- FILA 2 ---
        btn_kruskal = ctk.CTkButton(
            frame, text="Generar (Kruskal)",
            command=lambda: self.create_maze("Kruskal"),
            **button_style
        )
        btn_kruskal.grid(row=2, column=0, padx=8, pady=5)

        btn_astar = ctk.CTkButton(
            frame, text="Resolver (A*)",
            command=lambda: self.controller.solve_maze("ASTAR"),
            **button_style
        )
        btn_astar.grid(row=2, column=1, padx=8, pady=5)

        btn_maze = ctk.CTkButton(
            frame, text="Ver como Laberinto",
            command=self.show_maze,
            **button_style
        )
        btn_maze.grid(row=2, column=2, padx=8, pady=5)

    def change_difficulty(self, value):
        """Cambia la dificultad seleccionada."""
        self.current_difficulty = value
        config = self.difficulties[value]
        width, height = config["size"]

        self.update_info(f"Dificultad: {value} ({width}x{height} celdas)")

    def resize_canvas(self, width, height):
        """Redimensiona el canvas según el tamaño del laberinto."""
        canvas_width = width * self.cell_size + self.margin * 2
        canvas_height = height * self.cell_size + self.margin * 2

        # Redimensionar canvas
        self.canvas.configure(width=canvas_width, height=canvas_height)

        # Ajustar tamaño de ventana centrada
        window_width = canvas_width + 30
        window_height = canvas_height + 195

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) * 0.25)

        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def create_maze(self, algorithm):
        """Inicia el juego con la dificultad seleccionada."""
        config = self.difficulties[self.current_difficulty]
        width, height = config["size"]
        passages_ratio = config["passages"]

        # Ajustar canvas antes de generar
        self.resize_canvas(width, height)

        self.controller.generate_maze(width, height, algorithm)

    def update_info(self, text):
        """Actualiza el label de información."""
        self.info_label.configure(text=text)

    def draw_maze(self, graph):
        """
        Dibuja el laberinto en el canvas, construyendo paredes según las adyacencias del grafo.
        """
        self.canvas.delete("all")
        wall_color = "#cccccc"

        for x in range(graph.width):
            for y in range(graph.height):
                node = (x, y)
                neighbors = graph.adjacency.get(node, [])
                x1 = x * self.cell_size + self.margin
                y1 = y * self.cell_size + self.margin
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Pared superior
                if (x, y - 1) not in neighbors:
                    self.canvas.create_line(x1, y1, x2, y1, width=2, fill=wall_color)
                # Pared inferior
                if (x, y + 1) not in neighbors:
                    self.canvas.create_line(x1, y2, x2, y2, width=2, fill=wall_color)
                # Pared derecha
                if (x + 1, y) not in neighbors:
                    self.canvas.create_line(x2, y1, x2, y2, width=2, fill=wall_color)
                # Pared izquierda
                if (x - 1, y) not in neighbors:
                    self.canvas.create_line(x1, y1, x1, y2, width=2, fill=wall_color)

        if graph.exit:
            self._draw_opening(graph.exit, graph.width, graph.height)

        # Dibujar flechas de entrada/salida
        self._draw_entry_exit_arrows(graph)

    def _draw_opening(self, node, width, height):
        """Rompe la pared del borde en la entrada o salida."""
        x, y = node
        x1 = x * self.cell_size + self.margin
        y1 = y * self.cell_size + self.margin
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        if x == width - 1:
            # Quitar parte de la pared derecha
            self.canvas.create_line(x2, y1, x2, y2, fill="#1e1e1e", width=3)

    def _draw_entry_exit_arrows(self, graph):
        """Dibuja las flechas de entrada y salida en los bordes."""
        # Entrada
        if graph.entry:
            x = graph.entry[0] * self.cell_size + self.margin + self.cell_size // 2
            y = graph.entry[1] * self.cell_size + self.margin + self.cell_size // 2
            radius = 6

            # Borrar jugador anterior
            self.canvas.delete("player")

            # Dibujar nuevo jugador
            self.canvas.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                fill="#54AFFF", outline="#0070D1", width=2, tags="player"
            )

        # Salida
        if graph.exit:
            sx, sy = graph.exit
            sy_center = sy * self.cell_size + self.margin + self.cell_size // 2
            x_start = sx * self.cell_size + self.margin + self.cell_size - 5
            x_end = sx * self.cell_size + self.margin + self.cell_size + 10
            self.canvas.create_line(x_start, sy_center, x_end, sy_center, fill="red", width=3, arrow="last")

    def draw_visited_nodes(self, visited, exclude_path=None):
        """
        Dibuja los nodos visitados durante la búsqueda.
        Args:
            visited: conjunto de nodos visitados
            exclude_path: conjunto de nodos que están en el camino final (para no pintarlos)
        """
        if exclude_path is None:
            exclude_path = set()

        for node in visited:
            if node not in exclude_path:
                x = node[0] * self.cell_size + self.margin + self.cell_size // 2
                y = node[1] * self.cell_size + self.margin + self.cell_size // 2
                radius = 3
                self.canvas.create_oval(
                    x - radius, y - radius,
                    x + radius, y + radius,
                    fill="#FFD700", outline="", tags="visited"
                )

    def draw_path_animated(self, path, delay, visited=None, color="#057032"):
        """Dibuja el camino como una línea animada que crece paso a paso."""

        # Primero dibujar nodos visitados si están disponibles
        if visited:
            path_set = set(path)
            self.draw_visited_nodes(visited, exclude_path=path_set)

        def draw_step(index):
            if index == 0:
                draw_step(index + 1)
                return

            if index >= len(path):
                self.update_info(
                    f"Camino encontrado: {len(path) - 1} pasos | "
                    f"Nodos explorados: {len(visited) - 1 if visited else '?'}"
                )
                return

            x1, y1 = path[index - 1]
            x2, y2 = path[index]

            x1 = x1 * self.cell_size + self.margin + self.cell_size // 2
            y1 = y1 * self.cell_size + self.margin + self.cell_size // 2
            x2 = x2 * self.cell_size + self.margin + self.cell_size // 2
            y2 = y2 * self.cell_size + self.margin + self.cell_size // 2

            if index == 1:
                # Calcular el punto medio entre el nodo 0 y el nodo 1
                x1 = (x1 + x2) / 2
                y1 = (y1 + y2) / 2

            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=6, tags="path")
            self.root.after(delay, lambda: draw_step(index + 1))

        draw_step(0)

    def draw_graph(self, graph):
        """Dibuja el grafo del laberinto con nodos y aristas."""
        self.canvas.delete("all")
        node_radius = 5
        link_color = "#CFCFCF"
        default_node_color = "#696969"
        start_color = "#0070D1"
        exit_color = "#FF0000"

        # Dibujar aristas
        for node, neighbors in graph.adjacency.items():
            x1 = node[0] * self.cell_size + self.margin + self.cell_size // 2
            y1 = node[1] * self.cell_size + self.margin + self.cell_size // 2
            for n in neighbors:
                x2 = n[0] * self.cell_size + self.margin + self.cell_size // 2
                y2 = n[1] * self.cell_size + self.margin + self.cell_size // 2
                self.canvas.create_line(x1, y1, x2, y2, fill=link_color, width=1)

        # Dibujar nodos
        for node in graph.adjacency.keys():
            x = node[0] * self.cell_size + self.margin + self.cell_size // 2
            y = node[1] * self.cell_size + self.margin + self.cell_size // 2

            if node == graph.entry:
                node_color = start_color
            elif node == graph.exit:
                node_color = exit_color
            else:
                node_color = default_node_color

            self.canvas.create_oval(
                x - node_radius, y - node_radius,
                x + node_radius, y + node_radius,
                fill=node_color, outline=""
            )

    def show_graph(self):
        """Cambia a modo visualización de grafo."""
        if self.controller.graph:
            self.mode = "graph"
            self.draw_graph(self.controller.graph)
            self.update_info("Vista de Grafo - Nodos y aristas del laberinto")

    def show_maze(self):
        """Cambia a modo visualización de laberinto."""
        if self.controller.graph:
            self.mode = "maze"
            self.draw_maze(self.controller.graph)
            self.update_info("Vista de Laberinto - Listo para resolver")
