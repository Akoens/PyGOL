import tkinter as tk
from abc import abstractmethod, ABC

from windows.Pages import Pages


class Window(tk.Frame, ABC):
    """
    Abstract class for making windows in the app.
    """

    @abstractmethod
    def name(self) -> Pages:
        ...
