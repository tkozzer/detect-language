import os
import json
import tkinter as tk
import math
import time

from tkinter.constants import BOTH
from turtle import window_height
from detect_keyboard_lang import Language
from right_click_menu import RightClick
from top_menu import TopMenu
from tool_tip import Tooltip


class Win(tk.Tk):

    def __init__(self, master=None):
        # Create draggable always on top window that has one label that is dynamic based on
        # which keyboard language is detected.
        tk.Tk.__init__(self, master)
        self.overrideredirect(True)
        # Only need this self.overrideredirct in certain circumstances TODO figure out the edge cases for this and only use this when necessary
        self.overrideredirect(False)
        self.attributes('-topmost', 'true')
        self.attributes('-transparent', True)
        self.config(background='systemTransparent')

        self.app_config = self.get_config()
        self.initialize_variables()
        # TODO see initialize_window() method for TODO details
        self.initialize_window()

        self.canvas = tk.Canvas(self, bg="systemTransparent", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=1)

        self.language = Language()
        self.label = tk.Label(self.canvas, width=self.label_width, height=self.label_height, font=(self.label_font_type, self.label_font_size))

        self.bind('<B1-Motion>', self.dragwin)
        self.bind('<Button-1>', self.clickwin)

        self.bind('<Double-Button-1>', self.increase_size)
        # TODO need to check other mouses to make sure <Button-2> is the right click in all circumstances
        self.bind('<Button-2>', self.right_click)

        # TODO Need to do more testing on and parameters of tool tip
        # TODO Create a smoother fading of tool tip.
        self.label_tooltip = Tooltip(self.label, text="Double click to increase size", wraplength=200)

        # TODO add more menu bar items
        self.menubar = TopMenu(self)

        self.label.pack(padx=5, pady=5)
        self.show_language()

    def initialize_window(self):
        # TODO turn this into an initialize window starting position
        # We want the user to be able to have the window appear on the their screen in the correct location.
        # The x and y coordinates will be stored in the config.json file and user till be able to automatically set those
        # through the right click options.
        self.update_idletasks()

        # if width, height, x, y exist do this

        # else do that

        self.width = 200
        self.height = 70
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.x = int((self.screen_width/2) - (self.width/2))
        self.y = int((self.screen_height/2) - (self.height/2))

        self.geometry(f'{self.width}x{self.height}+{self.x}+{self.y}')


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

    def clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    # The will import in detect_keyboard_lang and check which language is used and print it to the window
    def show_language(self):
        self.current_lang = self.language.get_current_language()
        self.label.config(text=self.current_lang[1]["language"], fg=self.current_lang[1]
                          ["fg"], bg=self.current_lang[1]["bg"], width=self.label_width)
        if self.is_first_time:
            self.rounded = self.round_rectangle(0, 0, self.win_width, self.win_height, fill=self.current_lang[1]['bg'])
            self.is_first_time = False
        else:
            self.update_rect_coords(0, 0, self.win_width, self.win_height)
            self.canvas.itemconfig(self.rounded, fill=self.current_lang[1]['bg'])
        self.geometry(f'{self.win_width}x{self.win_height}')
        self.after(100, self.show_language)

    def increase_size(self, event):
        # TODO smooth out the logic of the click
        self.update_idletasks()
        self.click_count += 1
        if(self.click_count % 2 == 0):
            self.label_width = 10
            self.label_height = 2
            self.label_font_size = 40
            self.win_width = 200
            self.win_height = 70
            self.win_x = self.winfo_rootx() + 50
            self.win_y = self.winfo_rooty() + 25
        else:
            self.label_width = math.floor(self.label_width * 1.50)
            self.label_height = math.floor(self.label_height * 1.50)
            self.label_font_size = math.floor(self.label_font_size * 1.3)
            self.win_width = self.win_width + 100
            self.win_height = self.win_height + 50
            self.win_x  = self.winfo_rootx() - 50
            self.win_y = self.winfo_rooty() - 25

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
        self.right_click = RightClick(self, event)

    def get_config(self) -> dict:
        # TODO does config json files exist if so open file and get config variables

        __location__ = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(__location__, 'config.json'), 'r') as file:
            config_dict = json.load(file)
            self.app_config = config_dict['config']
        return self.app_config

    def initialize_variables(self):
        self.label_width = self.app_config['label']['width']
        self.label_height = self.app_config['label']['height']
        self.label_font_type = self.app_config['label']['font_type']
        self.label_font_size = self.app_config['label']['font_size']
        
        self.win_width = self.app_config['win']['width']
        self.win_height = self.app_config['win']['height']
        self.win_x = self.app_config['win']['x']
        self.win_y = self.app_config['win']['y']
        
        self.radius = 20
        self.click_count = 0
        self.is_first_time = True

