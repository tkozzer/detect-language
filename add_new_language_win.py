import tkinter as tk
import rounded_rect as rr

from validate import Validator as v
from tkinter import font, colorchooser

class AddLanguage(tk.Toplevel):

    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.main_config = self.parent.config.get_config()
        self.lang_config = self.main_config['languages']
        self.overrideredirect(1)
        self.overrideredirect(0)
        self.attributes('-topmost', 'true')
        self.attributes('-transparent', True)
        self.config(background=self.parent.current_lang[1]['bg'])

        self.setup()
        self.language = self.parent.language.output_keyboard[-1]
            
        self.create_widgets()
        self.bindings()

    # These two methods are the brains behind dragging a menuless window
    def dragwin(self, event):
        self.x = self.winfo_pointerx() - self._offsetx
        self.y = self.winfo_pointery() - self._offsety - 100
        self.parent.geometry(f'+{self.x}+{self.y}')
        self.geometry(f'+{self.x}+{self.y + self.parent.win_height}')

    def clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def setup(self):
        self.FOCUS_IN = '<FocusIn>'
        self.ENTER_KEY = '<Return>'

        self.win_width = self.parent.win_width
        self.win_height = self.parent.win_height - 5
        self.x_pos = self.parent.winfo_rootx()
        self.y_pos = self.parent.winfo_rooty()
        self.x = self.x_pos
        self.y = self.y_pos
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family=self.parent.app_config['label']['font_type'], size=20)
        self.geometry(f'{self.win_width}x{self.win_height}+{self.x_pos}+{self.y_pos + self.win_height}')

    def right_click(self, event):
        self.parent.right_click(event)

    def create_widgets(self):
        # Canvas
        self.canvas_border = tk.Canvas(self, bg="systemTransparent", highlightthickness=0, height=20)
        self.canvas = tk.Canvas(self.canvas_border, bg="systemTransparent", highlightthickness=0)

        # Labels
        self.current_lang_label = tk.Label(self, fg='white', bg='black', text=f"Current Language:\n{self.language}")
        self.lang_label = tk.Label(self.canvas,fg='white', bg='black', text="Enter Language: ")
        self.primary_color_label = tk.Label(self, fg='white', bg='black', text="Enter primary color: ")
        self.secondary_color_label = tk.Label(self, fg='white', bg='black', text="Enter secondary color: ")
        
        # Seperators
        self.seperator1 = tk.Frame(self, bg='white', height=1, bd=0)
        self.seperator2 = tk.Frame(self, bg='white', height=1, bd=0)
        
        # Entries
        self.lang_entry = tk.Entry(self, bg="white", fg='black')
        self.primary_color_entry = tk.Entry(self, bg="white", fg='black')
        self.secondary_color_entry = tk.Entry(self, bg="white", fg='black')
        
        # Buttons
        self.color_btn = tk.Button(self, text="Pick a color", width=10, command=self.choose_color, font=10)
        self.next_btn = tk.Button(self, text="Next", width=5, command=self.next_btn_command, font=10)
        self.prev_btn = tk.Button(self, text="Prev", width=5, command=self.prev_btn_command, font=10)
        self.submit_btn = tk.Button(self, text="Submit", command=self.submit_click, width=10, font=10)
        self.edit_btn = tk.Button(self, text="Edit", command=self.edit, width=10, font=10)
        
        # Pack the widgets
        self.pack_widgets()
        self.update()
        self.rounded = rr.round_rectangle(self.canvas, 0, 0, self.canvas_border.winfo_width() - 15, 40, radius=10, fill='black')
        
        # Insert current language from OS and set focus on entry box
        self.lang_entry.insert(0, self.language)
        self.lang_entry.focus()
        
        # Increase the win_height of both windows and move both windows up
        self.update_geometry_height(115)
        self.original_win_height = self.win_height
        self.move_window_up(self.win_height + self.parent.win_height)

    def bindings(self):
        self.lang_entry.bind(self.ENTER_KEY, self.lang_entry_bind)
        self.primary_color_entry.bind(self.ENTER_KEY, self.primary_color_entry_bind)
        self.secondary_color_entry.bind(self.ENTER_KEY, self.secondary_color_entry_bind)

        self.bind('<B1-Motion>', self.dragwin)
        self.bind('<Button-1>', self.clickwin)
        self.bind('<Button-2>', self.right_click)
    
    def pack_widgets(self):
        self.seperator1.pack(fill='x', pady=(10,5))
        self.current_lang_label.pack(pady=5)
        self.seperator2.pack(fill='x', pady=(5,5))
        self.canvas_border.pack(fill=tk.BOTH, expand=0,pady=10, padx=50)
        self.canvas.pack(fill=tk.BOTH, expand=1, padx=7, pady=7)
        self.lang_label.pack(pady=1)
        self.lang_entry.pack()
        self.next_btn.pack(pady=(10,10))
    
    def lang_entry_bind(self, event):
        try:
            v.validate_entry_input(self.lang_entry.get(), type="lang")
            self.primary_color_entry.focus()
            self.lang_label.config(text=f'{self.lang_entry.get()}')
            self.lang_key = self.lang_entry.get()
            self.lang_entry.pack_forget()
            self.next_btn.pack_forget()
            self.primary_color_label.pack()
            self.primary_color_entry.pack()
            self.prev_btn.pack(side=tk.LEFT, padx=(40,0), pady=(10,10))
            self.color_btn.pack(side=tk.LEFT, padx=(12, 1), pady=(10,10))
            self.next_btn.pack(side=tk.LEFT, padx=(10,10), pady=(10,10))
            self.update_geometry_height(30)
        except ValueError as ve:
            print(ve)
            self.lang_entry.bind(self.FOCUS_IN, lambda e: e.widget.select_range(0, tk.END))
            self.lang_entry.focus()             

    def primary_color_entry_bind(self, event):
        try:
            v.validate_entry_input(self.primary_color_entry.get(), type="color")
            self.secondary_color_entry.focus()
            primary_color = self.primary_color_entry.get()
            self.lang_label.config(fg=primary_color, pady=5)
            self.fg_key = primary_color
            self.primary_color_entry.pack_forget()
            self.primary_color_label.pack_forget()
            self.prev_btn.pack_forget()
            self.color_btn.pack_forget()
            self.next_btn.pack_forget()
            self.secondary_color_label.pack()
            self.secondary_color_entry.pack()
            self.prev_btn.pack(side=tk.LEFT, padx=(40,0), pady=(10,10))
            self.color_btn.pack(side=tk.LEFT, padx=(12, 1), pady=(10,10))
            self.next_btn.pack(side=tk.LEFT, padx=(10,10), pady=(10,10))
            self.update_geometry_height(7)
        except ValueError as ve:
            print(ve)
            self.focus()
            self.primary_color_entry.focus()
            self.primary_color_entry.bind(self.FOCUS_IN, lambda e: e.widget.select_range(0, tk.END))
        
    def secondary_color_entry_bind(self, event):
        try:
            v.validate_entry_input(self.secondary_color_entry.get(), type="color")
            secondary_color = self.secondary_color_entry.get()
            self.bg_key = secondary_color
            self.lang_label.config(bg=secondary_color)
            self.canvas.itemconfig(self.rounded, fill=secondary_color)
            self.secondary_color_entry.pack_forget()
            self.secondary_color_label.pack_forget()
            self.prev_btn.pack_forget()
            self.color_btn.pack_forget()
            self.next_btn.pack_forget()
            self.submit_btn.pack(side=tk.LEFT, padx=(50, 10), pady=(10, 30))
            self.edit_btn.pack(side=tk.LEFT, pady=(10,30))
            self.submit_id = self.bind(self.ENTER_KEY, self.submit)
            self.update_geometry_height(-35)
        except ValueError as ve:
            print(ve)
            self.focus()
            self.secondary_color_entry.focus()
            self.secondary_color_entry.bind(self.FOCUS_IN, lambda e: e.widget.select_range(0, tk.END))

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
        # TODO add functionality
        if self.lang_entry.winfo_ismapped():
            self.lang_entry_bind(None)
        if self.primary_color_entry.winfo_ismapped():
            self.primary_color_entry_bind(None)
        if self.secondary_color_entry.winfo_ismapped():
            self.secondary_color_entry_bind(None)

    def prev_btn_command(self):
        # TODO add functionality
        pass
 
    def update_geometry_height(self, x):
        self.win_height += x
        self.geometry(f'{self.win_width}x{self.win_height}')

    def move_window_up(self, y_offset):
        self.update()
        self.parent.update()
        self.geometry(f'+{self.winfo_rootx()}+{self.winfo_rooty() + self.parent.win_height - y_offset}')
        self.parent.geometry(f'+{self.winfo_rootx()}+{self.winfo_rooty() - y_offset}')

    def submit(self, event):
        self.submit_click()
    
    def submit_click(self):
        self.save_input(self.language, secondary_color=self.bg_key, primary_color=self.fg_key, language=self.lang_key)
        self.parent.input_win.destroy()
        self.destroy()
        delattr(self.parent, 'input_win')
        del self.parent.right_click1.__dict__['input_win']
        # This will add the increase/decrease binding back on
        self.parent.double_click_id = self.parent.bind('<Double-Button-1>', self.parent.increase_size)


    def save_input(self, key, **kwargs):
        self.lang_config[key] = {}
        if 'language' in kwargs:
            self.lang_config[key]['language'] = kwargs['language']
        if 'primary_color' in kwargs:
            self.lang_config[key]['fg'] = kwargs['primary_color']
        if 'secondary_color' in kwargs:
            self.lang_config[key]['bg'] = kwargs['secondary_color']
        self.parent.config.save_config(self.main_config)

    def edit(self):
        self.win_height = self.original_win_height
        self.unbind(self.ENTER_KEY, self.submit_id)
        self.update_geometry_height(10)
        self.submit_btn.pack_forget()
        self.edit_btn.pack_forget()
        self.lang_label.pack()
        self.lang_entry.pack()
        self.next_btn.pack(pady=12)
        self.lang_entry.focus()
        self.lang_entry.bind(self.FOCUS_IN, lambda e: e.widget.select_range(0, tk.END))
        self.primary_color_entry.bind(self.FOCUS_IN, lambda e: e.widget.select_range(0, tk.END))
        self.secondary_color_entry.bind(self.FOCUS_IN, lambda e: e.widget.select_range(0, tk.END))
        



