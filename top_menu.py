import tkinter as tk

class TopMenu(tk.Frame):

    def __init__(self, win) -> None:
        self.win = win
        self.menubar = tk.Menu(self.win)
        self.app_menu = tk.Menu(self.menubar, name="apple")
        self.menubar.add_cascade(menu=self.app_menu)
        self.app_menu.add_command(label="About Detect Language")
        self.app_menu.add_separator()
        self.win['menu'] = self.menubar

"""
TODO Add more functionality to the menu
"""