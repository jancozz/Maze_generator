from tkinter import messagebox

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
        self.mode = "maze"

        # Variables para modo manual
        self.manual_mode = False
        self.player_position = None
        self.manual_path = []
        self.player_marker = None

        self.info_label = ctk.CTkLabel(
            root,
            text="Genera un laberinto para comenzar",
            font=("Arial", 12)
        )
        self.info_label.pack(pady=5)

        self.canvas = ctk.CTkCanvas(
            root,
            width=705,
            height=705,
            bg="#1e1e1e",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)

        self.setup_controls()

        # Vincular teclas para modo manual
        self.root.bind('<Up>', lambda e: self.move_player(0, -1))
        self.root.bind('<Down>', lambda e: self.move_player(0, 1))
        self.root.bind('<Left>', lambda e: self.move_player(-1, 0))
        self.root.bind('<Right>', lambda e: self.move_player(1, 0))

    def setup_controls(self):
        """Crea los botones de control para generar y resolver el laberinto."""
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
            command=lambda: self.controller.solve_maze("BFS"),
            **button_style
        )
        btn_bfs.grid(row=0, column=1, padx=8, pady=5)

        btn_graph = ctk.CTkButton(
            frame, text="Ver como Grafo",
            command=self.show_graph,
            **button_style
        )
        btn_graph.grid(row=0, column=2, padx=8, pady=5)

        btn_manual = ctk.CTkButton(
            frame, text="Modo Manual",
            command=self.start_manual_mode,
            **button_style
        )
        btn_manual.grid(row=0, column=3, padx=8, pady=5)

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

        btn_reset = ctk.CTkButton(
            frame, text="Reiniciar",
            command=self.reset_manual_mode,
            **button_style
        )
        btn_reset.grid(row=1, column=3, padx=8, pady=5)

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

        # Dibujar aperturas (roturas) en entrada y salida
        if graph.entry:
            self._draw_opening(graph.entry, graph.width, graph.height)

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

        if x == 0:
            # Quitar parte de la pared izquierda
            self.canvas.create_line(x1, y1, x1, y2, fill="#1e1e1e", width=3)
        elif x == width - 1:
            # Quitar parte de la pared derecha
            self.canvas.create_line(x2, y1, x2, y2, fill="#1e1e1e", width=3)
        elif y == 0:
            # Quitar parte de la pared superior
            self.canvas.create_line(x1, y1, x2, y1, fill="#1e1e1e", width=3)
        elif y == height - 1:
            # Quitar parte de la pared inferior
            self.canvas.create_line(x1, y2, x2, y2, fill="#1e1e1e", width=3)

    def _draw_entry_exit_arrows(self, graph):
        """Dibuja las flechas de entrada y salida en los bordes."""
        # Entrada
        if graph.entry:
            ex, ey = graph.entry
            ey_center = ey * self.cell_size + self.margin + self.cell_size // 2
            x_start = ex * self.cell_size + self.margin - 5
            x_end = ex * self.cell_size + self.margin + 10
            self.canvas.create_line(x_start, ey_center, x_end, ey_center, fill="red", width=3, arrow="last")

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

            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=6, tags="path")
            self.root.after(delay, lambda: draw_step(index + 1))

        draw_step(0)

    def draw_graph(self, graph):
        """Dibuja el grafo del laberinto con nodos y aristas."""
        self.canvas.delete("all")
        node_radius = 5
        link_color = "#CFCFCF"
        default_node_color = "#696969"
        entry_exit_color = "#FF0000"

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

            if node == graph.entry or node == graph.exit:
                node_color = entry_exit_color
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
        else:
            messagebox.showerror("Error", "Primero debes generar un laberinto.")

    def show_maze(self):
        """Cambia a modo visualización de laberinto."""
        if self.controller.graph:
            self.mode = "maze"
            self.draw_maze(self.controller.graph)
            self.update_info("Vista de Laberinto - Listo para resolver")
        else:
            messagebox.showerror("Error", "Primero debes generar un laberinto.")

    def start_manual_mode(self):
        """Inicia el modo manual."""
        if not self.controller.graph:
            messagebox.showerror("Error", "Primero debes generar un laberinto.")
            return

        if not self.controller.graph.entry:
            messagebox.showerror("Error", "El laberinto no tiene punto de entrada.")
            return

        self.manual_mode = True
        self.player_position = self.controller.graph.entry
        self.manual_path = [self.player_position]

        # Redibujar el laberinto limpio
        self.draw_maze(self.controller.graph)

        # Dibujar el jugador
        self.draw_player()

        self.update_info(
            "Modo Manual - Usa las flechas del teclado para moverte"
        )

    def reset_manual_mode(self):
        """Reinicia el modo manual."""
        # Validar que haya un laberinto generado
        if not self.controller.graph:
            messagebox.showerror("Error", "Primero debes generar un laberinto.")
            return

        # Validar que esté en modo manual
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

        self.update_info(
            "Reiniciado | Usa las flechas del teclado para moverte"
        )

    def move_player(self, dx, dy):
        """Mueve al jugador en la dirección especificada."""
        if not self.manual_mode or not self.player_position:
            return

        current = self.player_position
        new_position = (current[0] + dx, current[1] + dy)

        # Verificar si el movimiento es válido (hay arista en el grafo)
        neighbors = self.controller.graph.neighbors(current)

        if new_position in neighbors:
            self.player_position = new_position
            self.manual_path.append(new_position)

            # Redibujar
            self.draw_maze(self.controller.graph)
            self.draw_manual_path()
            self.draw_player()

            # Verificar si llegó a la salida
            if self.player_position == self.controller.graph.exit:
                messagebox.showinfo("¡Ganaste!", "Has llegado a la salida del laberinto")
                self.update_info(
                    f"Completado en {len(self.manual_path) - 1} movimientos"
                )
                self.manual_mode = False
            else:
                self.update_info(
                    f"Modo Manual | Movimientos: {len(self.manual_path) - 1}"
                )
        else:
            # Movimiento inválido (hay pared)
            self.canvas.create_rectangle(
                0, 0, 705, 705,
                fill="", outline="#FF0000", width=5, tags="invalid"
            )
            self.root.after(100, lambda: self.canvas.delete("invalid"))

    def draw_player(self):
        """Dibuja al jugador en su posición actual."""
        if not self.player_position:
            return

        x = self.player_position[0] * self.cell_size + self.margin + self.cell_size // 2
        y = self.player_position[1] * self.cell_size + self.margin + self.cell_size // 2
        radius = 6

        # Borrar jugador anterior
        self.canvas.delete("player")

        # Dibujar nuevo jugador
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill="#FFD700", outline="#FFA000", width=2, tags="player"
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
