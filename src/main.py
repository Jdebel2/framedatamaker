from graphics import Window, FDMImage, FDMButton, ButtonFunction
from tkinter import *

def main():
    win = Window(800, 600)
    spr = FDMImage('assets/test_sprite.png', 100, 100, win)
    spr.draw()
    btn = FDMButton('New', 20, 20, 6, 1, ButtonFunction.NEW, win)
    btn.draw()
    win.wait_for_close()

if __name__ == '__main__':
    main()