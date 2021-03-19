import tkinter as tk
import windows.Window as Window
import time
import random
import math


class GameWindow(Window.Window):
    def __init__(self, master, controller):
        super().__init__(master=master)
        self.master = master
        self.controller = controller

        # Extra variables
        self._job = None
        self.dirs = [(0, -1), (-1, 0), (0, 1), (1, 0), (1, -1), (-1, 1), (1, 1), (-1, -1)]
        self.cells = {}

        # windows / Frames
        self.canvas = None
        self.button_frame = None

        # Buttons
        self.step_button = None
        self.auto_step_button = None
        self.random_fill_button = None
        self.clear_button = None
        self.settings_button = None

        self.setup()

    def setup(self):

        self.config(bg=self.controller.BACKGROUND_COLOR)

        self.canvas = tk.Canvas(master=self, bg="#333", width=self.controller.SCREEN_WIDTH,
                                height=self.controller.SCREEN_HEIGHT,
                                bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.callback)

        # Button Menu
        self.button_frame = tk.Frame(master=self, width=self.controller.SCREEN_WIDTH,
                                     bg=self.controller.BACKGROUND_COLOR)

        self.step_button = tk.Button(self.button_frame, text="Step", padx=10, pady=5, fg="black", relief="flat",
                                     bg=self.controller.PRIME_COLOR, command=self.step)
        self.step_button.pack(side=tk.LEFT)

        self.auto_step_button = tk.Button(self.button_frame, text="Start", padx=10, pady=5, fg="black", relief="flat",
                                          bg=self.controller.PRIME_COLOR, command=self.start)
        self.auto_step_button.pack(side=tk.LEFT)

        self.random_fill_button = tk.Button(self.button_frame, text="Random Fill", padx=10, pady=5, fg="black",
                                            relief="flat",
                                            bg=self.controller.PRIME_COLOR, command=self.random)
        self.random_fill_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.button_frame, text="Clear", padx=10, pady=5, fg="black", relief="flat",
                                      bg=self.controller.PRIME_COLOR, command=self.clear)
        self.clear_button.pack(side=tk.LEFT)

        self.settings_button = tk.Button(self.button_frame, text="Settings", padx=10, pady=5, fg="black", relief="flat",
                                         bg=self.controller.PRIME_COLOR,
                                         command=self.settings)
        self.settings_button.pack(side=tk.RIGHT)
        self.button_frame.pack(fill=tk.BOTH)

        self.update()

    def create_grid(self):
        start_width = self.controller.tile_width
        for idxC in range(self.controller.grid_width-1):
            self.canvas.create_line(start_width, 0, start_width, self.controller.SCREEN_HEIGHT,
                                    fill="#000", width=1)
            start_width += self.controller.tile_width

        start_height = self.controller.tile_height
        for idxR in range(self.controller.grid_height-1):
            self.canvas.create_line(0, start_height, self.controller.SCREEN_WIDTH, start_height,
                                    fill="#000", width=1)
            start_height += self.controller.tile_height

    def random(self):
        for r in range(self.controller.grid_width - 1):
            for c in range(self.controller.grid_height - 1):
                ri = random.randint(0, self.controller.random_level)
                if ri == (self.controller.random_level / 2) and self.cells.get((c, r), None) is None:
                    self.cells.update({(c, r): 1})
        self.update()

    def clear(self):
        self.cells.clear()
        self.update()

    def settings(self):
        self.stop()
        self.controller.show_frame("SettingsWindow")

    def update(self):
        self.canvas.delete('all')
        self.create_grid()

        for cell in self.cells.keys():
            tile_start_width = cell[1] * self.controller.tile_width
            tile_start_height = cell[0] * self.controller.tile_height
            self.canvas.create_rectangle(tile_start_width, tile_start_height, tile_start_width + self.controller.tile_width,
                                         tile_start_height + self.controller.tile_height, outline="#000",
                                         fill=self.controller.PRIME_COLOR, width=1)

    def step(self):
        if len(self.cells) <= 0:
            return
        start = time.perf_counter()
        neighbours = {}
        deaths = []
        for cell in self.cells.keys():
            non = 0
            for d in self.dirs:
                nc = cell[0] + d[0]
                nr = cell[1] + d[1]

                if self.cells.get((nc, nr), None) is not None:
                    non += 1
                if neighbours.get((nc, nr), None) is not None:
                    neighbours[(nc, nr)] += 1
                else:
                    neighbours.update({(nc, nr): 1})
            if (non < 2 or non > 3) or \
                    (0 > cell[0] >= self.controller.grid_height and 0 > cell[1] >= self.controller.grid_width):
                deaths.append(cell)

        for neighbour in neighbours.keys():
            if neighbours[neighbour] == 3 and (
                    0 <= neighbour[0] < self.controller.grid_height and 0 <= neighbour[1] < self.controller.grid_width):
                self.cells[neighbour] = 1

        for death in deaths:
            if self.cells.get(death, None) is not None:
                self.cells.pop(death)

        bfu = time.perf_counter()
        self.update()
        end = time.perf_counter()
        print(f'Finished in {round(end - start, 9)} second(s).\n'
              f'; Before Update {round(bfu - start, 9)} second(s).', end="\n\n")

    def auto_step(self):
        self.step()
        self._job = self.after(self.controller.delay, self.auto_step)

    def start(self):
        self.auto_step()
        self.auto_step_button.configure(text="Stop", command=self.stop)
        self.step_button.configure(state="disabled")

    def cancel(self):
        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None

    def stop(self):
        self.cancel()
        self.auto_step_button.configure(text="Start", command=self.start)
        self.step_button.configure(state="normal")

    def callback(self, event):
        print(f"Clicked at: x{event.x}, y{event.y}")
        ylo = math.floor(event.x / self.controller.tile_width)
        xlo = math.floor(event.y / self.controller.tile_height)
        cell = self.cells.get((xlo, ylo), None)
        if cell is not None:
            self.cells.pop((xlo, ylo))
        elif cell is None:
            self.cells.update({(xlo, ylo): 1})
        self.update()

    @staticmethod
    def name():
        return "GameWindow"
