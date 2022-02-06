import tkinter as tk
import tkinter
from turtle import left, width
from detect_keyboard_lang import Language

class Win(tkinter.Tk):

    def __init__(self, master=None):
        # Create draggable always on top window that has one label that is dynamic based on
        # which keyboard language is detected.
        tk.Tk.__init__(self, master)
        self.overrideredirect(True)
        self.overrideredirect(False)
        self.width = 10
        self.attributes('-topmost', 'true')
        self._offsetx = 0
        self._offsety = 0

        self.language = Language()
        self.label = tk.Label(self, width=self.width, padx=5)
        self.bind('<B1-Motion>', self.dragwin)
        self.bind('<Button-1>', self.clickwin)
        # TODO add tooltip so users know to double click the X to quit
        self.label_x = tk.Label(self, text="X")
        self.label_x.bind("<Double-Button-1>", lambda e:self.destroy())
        self.label.pack(side="right")
        self.label_x.pack(side="left")
        self.show_language()


    # These two methods are the brains behind dragging a menuless window
    def dragwin(self, event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x, y=y))

    def clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    # The will import in detect_keyboard_lang and check which language is used and print it to the window
    def show_language(self):
        self.current_lang = self.language.get_current_language()
        if self.current_lang[0] == 'not_supported':
            self.width = 20
        else:
            self.width = 10
        self.label.config(text=self.current_lang[1]["language"],fg=self.current_lang[1]["fg"], bg=self.current_lang[1]["bg"], width=self.width)
        self.label_x.config(fg=self.current_lang[1]["fg"], bg=self.current_lang[1]["bg"])
        self.after(100, self.show_language)
    
    def exit(self):
        self.after_cancel()
        self.destroy()


