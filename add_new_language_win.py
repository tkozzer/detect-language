import tkinter as tk

from validate import Validator as v
from tkinter import font, colorchooser

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
        self.x_pos = self.parent.winfo_rootx()
        self.y_pos = self.parent.winfo_rooty()
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Helvetica", size=20)
        self.geometry(f'{self.win_width}x{self.win_height}+{self.x_pos}+{self.y_pos + self.win_height - 10}')

    def right_click(self, event):
        self.parent.right_click(event)

    def create_widgets(self):
        self.current_lang_label = tk.Label(self, fg='white', bg='black', text=f"Current Language:\n{self.language}")
        self.seperator1 = tk.Frame(self, bg='white', height=1, bd=0)
        self.seperator2 = tk.Frame(self, bg='white', height=1, bd=0)
        self.lang_label = tk.Label(self,fg='white', bg='black', text="Enter Language: ")
        self.lang_entry = tk.Entry(self, bg="white", fg='black')
        self.primary_color_label = tk.Label(self, fg='white', bg='black', text="Enter primary color: ")
        self.primary_color_entry = tk.Entry(self, bg="white", fg='black')
        self.secondary_color_label = tk.Label(self, fg='white', bg='black', text="Enter secondary color: ")
        self.secondary_color_entry = tk.Entry(self, bg="white", fg='black')
        self.color_button = tk.Button(self, text="Pick a color", width=10, command=self.choose_color, font=10)
        self.seperator1.pack(fill='x', pady=(5,5))
        self.current_lang_label.pack(pady=5)
        self.seperator2.pack(fill='x', pady=(5,5))
        self.lang_label.pack()
        self.lang_entry.pack()
        self.lang_entry.insert(0, self.language)
        self.lang_entry.focus()
        self.update_geometry_height(40)

    def bindings(self):
        ENTER_KEY = '<Return>'
        self.lang_entry.bind(ENTER_KEY, self.lang_entry_bind)
        self.primary_color_entry.bind(ENTER_KEY, self.primary_color_entry_bind)
        self.secondary_color_entry.bind(ENTER_KEY, self.secondary_color_entry_bind)

        self.bind('<B1-Motion>', self.dragwin)
        self.bind('<Button-1>', self.clickwin)
        self.bind('<Button-2>', self.right_click)
    
    def lang_entry_bind(self,event):
        try:
            v.validate_entry_input(self.lang_entry.get(), type="lang")
            self.primary_color_entry.focus()
            self.lang_label.config(text=f'{self.lang_entry.get()}', pady=5)
            self.lang_entry.destroy()
            self.primary_color_label.pack()
            self.primary_color_entry.pack()
            self.color_button.pack(pady=(5,5))
            self.update_geometry_height(110)
        except ValueError as ve:
            print(ve)
            self.lang_entry.delete(0, 'end')
            self.lang_entry.focus()
                

    def primary_color_entry_bind(self,event):
        try:
            v.validate_entry_input(self.primary_color_entry.get(), type="color")
            self.secondary_color_entry.focus()
            self.primary_color_label.config(text=f'{self.primary_color_entry.get()}', pady=5)
            self.primary_color_entry.destroy()
            self.color_button.pack_forget()
            self.secondary_color_label.pack()
            self.secondary_color_entry.pack()
            self.color_button.pack(pady=(5,5))
            self.update_geometry_height(150)
        except ValueError as ve:
            print(ve)
            self.primary_color_entry.delete(0, 'end')
            self.primary_color_entry.focus()
        
    def secondary_color_entry_bind(self,event):
        try:
            v.validate_entry_input(self.secondary_color_entry.get(), type="color")
            # This will add the increase/decrease binding back on
            self.parent.double_click_id = self.parent.bind('<Double-Button-1>', self.parent.increase_size)
            self.secondary_color_label.config(text=f'{self.secondary_color_entry.get()}')
            self.secondary_color_entry.destroy()
            self.color_button.pack_forget()
            self.submit_btn = tk.Button(self, text="Submit", command=self.submit_by_click, width=10, font=10)
            self.submit_btn.pack(side=tk.LEFT, padx=(50, 20))
            self.edit_btn = tk.Button(self, text="Edit", command=self.edit, width=10, font=10)
            self.edit_btn.pack(side=tk.LEFT)
            self.bind('<Return>', self.submit)
            self.update_geometry_height(150)
        except ValueError as ve:
            print(ve)
            self.secondary_color_entry.delete(0, 'end')
            self.secondary_color_entry.focus()

    def choose_color(self):
        self.color_code = colorchooser.askcolor(title="Choose color")
        if self.primary_color_entry.winfo_exists() and self.primary_color_entry.winfo_ismapped():
            self.primary_color_entry.delete(0, 'end')
            self.primary_color_entry.insert(0, self.color_code[1])
            self.primary_color_entry.focus()
        if self.secondary_color_entry.winfo_exists() and self.secondary_color_entry.winfo_ismapped():
            self.secondary_color_entry.delete(0, 'end')
            self.secondary_color_entry.insert(0, self.color_code[1])
            self.secondary_color_entry.focus()

        
    def update_geometry_height(self, x):
        self.geometry(f'{self.win_width}x{self.win_height + x}')

    def submit(self, event):
        self.save_input()
        # TODO need to save the user's input in the config file
    
    def submit_by_click(self):
        self.save_input()

    def save_input(self):
        print("save_input")

    def edit(self):
        print("edit")

