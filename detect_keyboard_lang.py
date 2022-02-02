import os
import json

""" 
Simple method that uses a command line execution to get the value of the keyboard input language. The
only two langauges that are accepted at the moment are Chinese and English. There is simple logic that checks
to see if English is detected or nothing is detected. It gets a bit complicated detecting Pinyin (Chinese), so
it comes up empty. This will suffice for now since this is a tool to help with Duolingo exercises.
"""
class Language:

    def __init__(self) -> None:
        self.load_available_languages()
        self.current_language = self.get_current_language()

    def load_available_languages(self):
        #TODO check to make sure a language.json exists

        #TODO check list of AppleLanguages to determine which one the user has available
        
        __location__ = os.getcwd()

        with open(os.path.join(__location__, 'language.json'), 'r') as lang_json:
            self.languages = json.load(lang_json)

    def get_current_language(self) -> dict:

        # Use the command line to read current keylayout
        keyboard_layout = "defaults read ~/Library/Preferences/com.apple.HIToolbox.plist AppleCurrentKeyboardLayoutInputSourceID"

        data = os.popen(keyboard_layout)
        output = data.read().strip()
        output = output.split('.')

        return self.languages[output[-1]]



current = Language()
print(current.load_available_languages())


