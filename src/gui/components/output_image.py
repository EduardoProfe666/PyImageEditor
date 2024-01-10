from tkinter import Canvas

from src.code.settings import BACKGROUND_COLOR


class OutputImage(Canvas):
    def __init__(self, parent, resize_image):
        super().__init__(master=parent, background=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief='ridge')
        self.grid(row=0, column=1, sticky='nsew')
        self.bind('<Configure>', resize_image)
