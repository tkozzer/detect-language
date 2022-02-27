import tkinter as tk

class AddLanguage(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.overrideredirect(1)
        self.overrideredirect(0)
        self.attributes('-topmost', 'true')
        self.attributes('-transparent', True)
        self.config(background=self.parent.current_lang[1]['bg'])
        self.file = "config.json"

        self.bind('<B1-Motion>', self.dragwin)
        self.bind('<Button-1>', self.clickwin)
        self.bind('<Button-2>', self.right_click)

        self.setup()



    # These two methods are the brains behind dragging a menuless window
    def dragwin(self, event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety - 100
        self.parent.geometry(f'+{x}+{y}')
        self.geometry(f'+{x}+{y + self.win_height - 10}')


    def clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def setup(self):
        self.win_width = self.parent.win_width
        self.win_height = self.parent.win_height
        x_pos = self.parent.winfo_rootx()
        y_pos = self.parent.winfo_rooty()
        self.geometry(f'{self.win_width}x{self.win_height}+{x_pos}+{y_pos + self.win_height - 10}')

    def right_click(self, event):
        self.parent.right_click(event)