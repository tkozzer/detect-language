import tkinter as tk

class RightClick(tk.Frame):

    def __init__(self, win, event) -> None:
        self.win = win
        self.right_click_menu = tk.Menu(self.win)
        self.right_click_menu.add_command(label="About Detect Language", command=self.about)
        self.right_click_menu.add_command(label="Check for Updates", command=self.check_updates)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label="Customize...", command=self.customize)

        self.popup(event)

    def popup(self, event):
        try:
            self.right_click_menu.post(event.x_root, event.y_root)
        finally:
            self.right_click_menu.grab_release()

    def about(self):
        pass

    def check_updates(self):
        pass

    def customize(self):
        pass

