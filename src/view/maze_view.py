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

        # Variables para modo manual
        self.manual_mode = False
        self.player_position = None
        self.manual_path = []
        self.player_marker = None

        # Sistema de sonido
        self.sound_enabled = True
        self.init_sound_system()

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

    def init_sound_system(self):
        """Inicializa el sistema de sonido."""
        try:
            import winsound
            self.winsound = winsound
            self.use_winsound = True
        except ImportError:
            self.use_winsound = False
            print("winsound no disponible. Sonidos desactivados.")

    def play_sound(self, sound_type):
        """
        Reproduce un sonido según el tipo.
        Tipos: 'move', 'wall', 'victory'
        """
        if not self.sound_enabled or not self.use_winsound:
            return

        try:
            sounds = {
                'move': (450, 50),  # Movimiento
                'wall': (200, 100),  # Choque con pared
            }

            if sound_type == 'victory':
                # Melodía de victoria (4 notas ascendentes)
                self.root.after(0, lambda: self.winsound.Beep(523, 100))  # Do
                self.root.after(120, lambda: self.winsound.Beep(659, 100))  # Mi
                self.root.after(240, lambda: self.winsound.Beep(784, 100))  # Sol
                self.root.after(360, lambda: self.winsound.Beep(1047, 300))  # Do alto
            elif sound_type in sounds:
                freq, duration = sounds[sound_type]
                self.winsound.Beep(freq, duration)
        except Exception as e:
            # Silenciosamente ignorar errores de sonido
            pass

    def setup_controls(self):
        """Crea los botones de control para generar y resolver el laberinto."""
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10)

        button_style = {"width": 120, "height": 32, "corner_radius": 6}

        difficulty_selector = ctk.CTkSegmentedButton(
            frame,
            values=["Fácil", "Intermedio", "Difícil"],
            command=self.change_difficulty,
            width=360,
            selected_color="gray"
        )
        difficulty_selector.set("Fácil")
        difficulty_selector.grid(row=0, column=0, columnspan=3, padx=8, pady=5)

        # FILA 2: Botones de juego
        btn_new = ctk.CTkButton(
            frame, text="Nuevo Laberinto",
            command=self.start_play,
            **button_style
        )
        btn_new.grid(row=1, column=0, padx=8, pady=(10, 5))

        btn_solve = ctk.CTkButton(
            frame, text="Ver Solución",
            command=self.controller.solve_maze,
            **button_style
        )
        btn_solve.grid(row=1, column=1, padx=8, pady=(10, 5))

        btn_reset = ctk.CTkButton(
            frame, text="Reiniciar",
            command=self.reset_manual_mode,
            **button_style
        )
        btn_reset.grid(row=1, column=2, padx=8, pady=(10, 5))

    def change_difficulty(self, value):
        """Cambia la dificultad seleccionada."""
        self.current_difficulty = value
        config = self.difficulties[value]
        width, height = config["size"]
        self.canvas.delete("all")
        self.resize_canvas(width, height)

        self.update_info(f"Tamaño: {width}x{height}")

    def resize_canvas(self, width, height):
        """Redimensiona el canvas según el tamaño del laberinto."""
        canvas_width = width * self.cell_size + self.margin * 2
        canvas_height = height * self.cell_size + self.margin * 2

        # Redimensionar canvas
        self.canvas.configure(width=canvas_width, height=canvas_height)

        # Ajustar tamaño de ventana centrada
        window_width = canvas_width + 30
        window_height = canvas_height + 145

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) * 0.25)

        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def start_play(self):
        """Inicia el juego con la dificultad seleccionada."""
        config = self.difficulties[self.current_difficulty]
        width, height = config["size"]
        passages_ratio = config["passages"]

        # Ajustar canvas antes de generar
        self.resize_canvas(width, height)

        self.controller.generate_maze(width, height, passages_ratio)
        self.start_manual_mode()

    def update_info(self, text):
        """Actualiza el label de información."""
        self.info_label.configure(text=text)

    def draw_maze(self, graph):
        """Dibuja el laberinto ajustándose al tamaño del canvas."""
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

        # Dibujar apertura de salida
        if graph.exit:
            self.draw_opening(graph.exit, graph.width, graph.height)

        # Dibujar flecha de salida
        self._draw_exit_arrow(graph)

    def draw_opening(self, node, width, height):
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

    def _draw_exit_arrow(self, graph):
        """Dibuja la flecha de salida en el borde."""
        if graph.exit:
            sx, sy = graph.exit
            sy_center = sy * self.cell_size + self.margin + self.cell_size // 2
            x_start = sx * self.cell_size + self.margin + self.cell_size - 5
            x_end = sx * self.cell_size + self.margin + self.cell_size + 10
            self.canvas.create_line(x_start, sy_center, x_end, sy_center, fill="red", width=3, arrow="last")

    def draw_path_animated(self, path, delay, color="#057032"):
        """Dibuja el camino como una línea animada que crece paso a paso."""
        self.draw_player()

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

            if index == 1:
                # Calcular el punto medio entre el nodo 0 y el nodo 1
                x1 = (x1 + x2) / 2
                y1 = (y1 + y2) / 2

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

        self.player_position = self.controller.graph.entry
        self.manual_path = [self.player_position]

        self.draw_maze(self.controller.graph)
        self.draw_player()

        self.update_info(
            "Reiniciado | Usa las flechas del teclado para moverte"
        )

    def move_player(self, dx, dy):
        """Mueve al jugador en la dirección especificada con animación fluida."""
        if not self.manual_mode or not self.player_position:
            return

        current = self.player_position
        new_position = (current[0] + dx, current[1] + dy)

        # Verificar si el movimiento es válido
        neighbors = self.controller.graph.neighbors(current)
        if new_position not in neighbors:
            # Movimiento inválido
            self.play_sound('wall')
            canvas_width = self.controller.graph.width * self.cell_size + self.margin * 2
            canvas_height = self.controller.graph.height * self.cell_size + self.margin * 2
            self.canvas.create_rectangle(
                0, 0, canvas_width, canvas_height,
                fill="", outline="#FF0000", width=5, tags="invalid"
            )
            self.root.after(100, lambda: self.canvas.delete("invalid"))
            return

        # Movimiento válido
        self.play_sound('move')

        # Animar el movimiento
        steps = 200  # número de frames en la animación
        x0, y0 = current[0] * self.cell_size, current[1] * self.cell_size
        x1, y1 = new_position[0] * self.cell_size, new_position[1] * self.cell_size

        dx_step = (x1 - x0) / steps
        dy_step = (y1 - y0) / steps

        player_item = getattr(self, "player_item", None)

        if player_item is None:
            # Si aún no hay representación del jugador, dibujarla
            player_item = self.canvas.create_oval(
                x0 + self.margin + 5, y0 + self.margin + 5,
                x0 + self.cell_size - 5, y0 + self.cell_size - 5,
                fill="blue", outline=""
            )

        def animate(step=0):
            if step < steps:
                self.canvas.move(player_item, dx_step, dy_step)
                self.root.after(0, lambda: animate(step + 1))
            else:
                # Al final, actualizar la posición y el camino
                self.player_position = new_position
                self.manual_path.append(new_position)

                self.draw_maze(self.controller.graph)
                self.draw_manual_path()
                self.draw_player()

                # Verificar si llegó a la salida
                if self.player_position == self.controller.graph.exit:
                    self.play_sound('victory')
                    messagebox.showinfo("¡Felicitaciones!", "¡Completaste el laberinto!")
                    self.update_info(f"Completado en {len(self.manual_path) - 1} movimientos")
                    self.manual_mode = False
                else:
                    self.update_info(f"Movimientos: {len(self.manual_path) - 1}")

        animate()

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
        """Dibuja el camino recorrido por el jugador (sin diagonales)."""
        if len(self.manual_path) < 2:
            return

        # Elimina cualquier trazo previo del camino
        self.canvas.delete("manual_path")

        for i in range(1, len(self.manual_path)):
            x1, y1 = self.manual_path[i - 1]
            x2, y2 = self.manual_path[i]

            # Evitar diagonales: solo dibujar si cambia una sola coordenada
            if (x1 != x2) and (y1 != y2):
                continue  # ignorar movimiento diagonal

            x1 = x1 * self.cell_size + self.margin + self.cell_size // 2
            y1 = y1 * self.cell_size + self.margin + self.cell_size // 2
            x2 = x2 * self.cell_size + self.margin + self.cell_size // 2
            y2 = y2 * self.cell_size + self.margin + self.cell_size // 2

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="#4CAF50", width=4, tags="manual_path"
            )

