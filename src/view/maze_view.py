from tkinter import messagebox

import customtkinter as ctk


class MazeView:
    """Vista gráfica del laberinto usando customtkinter."""

    def __init__(self, root, controller):
        """Inicializa la vista con canvas y controles."""
        self.root = root
        self.controller = controller
        self.cell_size = 25
        self.margin = 15
        self.difficulties = {
            "Pequeño": {"size": (25, 25), "passages": 0.7},
            "Mediano": {"size": (35, 25), "passages": 0.5},
            "Grande": {"size": (45, 30), "passages": 0.3}
        }
        self.current_difficulty = "Pequeño"

        # Calcular tamaño inicial de canvas
        initial_size = self.difficulties["Pequeño"]["size"]
        self.canvas_size = max(initial_size) * self.cell_size + self.margin * 2
        self.mode = "maze"

        # Variables para modo manual
        self.manual_mode = False
        self.player_position = None
        self.manual_path = []
        self.player_marker = None

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
        self.canvas.pack(pady=0)

        self.setup_controls()

        # Vincular teclas para modo manual
        self.root.bind('<Up>', lambda e: self.move_player(0, -1))
        self.root.bind('<Down>', lambda e: self.move_player(0, 1))
        self.root.bind('<Left>', lambda e: self.move_player(-1, 0))
        self.root.bind('<Right>', lambda e: self.move_player(1, 0))

    def setup_controls(self):
        """Crea los botones de control para generar y resolver."""
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10)

        button_style = {"width": 150, "height": 32, "corner_radius": 6}

        # --- FILA 1 ---
        difficulty_selector = ctk.CTkSegmentedButton(
            frame,
            values=["Pequeño", "Mediano", "Grande"],
            command=self.change_difficulty,
            width=360,
            selected_color="gray"
        )
        difficulty_selector.set("Pequeño")
        difficulty_selector.grid(row=0, column=0, columnspan=4, padx=8, pady=5)

        # --- FILA 2 ---
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

        btn_manual = ctk.CTkButton(
            frame, text="Modo Manual",
            command=self.start_manual_mode,
            **button_style
        )
        btn_manual.grid(row=1, column=3, padx=8, pady=5)

        # --- FILA 3 ---
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

        btn_reset = ctk.CTkButton(
            frame, text="Reiniciar",
            command=self.reset_manual_mode,
            **button_style
        )
        btn_reset.grid(row=2, column=3, padx=8, pady=5)

    def change_difficulty(self, value):
        """Cambia la dificultad y redimensiona el canvas."""
        self.current_difficulty = value
        config = self.difficulties[value]
        width, height = config["size"]
        self.resize_canvas(width, height)
        self.canvas.delete("all")

        self.update_info(f"Tamaño: {value} ({width}x{height} celdas)")

    def resize_canvas(self, width, height):
        """Redimensiona el canvas y la ventana según el tamaño del laberinto."""
        canvas_width = width * self.cell_size + self.margin * 2
        canvas_height = height * self.cell_size + self.margin * 2

        self.canvas.configure(width=canvas_width, height=canvas_height)

        window_width = canvas_width + 30
        window_height = canvas_height + 185

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) * 0.25)

        self.root.geometry(
            f"{window_width}x{window_height}+{x_position}+{y_position}"
        )

    def create_maze(self, algorithm):
        """Genera un laberinto con la dificultad seleccionada."""
        config = self.difficulties[self.current_difficulty]
        width, height = config["size"]
        passages_ratio = config["passages"]

        self.resize_canvas(width, height)
        self.controller.generate_maze(width, height, algorithm, passages_ratio)

    def update_info(self, text):
        """Actualiza el label de información."""
        self.info_label.configure(text=text)

    def draw_maze(self, graph):
        """Dibuja el laberinto con paredes según las adyacencias del grafo."""
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
                    self.canvas.create_line(
                        x1, y1, x2, y1, width=2, fill=wall_color
                    )
                # Pared inferior
                if (x, y + 1) not in neighbors:
                    self.canvas.create_line(
                        x1, y2, x2, y2, width=2, fill=wall_color
                    )
                # Pared derecha
                if (x + 1, y) not in neighbors:
                    self.canvas.create_line(
                        x2, y1, x2, y2, width=2, fill=wall_color
                    )
                # Pared izquierda
                if (x - 1, y) not in neighbors:
                    self.canvas.create_line(
                        x1, y1, x1, y2, width=2, fill=wall_color
                    )

        if graph.exit:
            self.draw_opening(graph.exit, graph.width)

        self.draw_exit_arrow(graph)

    def draw_opening(self, node, width):
        """Abre la pared del borde en la entrada o salida."""
        x, y = node
        x1 = x * self.cell_size + self.margin
        y1 = y * self.cell_size + self.margin
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        if x == width - 1:
            self.canvas.create_line(x2, y1, x2, y2, fill="#1e1e1e", width=3)

    def draw_exit_arrow(self, graph):
        """Dibuja el marcador de entrada y la flecha de salida."""
        if graph.entry:
            x = (graph.entry[0] * self.cell_size + self.margin +
                 self.cell_size // 2)
            y = (graph.entry[1] * self.cell_size + self.margin +
                 self.cell_size // 2)
            radius = 7

            self.canvas.delete("player")

            self.canvas.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                fill="#54AFFF", outline="#0070D1", width=2, tags="player"
            )

        if graph.exit:
            sx, sy = graph.exit
            sy_center = sy * self.cell_size + self.margin + self.cell_size // 2
            x_start = sx * self.cell_size + self.margin + self.cell_size - 5
            x_end = sx * self.cell_size + self.margin + self.cell_size + 10
            self.canvas.create_line(
                x_start, sy_center, x_end, sy_center,
                fill="red", width=3, arrow="last"
            )

    def draw_visited_nodes(self, visited, exclude_path=None):
        """Dibuja los nodos visitados durante la búsqueda."""
        if exclude_path is None:
            exclude_path = set()

        for node in visited:
            if node not in exclude_path:
                x = (node[0] * self.cell_size + self.margin +
                     self.cell_size // 2)
                y = (node[1] * self.cell_size + self.margin +
                     self.cell_size // 2)
                radius = 3
                self.canvas.create_oval(
                    x - radius, y - radius,
                    x + radius, y + radius,
                    fill="#FFD700", outline="", tags="visited"
                )

    def draw_path_animated(self, path, delay, visited=None, color="#057032"):
        """Dibuja el camino de solución de forma animada."""
        if visited:
            path_set = set(path)
            self.draw_visited_nodes(visited, exclude_path=path_set)

        def draw_step(index):
            """Dibuja un paso del camino."""
            if index == 0:
                draw_step(index + 1)
                return

            if index >= len(path):
                self.update_info(
                    f"Camino encontrado: {len(path) - 1} movimientos | "
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
                x1 = (x1 + x2) / 2
                y1 = (y1 + y2) / 2

            self.canvas.create_line(
                x1, y1, x2, y2, fill=color, width=6, tags="path"
            )
            self.root.after(delay, lambda: draw_step(index + 1))

        draw_step(0)

    def draw_graph(self, graph):
        """Dibuja la representación en grafo del laberinto."""
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
        """Cambia a la visualización de grafo."""
        if self.controller.graph:
            self.mode = "graph"
            self.draw_graph(self.controller.graph)
            self.update_info("Vista de Grafo - Nodos y aristas del laberinto")
        else:
            messagebox.showerror("Error", "Primero debes generar un laberinto.")

    def show_maze(self):
        """Cambia a la visualización de laberinto."""
        if self.controller.graph:
            self.mode = "maze"
            self.draw_maze(self.controller.graph)
            self.update_info("Vista de Laberinto - Listo para resolver")
        else:
            messagebox.showerror("Error", "Primero debes generar un laberinto.")

    def start_manual_mode(self):
        """Inicia el modo de juego manual."""
        if not self.controller.graph:
            messagebox.showerror("Error", "Primero debes generar un laberinto.")
            return

        if not self.controller.graph.entry:
            messagebox.showerror(
                "Error", "El laberinto no tiene punto de entrada."
            )
            return

        self.manual_mode = True
        self.player_position = self.controller.graph.entry
        self.manual_path = [self.player_position]

        self.draw_maze(self.controller.graph)
        self.draw_player()

        self.update_info("Modo Manual - Usa las flechas del teclado para moverte")

    def reset_manual_mode(self):
        """Reinicia el modo manual al punto de entrada."""
        if not self.controller.graph:
            messagebox.showerror("Error", "Primero debes generar un laberinto.")
            return

        if not self.manual_mode:
            messagebox.showerror(
                "Error",
                "Primero debes iniciar el modo manual.\n\n"
                "Presiona el botón 'Modo Manual' para comenzar."
            )
            return

        self.player_position = self.controller.graph.entry
        self.manual_path = [self.player_position]

        self.draw_maze(self.controller.graph)
        self.draw_player()

        self.update_info("Reiniciado | Usa las flechas del teclado para moverte")

    def move_player(self, dx, dy):
        """Mueve al jugador en la dirección especificada."""
        if not self.manual_mode or not self.player_position:
            return

        current = self.player_position
        new_position = (current[0] + dx, current[1] + dy)

        neighbors = self.controller.graph.neighbors(current)

        if new_position in neighbors:
            self.player_position = new_position
            self.manual_path.append(new_position)

            self.draw_maze(self.controller.graph)
            self.draw_manual_path()
            self.draw_player()

            if self.player_position == self.controller.graph.exit:
                messagebox.showinfo(
                    "¡Felicitaciones!", "¡Completaste el laberinto!"
                )
                self.update_info(
                    f"Completado en {len(self.manual_path) - 1} movimientos"
                )
                self.manual_mode = False
            else:
                self.update_info(
                    f"Modo Manual | Movimientos: {len(self.manual_path) - 1}"
                )
        else:
            # Efecto visual de movimiento inválido
            canvas_width = (self.controller.graph.width * self.cell_size +
                            self.margin * 2)
            canvas_height = (self.controller.graph.height * self.cell_size +
                             self.margin * 2)
            self.canvas.create_rectangle(
                0, 0, canvas_width, canvas_height,
                fill="", outline="#FF0000", width=5, tags="invalid"
            )
            self.root.after(100, lambda: self.canvas.delete("invalid"))

    def draw_player(self):
        """Dibuja el marcador del jugador en su posición actual."""
        if not self.player_position:
            return

        x = (self.player_position[0] * self.cell_size + self.margin +
             self.cell_size // 2)
        y = (self.player_position[1] * self.cell_size + self.margin +
             self.cell_size // 2)
        radius = 7

        self.canvas.delete("player")

        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill="#54AFFF", outline="#0070D1", width=2, tags="player"
        )

    def draw_manual_path(self):
        """Dibuja el camino recorrido por el jugador."""
        if len(self.manual_path) < 2:
            return

        for i in range(1, len(self.manual_path)):
            x1, y1 = self.manual_path[i - 1]
            x2, y2 = self.manual_path[i]

            x1 = x1 * self.cell_size + self.margin + self.cell_size // 2
            y1 = y1 * self.cell_size + self.margin + self.cell_size // 2
            x2 = x2 * self.cell_size + self.margin + self.cell_size // 2
            y2 = y2 * self.cell_size + self.margin + self.cell_size // 2

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="#4CAF50", width=4, tags="manual_path"
            )