import os
import traceback
from window import Win
import sys
if __name__ == "__main__":
    try:
        from sys import platform

        # Check if we're on OS X, first.
        if platform == 'darwin':
            from Foundation import NSBundle
            bundle = NSBundle.mainBundle()
            if bundle:
                info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
                if info and info['CFBundleName'] == 'Python':
                    info['CFBundleName'] = "Detect Language"

        win = Win()
        win.mainloop()
    except SystemExit:
        sys.exit()
    except Exception as e:
        __location__ = os.path.dirname(os.path.realpath(__file__))
        print(__location__)
        print(e)
        traceback.print_exc()
