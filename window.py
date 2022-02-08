import tkinter as tk
import tkinter
import math
from detect_keyboard_lang import Language

class Win(tkinter.Tk):

    def __init__(self, master=None):
        # Create draggable always on top window that has one label that is dynamic based on
        # which keyboard language is detected.
        tk.Tk.__init__(self, master)
        self.overrideredirect(True)
        self.overrideredirect(False)
        self.attributes('-topmost', 'true')
        self.click_count = 0
        self.width = 10
        self.height = 2
        self.font_type = "Helvetica"
        self.font_size = 15
        self._offsetx = 0
        self._offsety = 0

        self.language = Language()
        self.label = tk.Label(self, width=self.width, height=self.height, padx=5, relief='ridge', borderwidth=2, font=(self.font_type, self.font_size))
        self.bind('<B1-Motion>', self.dragwin)
        self.bind('<Button-1>', self.clickwin)
        self.bind('<Double-Button-1>', lambda e:self.increase_size())
        # TODO add tooltip so users know to double click the X to quit
        self.label_x = tk.Label(self, text="X", height=self.height, relief='ridge', borderwidth=2, font=(self.font_type, self.font_size))
        self.label_x.bind("<Double-Button-1>", lambda e:self.exit())
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
        self.label.config(text=self.current_lang[1]["language"],fg=self.current_lang[1]["fg"], bg=self.current_lang[1]["bg"], width=self.width)
        self.config(bg=self.current_lang[1]["bg"])
        self.label_x.config(fg=self.current_lang[1]["fg"], bg=self.current_lang[1]["bg"])
        self.after(100, self.show_language)
    
    def increase_size(self):
        #TODO after the user double clicks the widgit it will increase in size including height, width, and font size
        self.click_count += 1
        if(self.click_count == 3):
            self.width = 10
            self.height = 2
            self.font_size = 15
            self.click_count = 0
        else:
            self.width = math.floor(self.width * 1.50)
            self.height = math.floor(self.height * 1.50)
            self.font_size = math.floor(self.font_size * 2)
        self.label.config(height=self.height, width=self.width, font=(self.font_type, self.font_size))
        self.label_x.config(height=self.height, font=(self.font_type, self.font_size))


    def exit(self):
        self.destroy()


