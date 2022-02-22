import sys
import traceback
from window import Win
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
        print(e)
        traceback.print_exc()
