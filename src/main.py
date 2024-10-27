from graphics import Window, FDMButton, ButtonFunction
from animation import Animation

def main():
    win = Window(800, 600)
    anim = Animation(win)
    btn = FDMButton('New', 20, 20, 6, 1, ButtonFunction.NEW, win, anim=anim)
    btn.draw()
    win.mainloop()

if __name__ == '__main__':
    main()