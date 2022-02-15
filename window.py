import os
import json
import tkinter as tk
import math
import time
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
        self.app_config = self.get_config()
        self.click_count = 0

        # Places window in the middle of screen
        self.eval('tk::PlaceWindow . center')

        self.language = Language()
        self.label = tk.Label(self, width=self.app_config['width'], height=self.app_config['height'], padx=self.app_config['padx'],
                              relief=self.app_config['relief'], borderwidth=self.app_config['borderwidth'], font=(self.app_config['font_type'], self.app_config['font_size']))
        self.label_x = tk.Label(self, text="X", height=self.app_config['height'], relief=self.app_config['relief'],
                                borderwidth=self.app_config['borderwidth'], font=(self.app_config['font_type'], self.app_config['font_size']))
        
        self.bind('<B1-Motion>', self.dragwin)
        self.bind('<Button-1>', self.clickwin)

        self.label.bind('<Double-Button-1>', self.increase_size)
        # TODO need to check other mouses to make sure <Button-2> is the right click in all circumstances
        self.label.bind('<Button-2>', self.right_click)
        self.label_x.bind("<Double-Button-1>", self.exit)

        # TODO Need to do more testing on and parameters of tool tip
        # TODO Create a smoother fading of tool tip.
        self.x_tooltip = Tooltip(
            self.label_x, text="Double click to exit", wraplength=200)
        self.label_tooltip = Tooltip(
            self.label, text="Double click to increase size", wraplength=200)

        # TODO add more menu bar items
        self.menubar = TopMenu(self)

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
        self.label.config(text=self.current_lang[1]["language"], fg=self.current_lang[1]
                          ["fg"], bg=self.current_lang[1]["bg"], width=self.app_config['width'])
        self.config(bg=self.current_lang[1]["bg"])
        self.label_x.config(
            fg=self.current_lang[1]["fg"], bg=self.current_lang[1]["bg"])
        self.after(100, self.show_language)

    def increase_size(self, event):
        # TODO smooth out the logic of the click
        self.click_count += 1
        if(self.click_count == 2):
            self.app_config['width'] = 10
            self.app_config['height'] = 2
            self.app_config['font_size'] = 15
            self.click_count = 0
        else:
            self.app_config['width'] = math.floor(self.app_config['width'] * 1.50)
            self.app_config['height'] = math.floor(self.app_config['height'] * 1.50)
            self.app_config['font_size'] = math.floor(self.app_config['font_size'] * 2)

        # TODO priliminary window increase size animation. Needs work
        print(self.label['width'])
        print(self.app_config['width'])
        current_width = self.label['width']
        next_width = self.app_config['width']
        stepper = 1 if current_width < next_width else -1
        for x in range(self.label['width'], self.app_config['width'], stepper):
            print(f'x: {x}')
            self.label.config(width=x)
            time.sleep(.01)
            self.update()


        self.label.config(height=self.app_config['height'], width=self.app_config['width'],
                          font=(self.app_config['font_type'], self.app_config['font_size']))
        self.label_x.config(height=self.app_config['height'],
                          font=(self.app_config['font_type'], self.app_config['font_size']))

    def right_click(self, event):
        # TODO create a right click menu that lets the user input new languages, check current languages and other options
        self.right_click = RightClick(self, event)

    def get_config(self) -> dict:
        # TODO does config json files exist if so open file and get config variables

        __location__ = os.path.dirname(os.path.realpath(__file__))
        print(__location__)
        with open(os.path.join(__location__, 'config.json'), 'r') as file:
            config_dict = json.load(file)
            self.app_config = config_dict['config']
        return self.app_config

    def exit(self, event):
        self.destroy()
