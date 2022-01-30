import os

""" 
Simple method that uses a command line execution to get the value of the keyboard input language. The
only two langauges that are accepted at the moment are Chinese and English. There is simple logic that checks
to see if English is detected or nothing is detected. It gets a bit complicated detecting Pinyin (Chinese), so
it comes up empty. This will suffice for now since this is a tool to help with Duolingo exercises.
"""
def detect_keyboard_language():
    language = {}
    get_list = "defaults read ~/Library/Preferences/com.apple.HIToolbox.plist AppleSelectedInputSources"
    search_for_keyboard = "egrep -w 'KeyboardLayout Name'"
    both = f"{get_list} | {search_for_keyboard}"
    
    stream = os.popen(both)
    output = stream.read()
    output = output.replace("\"", "").replace(";", "").strip().split("=")

    if(len(output) > 1):
        output_dict = {'name': output[1].strip()}


    if(len(output) > 1 and output_dict['name'] == "U.S."):
        language = {"lang":"English", "bg":"#002868", "fg":"#ff4d4d"}
    else:
        language = {"lang":"Chinese", "bg":"#ff4d4d", "fg":"white"}

    return language