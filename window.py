import tkinter as tk
import tkinter
import detect_keyboard_lang as dkl

class Win(tkinter.Tk):

    def __init__(self, master=None):
        # Create draggable always on top window that has one label that is dynamic based on
        # which keyboard language is detected. Only languages accepted are "English" and "Chinese"
        tk.Tk.__init__(self, master)
        self.overrideredirect(True)
        self.overrideredirect(False)
        self.attributes('-topmost', 'true')
        self._offsetx = 0
        self._offsety = 0
        self.bind('<Button-1>', self.clickwin)
        self.bind('<B1-Motion>', self.dragwin)
        self.label = tk.Label(self, bg='red', width=10, padx=5, fg='white')
        self.label.pack()
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
        language = dkl.detect_keyboard_language()
        self.label.config(text=language["lang"],fg=language["fg"], bg=language["bg"])
        self.after(100, self.show_language)
        


win = Win()
win.mainloop()