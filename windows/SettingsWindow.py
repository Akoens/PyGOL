import tkinter as tk

from windows.Window import Window
from windows.Pages import Pages


class SettingsWindow(Window):
    """
    The SettingsWindow allows the user to edit different settings of the game and the UI.
    """

    SPACER_HEIGHT = 20

    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller

        self.settings_frame = None

        self.grid_height_scale = None
        self.grid_width_scale = None
        self.random_level_scale = None
        self.delay_scale = None

        self.button_frame = None
        self.return_button = None

        self.setup()

    def setup(self) -> None:
        """
        Define the different widgets for the settings page.
        :return: None
        """

        # Settings
        self.settings_frame = tk.Frame(master=self, bg=self.controller.BACKGROUND_COLOR, padx=20, pady=20)

        # Height
        self.grid_height_scale = tk.Scale(
            master=self.settings_frame,
            tickinterval=10,
            length=700,
            from_=2,
            to=self.controller.MAX_GRID_HEIGHT,
            orient=tk.HORIZONTAL,
            highlightthickness=0,
            bg=self.controller.PRIME_COLOR,
            troughcolor=self.controller.PRIME_2_COLOR,
            bd=0,
            relief='ridge',
            label='Grid height')
        self.grid_height_scale.set(self.controller.grid_height)
        self.grid_height_scale.pack()

        # Spacer
        tk.LabelFrame(master=self.settings_frame, height=self.SPACER_HEIGHT, bg=self.controller.BACKGROUND_COLOR).pack()

        # Width
        self.grid_width_scale = tk.Scale(
            master=self.settings_frame,
            tickinterval=10,
            length=700,
            from_=2,
            to=self.controller.MAX_GRID_WIDTH,
            orient=tk.HORIZONTAL,
            highlightthickness=0,
            bg=self.controller.PRIME_COLOR,
            troughcolor=self.controller.PRIME_2_COLOR,
            bd=0,
            relief='ridge',
            label='Grid width')
        self.grid_width_scale.set(self.controller.grid_width)
        self.grid_width_scale.pack()

        # Spacer
        tk.LabelFrame(master=self.settings_frame, height=self.SPACER_HEIGHT, bg=self.controller.BACKGROUND_COLOR).pack()

        # Randomness
        self.random_level_scale = tk.Scale(
            master=self.settings_frame,
            tickinterval=10,
            length=700,
            from_=self.controller.MIN_RANDOM,
            to=self.controller.MAX_RANDOM,
            orient=tk.HORIZONTAL,
            highlightthickness=0,
            bg=self.controller.PRIME_COLOR,
            troughcolor=self.controller.PRIME_2_COLOR,
            bd=0,
            relief='ridge',
            label='Random level (1/x)'
        )
        self.random_level_scale.set(self.controller.random_level)
        self.random_level_scale.pack()

        # Spacer
        tk.LabelFrame(master=self.settings_frame, height=self.SPACER_HEIGHT, bg=self.controller.BACKGROUND_COLOR).pack()

        # Delay
        self.delay_scale = tk.Scale(
            master=self.settings_frame,
            tickinterval=500,
            length=700,
            from_=self.controller.MIN_DELAY,
            to=self.controller.MAX_DELAY, resolution=100,
            orient=tk.HORIZONTAL,
            highlightthickness=0,
            bg=self.controller.PRIME_COLOR,
            troughcolor=self.controller.PRIME_2_COLOR,
            bd=0,
            relief='ridge',
            label='Update delay (ms)')
        self.delay_scale.set(self.controller.delay)
        self.delay_scale.pack()

        # Show frame
        self.settings_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Menu Buttons
        self.button_frame = tk.Frame(master=self, bg=self.controller.BACKGROUND_COLOR)
        self.return_button = tk.Button(
            self.button_frame,
            text="Back",
            padx=10, pady=5,
            fg="black",
            relief="flat",
            bg=self.controller.PRIME_COLOR,
            command=self.back)
        self.return_button.pack(side=tk.RIGHT)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def apply(self) -> None:
        """
        Apply the settings that have been altered.
        :return: None
        """
        height = self.grid_height_scale.get()
        width = self.grid_width_scale.get()

        self.controller.grid_height = height
        self.controller.grid_width = width

        self.controller.tile_height = self.controller.SCREEN_HEIGHT / self.controller.grid_height
        self.controller.tile_width = self.controller.SCREEN_WIDTH / self.controller.grid_width

        self.controller.random_level = self.random_level_scale.get()
        self.controller.delay = self.delay_scale.get()

        self.controller.page_frames.get(Pages.GameWindow).update()

    def back(self) -> None:
        self.apply()
        self.controller.show_page(Pages.GameWindow)

    def name(self) -> Pages:
        return Pages.SettingsWindow
