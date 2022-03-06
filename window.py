import tkinter as tk
import time

from tkinter.constants import BOTH
from detect_keyboard_lang import Language
from right_click_menu import RightClick
from top_menu import TopMenu
from tool_tip import Tooltip
from config import Config

class Win(tk.Tk):


    def __init__(self, master=None):
        # Create draggable always on top window that has one label that is dynamic based on
        # which keyboard language is detected.
        tk.Tk.__init__(self, master)
        self.overrideredirect(True)
        # Only need this self.overrideredirct in certain circumstances TODO figure out the edge cases for this and only use this when necessary
        self.overrideredirect(False)
        self.attributes('-topmost', True)
        self.attributes('-transparent', True)
        self.config(background='systemTransparent')
        self.file = "json/config.json"

        # Window pos setup along with initialization of variables
        self.setup()

        self.canvas = tk.Canvas(self, bg="systemTransparent", highlightthickness=0)
        self.label = tk.Label(self.canvas, width=self.label_width, height=self.label_height, font=(self.label_font_type, self.label_font_size))

        self.bindings()

        # TODO Need to do more testing on and parameters of tool tip
        # TODO Create a smoother fading of tool tip.
        self.label_tooltip = Tooltip(self.label, text=self.tool_tip_text(), wraplength=200)

        # TODO add more menu bar items
        self.menubar = TopMenu(self)
        self.right_click1 = RightClick(self)

        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.label.pack(padx=5, pady=5)
        self.language = Language(win=self)
        self.show_language()

    def bindings(self, **kwargs):
        # TODO need to check other mouses to make sure <Button-2> is the right click in all circumstances
        self.bind('<Button-2>', self.right_click)
        self.bind('<B1-Motion>', self.dragwin)
        self.bind('<Button-1>', self.clickwin)
        # The first time through all bindings will be activated. If bindings is called again a key-word can be
        # passed to unbind increase/decrease. This is use for when input is required for a adding a new language
        if 'double_click' in kwargs:
            is_double_on = kwargs['double_click']
            if not is_double_on:
                self.unbind('<Double-Button-1>', self.double_click_id)
        else:
           self.double_click_id = self.bind('<Double-Button-1>', self.increase_size)

    def setup(self):
        self.update_idletasks()
        self.config = Config(self.file)
        self.app_config = self.config.get_config()['config']

        if 'win' in self.app_config and 'label' in self.app_config:
            self.initialize_variables()
        else:
            self.win_width = 200
            self.win_height = 70
            self.screen_width = self.winfo_screenwidth()
            self.screen_height = self.winfo_screenheight()

            self.win_x = int((self.screen_width/2) - (self.win_width/2))
            self.win_y = int((self.screen_height/2) - (self.win_height/2))

            self.label_width = 10
            self.label_height = 2
            self.label_font_type = "Helvetica"
            self.label_font_size = 40
            self.click_count = 0
        
        self.radius = 20
        self.is_first_time = True
        self.first_pass = True

        self.geometry(f'{self.win_width}x{self.win_height}+{self.win_x}+{self.win_y}')

    def round_rectangle(self, x1, y1, x2, y2, **kwargs):  # Creating a rounded rectangle
        radius = self.radius
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]

        
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def update_rect_coords(self, x1, y1, x2, y2, **kwargs):  # Creating a rounded rectangle
        radius = self.radius
        points = [x1+radius, y1,
                    x1+radius, y1,
                    x2-radius, y1,
                    x2-radius, y1,
                    x2, y1,
                    x2, y1+radius,
                    x2, y1+radius,
                    x2, y2-radius,
                    x2, y2-radius,
                    x2, y2,
                    x2-radius, y2,
                    x2-radius, y2,
                    x1+radius, y2,
                    x1+radius, y2,
                    x1, y2,
                    x1, y2-radius,
                    x1, y2-radius,
                    x1, y1+radius,
                    x1, y1+radius,
                    x1, y1]

        
        return self.canvas.coords(self.rounded, points)

    # These two methods are the brains behind dragging a menuless window
    def dragwin(self, event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry(f'+{x}+{y}')

        if hasattr(self, 'input_win'):
            self.input_win.geometry(f'+{x}+{y + self.input_win.win_height - 10}')

    def clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    # The will import in detect_keyboard_lang and check which language is used and print it to the window
    def show_language(self):
        if not self.is_first_time:
            self.last_lang = self.current_lang[0]
        self.current_lang = self.language.get_current_language()
        self.first_pass = not self.is_first_time and self.last_lang != self.current_lang[0]

        if self.current_lang[0] == 'not_supported' and not self.first_pass:
            self.set_label_vars()

        if self.first_pass:
            self.set_label_vars()

        if hasattr(self, 'input_win'):
            self.right_click1.disable_add_new_language()
        elif self.current_lang[0] != 'not_supported':
            self.right_click1.disable_add_new_language()
        else:
            self.right_click1.enable_add_new_language()

        self.label.config(text=self.current_lang[1]["language"], fg=self.current_lang[1]
                          ["fg"], bg=self.current_lang[1]["bg"], width=self.label_width, font=(self.label_font_type,self.label_font_size))

        if self.is_first_time:
            self.rounded = self.round_rectangle(0, 0, self.win_width, self.win_height, fill=self.current_lang[1]['bg'])
            self.is_first_time = False
        else:
            self.update_rect_coords(0, 0, self.win_width, self.win_height)
            self.canvas.itemconfig(self.rounded, fill=self.current_lang[1]['bg'])
        self.geometry(f'{self.win_width}x{self.win_height}')
        self.after(100, self.show_language)

    def increase_size(self, event):
        self.update_idletasks()
        self.click_count += 1
        self.set_label_vars()
        # There are two size choices, change the number to after the modulo to increase size choices
        if self.click_count % 2 == 0:
            self.win_width = 200
            self.win_height = 70
            self.win_x = self.winfo_rootx() + 50
            self.win_y = self.winfo_rooty() + 25
            self.label_tooltip.update_text(self.tool_tip_text())
        else:
            self.win_width = 200 + 100
            self.win_height = 70 + 50
            self.win_x = self.winfo_rootx() - 50
            self.win_y = self.winfo_rooty() - 25
            self.label_tooltip.update_text(self.tool_tip_text())

        # TODO preliminary window increase size animation. Works fairly decent, but could use a bit more work. Sufficient for now
        current_width = self.label['width']
        next_width = self.label_width

        stepper = 1 if current_width < next_width else -1
        for x in range(self.label['width'], self.label_width, stepper):
            self.label.config(width=x, height=self.label_height, font=(self.label_font_type, self.label_font_size))
            self.update_rect_coords(0, 0, self.win_width, self.win_height)
            # TODO Make it so when the window increases, it increases from the middles out
            self.geometry(f'{self.win_width}x{self.win_height}+{self.win_x}+{self.win_y}')
    
            time.sleep(.01)
            self.update()

    def right_click(self, event):
        # TODO create a right click menu that lets the user input new languages, check current languages and other options
        self.right_click1.popup(event)
        if 'input_win' in self.right_click1.__dict__:
            self.input_win = self.right_click1.input_win

    def tool_tip_text(self):
        if self.click_count % 2 == 0:
            return "Double click to increase size"
        else:
            return "Double click to decrease size"

    def set_label_vars(self):
        if self.click_count % 2 == 0:
            if self.current_lang[0] == 'not_supported':
                self.label_width = 12
                self.label_font_size = int(40/1.6)
            else:
                self.label_width = 10
                self.label_font_size = 40
            self.label_height = 2
        else:
            if self.current_lang[0] == 'not_supported':
                self.label_width = 17
                self.label_font_size = int(52/1.6)
            else:
                self.label_width = 15
                self.label_font_size = 52
            self.label_height = 3

    def initialize_variables(self):
        # This method will only be called if label and win exist in self.app_config dict
        # Set label variables
        self.label_width = self.app_config['label']['width']
        self.label_height = self.app_config['label']['height']
        self.label_font_type = self.app_config['label']['font_type']
        self.label_font_size = self.app_config['label']['font_size']
        self.click_count = self.app_config['label']['click_count']

        # Set win variables
        self.win_width = self.app_config['win']['width']
        self.win_height = self.app_config['win']['height']
        self.win_x = self.app_config['win']['x']
        self.win_y = self.app_config['win']['y']
        


