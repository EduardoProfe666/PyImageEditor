import customtkinter as ctk

from src.gui.components.panels import Panel, SliderPanel


class Menu(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky="nsew")

        # tabs
        self.add('Posición')
        self.add('Colores')
        self.add('Efectos')
        self.add('Exportar')

        # widgets
        PositionFrame(self.tab('Posición'))
        ColorFrame(self.tab('Colores'))
        EffectFrame(self.tab('Efectos'))
        ExportFrame(self.tab('Exportar'))


class PositionFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill="both")

        SliderPanel(self, 'Rotación')
        SliderPanel(self, 'Zoom')


class ColorFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill="both")


class EffectFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill="both")


class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill="both")
