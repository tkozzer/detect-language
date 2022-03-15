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
        # self.file = "json/config.json"

        self.setup()
        self.language = self.parent.language.output_keyboard[-1]
            
        self.create_widgets()
        self.bindings()

    # These two methods are the brains behind dragging a menuless window
    def dragwin(self, event):
        self.x = self.winfo_pointerx() - self._offsetx
        self.y = self.winfo_pointery() - self._offsety - 100
        self.parent.geometry(f'+{x}+{y}')
        self.geometry(f'+{x}+{y + self.parent.win_height}')

    def clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def setup(self):
        self.win_width = self.parent.win_width
        self.win_height = self.parent.win_height - 5
        self.x_pos = self.parent.winfo_rootx()
        self.y_pos = self.parent.winfo_rooty()
        self.x = self.x_pos
        self.y = self.y_pos
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Helvetica", size=20)
        self.geometry(f'{self.win_width}x{self.win_height}+{self.x_pos}+{self.y_pos + self.win_height}')

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
        self.color_btn = tk.Button(self, text="Pick a color", width=10, command=self.choose_color, font=10)
        self.next_btn = tk.Button(self, text="Next", width=9, command=self.next_btn_command, font=10)
        self.seperator1.pack(fill='x', pady=(10,5))
        self.current_lang_label.pack(pady=5)
        self.seperator2.pack(fill='x', pady=(5,5))
        self.lang_label.pack()
        self.lang_entry.pack()
        self.lang_entry.insert(0, self.language)
        self.lang_entry.focus()
        self.next_btn.pack(pady=12)
        self.update_geometry_height(80)
        self.move_window_up(self.win_height)

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
            self.next_btn.pack_forget()
            self.primary_color_label.pack()
            self.primary_color_entry.pack()
            self.color_btn.pack(pady=(5,5), padx=(55, 1), side=tk.LEFT)
            self.next_btn.pack(padx=(10,10), side=tk.LEFT)
            self.update_geometry_height(40)
            self.move_window_up(self.win_height)
        except ValueError as ve:
            print(ve)
            self.lang_entry.delete(0, 'end')
            self.lang_entry.focus()             

    def primary_color_entry_bind(self,event):
        try:
            v.validate_entry_input(self.primary_color_entry.get(), type="color")
            self.secondary_color_entry.focus()
            self.primary_color_label.config(text=f'{self.primary_color_entry.get()}', pady=5, fg=self.primary_color_entry.get())
            self.primary_color_entry.destroy()
            self.color_btn.pack_forget()
            self.next_btn.pack_forget()
            self.secondary_color_label.pack()
            self.secondary_color_entry.pack()
            self.color_btn.pack(pady=(5,5), padx=(55, 1), side=tk.LEFT)
            self.next_btn.pack(padx=(10,10), side=tk.LEFT)
            self.update_geometry_height(40)
            self.move_window_up(self.win_height)
        except ValueError as ve:
            print(ve)
            self.primary_color_entry.delete(0, 'end')
            self.primary_color_entry.focus()
        
    def secondary_color_entry_bind(self,event):
        try:
            v.validate_entry_input(self.secondary_color_entry.get(), type="color")
            # This will add the increase/decrease binding back on
            self.parent.double_click_id = self.parent.bind('<Double-Button-1>', self.parent.increase_size)
            self.secondary_color_label.config(text=f'{self.secondary_color_entry.get()}', fg=self.secondary_color_entry.get())
            self.secondary_color_entry.destroy()
            self.color_btn.pack_forget()
            self.next_btn.pack_forget()
            self.submit_btn = tk.Button(self, text="Submit", command=self.submit_by_click, width=10, font=10)
            self.submit_btn.pack(side=tk.LEFT, padx=(50, 20))
            self.edit_btn = tk.Button(self, text="Edit", command=self.edit, width=10, font=10)
            self.edit_btn.pack(side=tk.LEFT)
            self.bind('<Return>', self.submit)
            # self.update_geometry_height(150)
        except ValueError as ve:
            print(ve)
            self.secondary_color_entry.delete(0, 'end')
            self.secondary_color_entry.focus()

    def choose_color(self):
        self.color_code = colorchooser.askcolor(title="Choose color", parent=self)
        if self.color_code[1] is None:
            return
        if self.primary_color_entry.winfo_exists() and self.primary_color_entry.winfo_ismapped():
            self.primary_color_entry.delete(0, 'end')
            self.primary_color_entry.insert(0, self.color_code[1])
            self.focus()
            self.primary_color_entry.focus()
        if self.secondary_color_entry.winfo_exists() and self.secondary_color_entry.winfo_ismapped():
            self.secondary_color_entry.delete(0, 'end')
            self.secondary_color_entry.insert(0, self.color_code[1])
            self.focus()
            self.secondary_color_entry.focus()
    
    def next_btn_command(self):
        print("next")
 
    def update_geometry_height(self, x):
        self.win_height += x
        self.geometry(f'{self.win_width}x{self.win_height}')

    def move_window_up(self, y_offset):
        self.geometry(f'+{self.x}+{self.y + self.parent.win_height - y_offset}')
        self.parent.geometry(f'+{self.x}+{self.y - y_offset}')

    def submit(self, event):
        self.save_input()
        # TODO need to save the user's input in the config file
    
    def submit_by_click(self):
        self.save_input()

    def save_input(self):
        print("save_input")

    def edit(self):
        print("edit")

