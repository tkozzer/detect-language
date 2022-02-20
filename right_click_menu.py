import tkinter as tk
import sys
import traceback
import config

class RightClick(tk.Frame):

    def __init__(self, win, event, **kwargs) -> None:
        self.kwargs = kwargs
        self.win = win
        self.right_click_menu = tk.Menu(self.win)
        self.right_click_menu.add_command(label="About Detect Language", command=self.about)
        self.right_click_menu.add_command(label="Check for Updates", command=self.check_updates)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label="Customize...", command=self.customize)
        self.right_click_menu.add_command(label="Set Position", command=self.set_position)
        self.right_click_menu.add_command(label="Quit", command=self.exit)

        self.popup(event)

    def popup(self, event):
        try:
            self.right_click_menu.post(event.x_root, event.y_root)
        finally:
            # TODO figure out what grab_release() does
            # self.right_click_menu.grab_release()
            pass

    def about(self):
        pass

    def check_updates(self):
        pass

    def customize(self):
        pass

    def set_position(self):
        try:
            self.file = self.kwargs['file']            
            print("From right click menu set position")
            self.config = config.get_config(self.file)
            print(self.config)
        except Exception:
            traceback.print_exc()
            print(f"There seems to be an error.")

    def exit(self):
        try:
            self.win.destroy()
        except SystemExit:
            sys.exit()
