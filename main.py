import tkinter as tk
import json
from windows.GameWindow import GameWindow
from windows.SettingsWindow import SettingsWindow


class App(tk.Tk):

    SCREEN_HEIGHT_MENU_OFFSET = 34
    SCREEN_WIDTH_MENU_OFFSET = 4

    MIN_GRID_WIDTH = 2
    MIN_GRID_HEIGHT = 2
    MAX_GRID_WIDTH = 200
    MAX_GRID_HEIGHT = 200

    MIN_RANDOM = 1
    MAX_RANDOM = 100

    MIN_DELAY = 100
    MAX_DELAY = 3000

    BACKGROUND_COLOR = "#232323"
    PRIME_COLOR = "#fb0"
    PRIME_2_COLOR = "#ffe300"
    SEC_COLOR = "#004fff"

    PAGES = (GameWindow, SettingsWindow)

    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # System Settings
        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 600

        with open('settings.json') as f:
            settings = json.load(f)
        self.SCREEN_WIDTH = settings['screen']['width']
        self.SCREEN_HEIGHT = settings['screen']['height']

        self.grid_width = 20
        self.grid_height = 20

        self.tile_width = self.SCREEN_WIDTH / self.grid_width
        self.tile_height = self.SCREEN_HEIGHT / self.grid_height

        self.random_level = 100
        self.delay = 250

        self.title("Game Of Life")
        self.iconbitmap('resources/icons/gof.ico')
        self.minsize(width=(self.SCREEN_WIDTH + self.SCREEN_WIDTH_MENU_OFFSET),
                     height=(self.SCREEN_HEIGHT + self.SCREEN_HEIGHT_MENU_OFFSET))
        self.config(bg=self.BACKGROUND_COLOR)

        # Creating a container
        container = tk.Frame(self, width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.page_frames = {

        }

        for F in self.PAGES:
            frame = F(container, self)
            self.page_frames[F.name()] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("GameWindow")

    def show_frame(self, cont):
        frame = self.page_frames[cont]
        frame.tkraise()


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
