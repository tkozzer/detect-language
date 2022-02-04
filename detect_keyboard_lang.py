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
       #Only works when called from directory needs to be fixed 
        __location__ = os.path.dirname(os.path.realpath(__file__))

        with open(os.path.join(__location__, 'language.json'), 'r') as lang_json:
            self.languages = json.load(lang_json)

    def get_current_language(self) -> tuple:

        # Use the command line to read current keylayout
        keyboard_layout = "defaults read ~/Library/Preferences/com.apple.HIToolbox.plist AppleCurrentKeyboardLayoutInputSourceID"

        data = os.popen(keyboard_layout)
        output = data.read().strip()
        output = output.split('.')

        #TODO *fix bug* When a use switches from a non-US keyboard input to Pinyin 'defaults read' doesn't
        # detect that the keyboard has changed. In order to fix this bug, there will need to be a call to AppleSelectedInputSources
        # need to look for "Input Mode" = "com.apple.inputmethod.SCIM.ITABC"。 This can also be found under the first index of
        # the AppleInputSourceHistory

        #TODO if language isn't supported print to widget "Language Currently Not Supported"
        print(f"output[-1] not in self.languages.keys(): {output[-1] not in self.languages.keys()}")
        print(f"output[-1]: {output[-1]}")
        if output[-1] not in self.languages.keys():
            return ("not_supported", self.languages["not_supported"])
        else:
            return (output[-1], self.languages[output[-1]])

            
        #TODO if not supported allow user to add it to the language.json



if __name__ == "__main__":
    # Used to test
    # pass
    lang = Language()
    print(lang.get_current_language())


