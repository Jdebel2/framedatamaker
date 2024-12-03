from graphics import Window, FDMButton, ButtonFunction
from editor import Editor

def main():
    win = Window(800, 600)
    editor = Editor(win)
    btn = FDMButton('New', 20, 20, 6, 1, ButtonFunction.NEW, win, editor=editor)
    btn.draw()
    btnSave = FDMButton('Save', 80, 20, 6, 1, ButtonFunction.SAVE, win, editor=editor)
    btnSave.draw()
    win.mainloop()

if __name__ == '__main__':
    main()