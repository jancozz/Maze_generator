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

        button_style = {"width": 120, "height": 32, "corner_radius": 6}

        # --- FILA 1 ---
        btn_dfs = ctk.CTkButton(
            frame, text="Nuevo laberinto",
            command=lambda: self.start_play(),
            **button_style
        )
        btn_dfs.grid(row=0, column=0, padx=12, pady=5)

        btn_astar = ctk.CTkButton(
            frame, text="Resolver",
            command=lambda: self.controller.solve_maze(),
            **button_style
        )
        btn_astar.grid(row=0, column=1, padx=12, pady=5)

        btn_reset = ctk.CTkButton(
            frame, text="Reiniciar",
            command=self.reset_manual_mode,
            **button_style
        )
        btn_reset.grid(row=0, column=3, padx=12, pady=5)

    def start_play(self):
        self.controller.generate_maze(25,25)
        self.start_manual_mode()

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

    def draw_path_animated(self, path, delay, color="#057032"):
        """Dibuja el camino como una línea animada que crece paso a paso."""

        def draw_step(index):
            if index == 0:
                draw_step(index + 1)
                return

            if index >= len(path):
                self.update_info(
                    f"Camino encontrado: {len(path) - 1} movimientos"
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
            "Usa las flechas del teclado para moverte"
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
                    f"Movimientos: {len(self.manual_path) - 1}"
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
