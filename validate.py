
class Validator:

    def __init__(self):
        pass

    @staticmethod
    def validate_entry_input(input, **kwargs) -> bool:
        print(input)
        if 'type' in kwargs:
            validate_type = kwargs['type']
            
        if len(input) == 0 or len(input) >= 30:
            raise ValueError("There was no input entered. Please input anything greater than 0 and less than 30")
        if validate_type == 'lang':
            # raise ValueError("Language isn't accepted")
            pass
        if validate_type == 'color':
            # raise ValueError("Color not accepted")
            pass
        
        return True

        