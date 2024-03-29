import customtkinter as ctk
from tkinter import filedialog

from src.settings import PURPLE, DARK_PURPLE


class ImportImage(ctk.CTkFrame):
    def __init__(self, parent, import_function):
        super().__init__(master=parent)
        self.grid(column=0, row=0, columnspan=2, sticky='nsew')
        self.import_func = import_function

        ctk.CTkButton(self, text='Abrir Imagen', command=self.open_dialog,
                      fg_color=PURPLE, hover_color=DARK_PURPLE).pack(expand=True)

    def open_dialog(self):
        path = filedialog.askopenfile(title='Seleccione la imagen deseada',
                                      filetypes=[("Imágenes", ["*.png", '*.jpg', '*.jpeg', '*.gif'])]).name
        self.import_func(path)
