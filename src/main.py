from graphics import Window, Sprite
from tkinter import *

def main():
    win = Window(800, 600)
    spr = Sprite('assets/test_sprite.png', 100, 100, win)
    spr.draw()
    win.wait_for_close()

if __name__ == '__main__':
    main()