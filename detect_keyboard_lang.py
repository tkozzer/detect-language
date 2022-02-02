import os
import json
import plistlib
from io import StringIO
from plistlib import readPlist
from textwrap import indent

""" 
Simple method that uses a command line execution to get the value of the keyboard input language. The
only two langauges that are accepted at the moment are Chinese and English. There is simple logic that checks
to see if English is detected or nothing is detected. It gets a bit complicated detecting Pinyin (Chinese), so
it comes up empty. This will suffice for now since this is a tool to help with Duolingo exercises.
"""


def detect_keyboard_language():
    language = {}
    # Use the command line to
    get_list = "defaults read ~/Library/Preferences/com.apple.HIToolbox.plist AppleSelectedInputSources"
    search_for_keyboard = "egrep -w 'KeyboardLayout Name'"
    search_for_input_mode = "egrep -w 'Input Mode'"

    # with open('/Library/Preferences/com.apple.HIToolbox.plist', 'rb') as itl:
    #     library = plistlib.load(itl)

    # print(json.dumps(library,indent=4))

    # data = os.popen("plutil -convert json -o - ~/Library/Preferences/com.apple.HIToolbox.plist")
    # output = data.read()

    # output = json.loads(output)
    # print(json.dumps(output['AppleSelectedInputSources'],indent=4))
    # print(type(output))

    # stream = os.popen(f"{get_list} | {search_for_keyboard}")
    # output = stream.read()

    # if(len(output) == 0):
    #     stream = os.popen(f"{get_list} | {search_for_input_mode}")
    #     output = stream.read()

    # in_file = StringIO(output)
    # plist_dict = readPlist(in_file)

    # print(json.dumps(plist_dict))

    # check_keyboard = check_keyboard.read()
    # print(len(check_keyboard))
    # print(check_keyboard.replace("=", ":").replace("(", "{").replace(")", "}"))
    # output = json.dumps(check_keyboard)
    # print(output.strip())
    # output = output.replace("\"", "").replace(";", "").strip().split("=")

    # print(output)

    # if(len(output) > 1):
    #     output_dict = {'name': output[1].strip()}

    # if(len(output) > 1 and output_dict['name'] == "U.S."):
    #     language = {"lang":"English", "bg":"#002868", "fg":"#ff4d4d"}
    # else:
    #     language = {"lang":"Chinese", "bg":"#ff4d4d", "fg":"white"}
    # return language
detect_keyboard_language()
