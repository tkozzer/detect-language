from window import Win
import sys
if __name__ == "__main__":
    try:
        win = Win()
        win.mainloop()
    except SystemExit:
        sys.exit()
    except Exception as e:
        print(e)