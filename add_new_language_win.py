import tkinter as tk

class AddLanguage(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.overrideredirect(1)
        self.overrideredirect(0)
        self.attributes('-topmost', 'true')
        self.attributes('-transparent', True)
        self.config(background='white')
        self.file = "config.json"

        self.bind('<B1-Motion>', self.dragwin)
        self.bind('<Button-1>', self.clickwin)



    # These two methods are the brains behind dragging a menuless window
    def dragwin(self, event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry(f'+{x}+{y}')

    def clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y