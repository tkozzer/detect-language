
class Validator:

    def __init__(self):
        pass

    @staticmethod
    def validate_entry_input(input, **kwargs) -> bool:
        print(input)
        if 'type' in kwargs:
            validate_type = kwargs['type']
            
        if validate_type == 'lang':
            
            # raise ValueError("Language isn't accepted")
            pass
        if validate_type == 'color':

            # raise ValueError("Color isn't accepted")
            pass
        
        return True

        