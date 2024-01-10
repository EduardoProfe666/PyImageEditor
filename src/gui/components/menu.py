import customtkinter as ctk

from src.settings import *
from src.gui.components.panels import SliderPanel, SegmentedPanel, SwitchPanel, DropdownPanel, RevertButton, \
    FileNamePanel


class Menu(ctk.CTkTabview):
    def __init__(self, parent, pos_vars, color_vars, effect_vars):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky="nsew", pady=10, padx=10)

        # tabs
        self.add('Posición')
        self.add('Colores')
        self.add('Efectos')
        self.add('Exportar')

        # widgets
        PositionFrame(self.tab('Posición'), pos_vars.get('rotate'), pos_vars.get('zoom'), pos_vars.get('flip'))
        ColorFrame(self.tab('Colores'), color_vars)
        EffectFrame(self.tab('Efectos'), effect_vars)
        ExportFrame(self.tab('Exportar'))


class PositionFrame(ctk.CTkFrame):
    def __init__(self, parent, rotation, zoom, invert):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill="both")

        SliderPanel(self, 'Rotación', rotation, -180, 180)
        SliderPanel(self, 'Zoom', zoom, 0, 100)
        SegmentedPanel(self, 'Inversión', invert, FLIP_OPTIONS)
        RevertButton(self,
                     (rotation, ROTATE_DEFAULT),
                     (zoom, ZOOM_DEFAULT),
                     (invert, FLIP_OPTIONS[0]))


class ColorFrame(ctk.CTkFrame):
    def __init__(self, parent, color_vars):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill="both")

        SwitchPanel(self, (color_vars['grayscale'], 'B/N'), (color_vars['invert'], 'Invertir'))
        SwitchPanel(self, (color_vars['sepia'], 'Sepia'))
        SliderPanel(self, 'Brillo', color_vars.get('brightness'), 0, 10)
        SliderPanel(self, 'Saturación', color_vars.get('vibrance'), -10, 10)
        RevertButton(self,
                     (color_vars['grayscale'], GRAYSCALE_DEFAULT),
                     (color_vars['sepia'], SEPIA_DEFAULT),
                     (color_vars['invert'], INVERT_DEFAULT),
                     (color_vars.get('brightness'), BRIGHTNESS_DEFAULT),
                     (color_vars.get('vibrance'), VIBRANCE_DEFAULT))


class EffectFrame(ctk.CTkFrame):
    def __init__(self, parent, effect_vars):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill="both")

        DropdownPanel(self, effect_vars['effect'], EFFECT_OPTIONS)
        DropdownPanel(self, effect_vars['filter'], FILTER_OPTIONS)
        SliderPanel(self, 'Blur', effect_vars.get('blur'), 0, 50)
        SliderPanel(self, 'Contraste', effect_vars.get('contrast'), 0, 5)
        SliderPanel(self, 'Nitidez', effect_vars.get('clarity'), 0, 10)
        RevertButton(self,
                     (effect_vars['effect'], EFFECT_OPTIONS[0]),
                     (effect_vars['filter'], FILTER_OPTIONS[0]),
                     (effect_vars.get('blur'), BLUR_DEFAULT),
                     (effect_vars.get('contrast'), CONTRAST_DEFAULT),
                     (effect_vars.get('clarity'), CLARITY_DEFAULT))


class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill="both")

        # data
        self.name_string = ctk.StringVar()
        self.file_string = ctk.StringVar(value='png')

        # widgets
        FileNamePanel(self, self.name_string, self.file_string)
