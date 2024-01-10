import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps

from src.code.settings import *
from src.gui.components.close_output import CloseOutput
from src.gui.components.import_image import ImportImage
from src.gui.components.menu import Menu
from src.gui.components.output_image import OutputImage


class App(ctk.CTk):
    def __init__(self):
        # setup
        super().__init__()
        self.init_parameters()
        ctk.set_appearance_mode('dark')
        self.geometry('1100x600+30+30')
        self.title('PyImageEditor')
        self.minsize(800, 500)

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')

        # canvas_data
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0

        # widgets
        self.image_import = ImportImage(self, self.import_image)

        # run
        self.mainloop()

    def import_image(self, path):
        self.original = Image.open(path)
        self.image = self.original
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_ratio = self.image.size[0] / self.image.size[1]

        self.image_import.grid_forget()
        self.image_output = OutputImage(self, self.resize_image)
        self.close_button = CloseOutput(self, self.close_edit)
        self.menu = Menu(self, self.pos_vars, self.color_vars, self.effect_vars)

    def init_parameters(self):
        self.pos_vars = {
            'rotate': ctk.DoubleVar(value=ROTATE_DEFAULT),
            'zoom': ctk.DoubleVar(value=ZOOM_DEFAULT),
            'flip': ctk.StringVar(value=FLIP_OPTIONS[0])
        }

        self.color_vars = {
            'brightness': ctk.DoubleVar(value=BRIGHTNESS_DEFAULT),
            'grayscale': ctk.BooleanVar(value=GRAYSCALE_DEFAULT),
            'sepia': ctk.BooleanVar(value=SEPIA_DEFAULT),
            'invert': ctk.BooleanVar(value=INVERT_DEFAULT),
            'vibrance': ctk.DoubleVar(value=VIBRANCE_DEFAULT),
            'tone': ctk.DoubleVar(value=TONE_DEFAULT),
            'calidez': ctk.DoubleVar(value=CALIDEZ_DEFAULT)
        }

        self.effect_vars = {
            'blur': ctk.DoubleVar(value=BLUR_DEFAULT),
            'contrast': ctk.IntVar(value=CONTRAST_DEFAULT),
            'clarity': ctk.DoubleVar(value=CLARITY_DEFAULT),
            'filter': ctk.StringVar(value=FILTER_OPTIONS[0]),
            'effect': ctk.StringVar(value=EFFECT_OPTIONS[0])
        }

        for var in list(self.pos_vars.values()) + list(self.color_vars.values()) + list(self.effect_vars.values()):
            var.trace('w', self.manipulate_image)

    def manipulate_image(self, *args):
        self.image = self.original

        # rotate
        self.image = self.image.rotate(self.pos_vars.get('rotate').get())

        # zoom
        self.image = ImageOps.crop(self.image, border=self.pos_vars.get('zoom').get())

        self.place_image()

    def resize_image(self, event):
        canvas_ratio = event.width / event.height

        self.canvas_width = event.width
        self.canvas_height = event.height

        if canvas_ratio > self.image_ratio:
            self.image_height = int(event.height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(event.width)
            self.image_height = int(self.image_width / self.image_ratio)
        self.place_image()

    def place_image(self, ):
        self.image_output.delete('all')
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk)

    def close_edit(self):
        self.init_parameters()
        self.image_output.grid_forget()
        self.close_button.place_forget()
        self.menu.grid_forget()
        self.image_import = ImportImage(self, self.import_image)


if __name__ == '__main__':
    App()
