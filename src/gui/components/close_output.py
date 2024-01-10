import customtkinter as ctk

from src.code.settings import WHITE, CLOSE_RED


class CloseOutput(ctk.CTkButton):
    def __init__(self, parent, func):
        super().__init__(master=parent,
                         command = func,
                         text='Olvidar Imagen',
                         text_color=WHITE,
                         fg_color='transparent',
                         width=40,
                         height=40,
                         corner_radius=10,
                         hover_color=CLOSE_RED)
        self.place(relx=0.99, rely=0.01, anchor='ne')
