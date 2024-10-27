from graphics import Window, FDMImage, FDMButton, ButtonFunction

def main():
    win = Window(800, 600)
    btn = FDMButton('New', 20, 20, 6, 1, ButtonFunction.NEW, win)
    btn.draw()
    win.mainloop()

if __name__ == '__main__':
    main()