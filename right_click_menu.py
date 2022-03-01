from faulthandler import disable
import tkinter as tk
import sys
import traceback

from add_new_language_win import AddLanguage

class RightClick(tk.Frame):

    def __init__(self, win, **kwargs) -> None:
        self.kwargs = kwargs
        self.win = win
        self.config = self.win.config.get_config()
        self.right_click_menu = tk.Menu(self.win)
        self.right_click_menu.add_command(label="About Detect Language", command=self.about)
        self.right_click_menu.add_command(label="Check for Updates", command=self.check_updates)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label="Customize...", command=self.customize)
        self.right_click_menu.add_command(label="Set Position", command=self.set_position)
        self.right_click_menu.add_command(label="Add New Language", command=self.add_new_language)
        self.right_click_menu.add_command(label="Quit", command=self.exit)

        # self.popup(event)

    def popup(self, event):
        try:
            self.right_click_menu.post(event.x_root, event.y_root)
        finally:
            # TODO figure out what grab_release() does
            # self.right_click_menu.grab_release()
            pass

    def about(self):
        pass

    def check_updates(self):
        pass

    def customize(self):
        pass

    def set_position(self):
        try:
            click_count = 0 if self.win.click_count % 2 == 0 else 1

            if 'win' not in self.config['config']:
                update_dict = {'win': {'x': self.win.winfo_rootx(), 'y':  self.win.winfo_rooty(), 'width': self.win.winfo_width(), 'height': self.win.winfo_height()}}
                self.config['config'].update(update_dict)
            else:
                self.config['config']['win']['x'] = self.win.winfo_rootx()
                self.config['config']['win']['y'] = self.win.winfo_rooty()
                self.config['config']['win']['width'] = self.win.winfo_width()
                self.config['config']['win']['height'] = self.win.winfo_height()

            if 'label' not in self.config['config']:
                update_dict = {'label': {'width': self.win.label['width'], 'height': self.win.label['height'], 'font_type': self.win.label_font_type, 'font_size': self.win.label_font_size, 'click_count': click_count}}
                self.config['config'].update(update_dict)
            else:
                self.config['config']['label']['width'] = self.win.label['width']
                self.config['config']['label']['height'] = self.win.label['height']
                self.config['config']['label']['font_type'] = self.win.label_font_type
                self.config['config']['label']['font_size'] = self.win.label_font_size
                self.config['config']['label']['click_count'] = click_count
            is_saved = self.win.config.save_config(self.config)
            if not is_saved:
                raise FileExistsError("File was not found.")
        except FileExistsError as fe:
            print(f'Error: {fe}')
        except Exception as e:
            print(f"There seems to be an error.")
            traceback.print_exc()

    def add_new_language(self):
        self.language = self.win.language.output_keyboard 
        if self.language[-1] in self.config['languages']:
            print(self.config['languages'][self.language[-1]])
        else:
            print(self.language[-1])
            print('Not in config.json')
            self.input_win = AddLanguage(self.win)
            self.disable_add_new_language()
        
            # self.input_win.grab_set()

    def disable_add_new_language(self):
        self.right_click_menu.entryconfig("Add New Language", state="disabled")

    def enable_add_new_language(self):
        self.right_click_menu.entryconfig("Add New Language", state="normal")

    def exit(self):
        try:
            self.win.destroy()
        except SystemExit:
            sys.exit()
        except Exception:
            sys.exit()
