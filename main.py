from window import Win
if __name__ == "__main__":
    try:
        win = Win()
        win.mainloop()
    except SystemExit:
        pass
    except Exception as e:
        print(e)