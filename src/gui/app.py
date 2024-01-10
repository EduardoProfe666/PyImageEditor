from tkinter import messagebox

import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter

from src.settings import *
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
        self.menu = Menu(self, self.pos_vars, self.color_vars, self.effect_vars, self.export_image)

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
        }

        self.effect_vars = {
            'blur': ctk.DoubleVar(value=BLUR_DEFAULT),
            'contrast': ctk.IntVar(value=CONTRAST_DEFAULT),
            'clarity': ctk.DoubleVar(value=CLARITY_DEFAULT),
            'effect': ctk.StringVar(value=EFFECT_OPTIONS[0])
        }

        for var in list(self.pos_vars.values()) + list(self.color_vars.values()) + list(self.effect_vars.values()):
            var.trace('w', self.manipulate_image)

    def manipulate_image(self, *args):
        self.image = self.original

        # rotate
        if self.pos_vars['rotate'].get() != ROTATE_DEFAULT:
            self.image = self.image.rotate(self.pos_vars.get('rotate').get())

        # zoom
        if self.pos_vars['zoom'].get() != ZOOM_DEFAULT:
            self.image = ImageOps.crop(self.image, border=self.pos_vars.get('zoom').get() * 3)

        # flip
        if self.pos_vars['flip'].get() != FLIP_OPTIONS[0]:
            if self.pos_vars.get('flip').get() == 'X':
                self.image = ImageOps.mirror(self.image)
            elif self.pos_vars.get('flip').get() == 'Y':
                self.image = ImageOps.flip(self.image)
            elif self.pos_vars.get('flip').get() == 'Ambos':
                self.image = ImageOps.mirror(self.image)
                self.image = ImageOps.flip(self.image)

        # brightness & vibrance
        if self.color_vars['brightness'].get() != BRIGHTNESS_DEFAULT:
            self.image = ImageEnhance.Brightness(self.image).enhance(self.color_vars['brightness'].get())
        if self.color_vars['vibrance'].get() != VIBRANCE_DEFAULT:
            self.image = ImageEnhance.Color(self.image).enhance(self.color_vars['vibrance'].get())

        # grayscale & invert & sepia
        if self.color_vars['grayscale'].get():
            self.image = ImageOps.grayscale(self.image)

        if self.color_vars['invert'].get():
            self.image = ImageOps.invert(self.image)

        if self.color_vars['sepia'].get():
            palette = []
            r, g, b = (255, 240, 192)
            for i in range(255):
                palette.extend((r * i // 255, g * i // 255, b * i // 255))
            self.image = self.image.convert('L')
            self.image.putpalette(palette)

        # blur & contrast & claridad
        if self.effect_vars['blur'] != BLUR_DEFAULT:
            self.image = self.image.filter(ImageFilter.GaussianBlur(self.effect_vars['blur'].get()))
        if self.effect_vars['contrast'] != CONTRAST_DEFAULT:
            self.image = self.image.filter(ImageFilter.UnsharpMask(self.effect_vars['contrast'].get()))
        if self.effect_vars['clarity'] != CLARITY_DEFAULT:
            self.image = ImageEnhance.Sharpness(self.image).enhance(self.effect_vars['clarity'].get())

        # effects
        if self.effect_vars['effect'] != EFFECT_OPTIONS[0]:
            match self.effect_vars['effect'].get():
                case 'Emboss':
                    self.image = self.image.filter(ImageFilter.EMBOSS)
                case 'Bordes Find':
                    self.image = self.image.filter(ImageFilter.FIND_EDGES)
                case 'Contour':
                    self.image = self.image.filter(ImageFilter.CONTOUR)
                case 'Bordes Enhance':
                    self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
                case 'Bordes Enhance+':
                    self.image = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)
                case 'Blur':
                    self.image = self.image.filter(ImageFilter.BLUR)
                case 'Detalles':
                    self.image = self.image.filter(ImageFilter.DETAIL)
                case 'Nítido':
                    self.image = self.image.filter(ImageFilter.SHARPEN)
                case 'Suave':
                    self.image = self.image.filter(ImageFilter.SMOOTH)
                case 'Suave+':
                    self.image = self.image.filter(ImageFilter.SMOOTH_MORE)

        # filters

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

    def export_image(self, name, file, path):
        try:
            print(name)
            if not name:
                messagebox.showerror('Nombre no válido', 'Introduzca un nombre válido')
            elif path == '':
                messagebox.showerror('Ruta no válida', 'Introduzca una ruta válida')
            else:
                export_string = f'{path}/{name}.{file}'
                self.image.save(export_string)
                messagebox.showinfo('Exportación con Éxito',
                                    'Se exportó la imagen correctamente en la ruta: ' + export_string)
                Image.open(export_string).show(name)
        except Exception:
            messagebox.showerror('Exportación Fallida',
                                 'Fallo durante la exportación de la imagen. Vuelva a intentarlo')


if __name__ == '__main__':
    App()
