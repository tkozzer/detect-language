import os
import json

""" 
Simple method that uses a command line execution to get the value of the keyboard input language. It checks a list of languages (which can and will grow over time). If 
the language is in the list, then the language will be returned or if it doesn't exist the user will see message that says that the langauge is not supported. 

The purpose of this program is to help people detemine which keyboard input is current. This is helpful for multiligual people who type in multiple languages and is a useful
widget for those who do language exercise on apps/websites like duolingo. For example, A user who is doing exercises in Pinyin (Chinese) can easily see when their keyboard 
input is in English (or any other language) or Pinyin.

"""
class Language:

    def __init__(self) -> None:
        self.load_available_languages()
        self.current_language = self.get_current_language()

    def load_available_languages(self):
        #TODO check to make sure a language.json exists

        #TODO check list of AppleLanguages to determine which one the user has available
       #Only works when called from directory needs to be fixed 
        __location__ = os.path.dirname(os.path.realpath(__file__))

        with open(os.path.join(__location__, 'config.json'), 'r') as file:
            lang_dict = json.load(file)
            self.languages = lang_dict['languages']
            self.scim_list = lang_dict['scim_list']

    def get_current_language(self) -> tuple:
        #TODO check to make sure that the file exists on the computer --> ~/Library/Preferences/com.apple.HIToolbox.plist

        # These two commands will be used in conjunction to give us the the current keyboard layout 
        # *note* There is a bug in macOS that shows the wrong keyboard layout when switching from certain languages to pinyin
        keyboard_layout_command = "defaults read ~/Library/Preferences/com.apple.HIToolbox.plist AppleCurrentKeyboardLayoutInputSourceID"
        input_mode_command = 'defaults read ~/Library/Preferences/com.apple.HIToolbox.plist AppleSelectedInputSources | egrep "com.apple.inputmethod.SCIM.ITABC"'
        
        keyboard_layout = os.popen(keyboard_layout_command)
        input_mode = os.popen(input_mode_command)

        output_keyboard = keyboard_layout.read().strip().split('.')
        output_input = input_mode.read().strip().replace(' ', '').replace(';', '').replace('"', '').split("=")

        if len(output_input) > 1 and output_keyboard[-1] not in self.scim_list:
            defaults_write = "defaults write ~/Library/Preferences/com.apple.HIToolbox.plist \"AppleCurrentKeyboardLayoutInputSourceID\" 'com.apple.keylayout.PinyinKeyboard'"
            os.popen(defaults_write)
            print(f"Executed write to defaults: {defaults_write}")

        if output_keyboard[-1] not in self.languages.keys():
            return ("not_supported", self.languages["not_supported"])
        else:
            return (output_keyboard[-1], self.languages[output_keyboard[-1]])

            
        #TODO if not supported allow user to add it to the language.json



if __name__ == "__main__":
    # Used to test
    # pass
    lang = Language()
    print(lang.get_current_language())


