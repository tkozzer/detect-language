import tkinter as tk

from validate import Validator as v

class AddLanguage(tk.Toplevel):

    def __init__(self, parent, **kwargs):
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
        self.language = self.parent.language.output_keyboard[-1]

            
        self.create_widgets()
        self.bindings()

        


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
        self.geometry(f'{self.win_width}x{self.win_height + 100}+{x_pos}+{y_pos + self.win_height - 10}')

    def right_click(self, event):
        self.parent.right_click(event)

    def create_widgets(self):
        self.current_lang_label = tk.Label(self, fg='white', bg='black', text=self.language)
        self.lang_label = tk.Label(self,fg='white', bg='black', text="Enter Language: ")
        self.lang_entry = tk.Entry(self, bg="white", fg='black')
        self.primary_color_label = tk.Label(self, fg='white', bg='black', text="Enter primary color: ")
        self.primary_color_entry = tk.Entry(self, bg="white", fg='black')
        self.secondary_color_label = tk.Label(self, fg='white', bg='black', text="Enter secondary color: ")
        self.secondary_color_entry = tk.Entry(self, bg="white", fg='black')
        self.current_lang_label.pack(pady=5)
        self.lang_label.pack()
        self.lang_entry.pack()
        self.primary_color_label.pack()
        self.primary_color_entry.pack()
        self.secondary_color_label.pack()
        self.secondary_color_entry.pack()
        self.lang_entry.focus()

    def bindings(self):
        ENTER_KEY = '<Return>'
        self.lang_entry.bind(ENTER_KEY, self.lang_entry_bind)
        self.primary_color_entry.bind(ENTER_KEY, self.primary_color_entry_bind)
        self.secondary_color_entry.bind(ENTER_KEY, self.secondary_color_entry_bind)
    
    def lang_entry_bind(self,event):
        print("lang_entry_bind: ", event)
        validated = False
        while not validated:
            try:
                validated = v.validate_entry_input(self.lang_entry.get(), type="lang")
                self.primary_color_entry.focus()
            except ValueError as ve:
                # print(ve)
                self.lang_entry.delete(0, 'end')
                break
        

    def primary_color_entry_bind(self,event):
        print("primary_color_entry_bind: ", event)
        validated = False
        while not validated:
            try:
                validated = v.validate_entry_input(self.primary_color_entry.get(), type="color")
            except ValueError as ve:
                pass
        self.secondary_color_entry.focus()
    
    def secondary_color_entry_bind(self,event):
        print("secondary_color_entry_bind: ", event)
        validated = False
        while not validated:
            try:
                validated = v.validate_entry_input(self.secondary_color_entry.get(), type="color")
            except ValueError as ve:
                pass
        self.parent.double_click_id = self.parent.bind('<Double-Button-1>', self.parent.increase_size)
        self.destroy()