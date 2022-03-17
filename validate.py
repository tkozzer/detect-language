import re

from config import Config

class Validator:
    file = 'json/tkinter_colors.json'
    def __init__(self):
        pass

    @staticmethod
    def validate_entry_input(input, **kwargs) -> tuple:
        if 'type' in kwargs:
            validate_type = kwargs['type']
            
        if validate_type == 'lang':
            if len(input) == 0 or len(input) >= 20:
                raise ValueError("Please input anything greater than 0 and less than 30.")
            # raise ValueError("Language isn't accepted")
        if validate_type == 'color':
            # TODO check if input starts with a '#', if so make sure hex color is of correct length
            # else if color is in plaintext, make sure it is an acceptable tkinter color
            # raise ValueError("Color not accepted")
            if input[0] == "#":
                regex = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
                p = re.compile(regex)
                if re.search(p, input):
                    return (True, input)
                else:
                    raise ValueError("Hex colors must be either 3 or 6 characters in length")
            else:
                colors_dict = Config(Validator.file)
                colors_list = colors_dict.get_config()['colors']
                str_match = [s for s in colors_list if s.casefold() == input.casefold()]
                
                if str_match:
                    return (True, str_match[0])
                else:
                    raise ValueError("This color isn't acceptable tkinter color. Note: Tkinter colors are case sensitive.")
        
        # return True

        