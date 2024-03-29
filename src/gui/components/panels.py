from tkinter import filedialog

import customtkinter as ctk

from src.settings import *


class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=DARK_GREY)
        self.pack(fill='x', pady=4, ipady=8)


class SliderPanel(Panel):
    def __init__(self, parent, text, var, min_value, max_value):
        super().__init__(parent=parent)

        # layout
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.data_var = var
        self.data_var.trace('w', self.update_text)

        ctk.CTkLabel(self, text=text).grid(column=0, row=0, sticky='W', padx=5)
        self.num_label = ctk.CTkLabel(self, text=var.get())
        self.num_label.grid(column=1, row=0, sticky='E', padx=5)
        ctk.CTkSlider(self, fg_color=SLIDER_BG,
                      button_color=PURPLE,
                      button_hover_color=DARK_PURPLE,
                      variable=self.data_var,
                      from_=min_value,
                      to=max_value).grid(row=1, column=0, columnspan=2, sticky='ew',
                                         padx=5, pady=5)

    def update_text(self, *args):
        self.num_label.configure(text=f'{round(self.data_var.get(), 2)}')


class SegmentedPanel(Panel):
    def __init__(self, parent, text, var, options):
        super().__init__(parent=parent)
        ctk.CTkLabel(self, text=text).pack()
        ctk.CTkSegmentedButton(self, variable=var, values=options, selected_color=PURPLE,
                               selected_hover_color=DARK_PURPLE, unselected_hover_color=DARK_PURPLE).pack(expand=True,
                                                                                                          fill='both',
                                                                                                          padx=4,
                                                                                                          pady=4)


class SwitchPanel(Panel):
    def __init__(self, parent, *args):
        super().__init__(parent=parent)

        for var, text in args:
            s = ctk.CTkSwitch(self, text=text, variable=var, progress_color=DARK_PURPLE, button_color=PURPLE, fg_color=SLIDER_BG)
            s.pack(side='left', expand=True, fill='both', padx=5, pady=5)


class DropdownPanel(ctk.CTkOptionMenu):
    def __init__(self, parent, var, options):
        super().__init__(master=parent,
                         values=options,
                         fg_color=DARK_GREY,
                         button_color=DROPDOWN_MAIN_COLOR,
                         button_hover_color=DROPDOWN_HOVER_COLOR,
                         dropdown_fg_color=DROPDOWN_MENU_COLOR,
                         variable=var)
        self.pack(fill='x', pady=4)


class RevertButton(ctk.CTkButton):
    def __init__(self, parent, *args):
        super().__init__(master=parent, text='Deshacer Todo', fg_color=PURPLE, hover_color=DARK_PURPLE, command=self.revert)
        self.pack(side='bottom', pady=10)
        self.args = args

    def revert(self):
        for var, value in self.args:
            var.set(value)


class FileNamePanel(Panel):
    def __init__(self, parent, name_string, file_string):
        super().__init__(parent=parent)

        self.file_string = file_string
        self.file_string.trace('w', self.update_text)
        self.name_string = name_string
        self.name_string.trace('w', self.update_text)

        ctk.CTkEntry(self, textvariable=self.name_string, placeholder_text='Nombre de la Imagen').pack(fill='x',
                                                                                                       padx=20, pady=5)
        frame = ctk.CTkFrame(self, fg_color='transparent')
        png_check = ctk.CTkCheckBox(frame, text='png', hover_color=DARK_PURPLE, fg_color=PURPLE, variable=self.file_string, onvalue='png', offvalue='jpg',
                                    command=lambda: self.click('png'))
        jpg_check = ctk.CTkCheckBox(frame, text='jpg', hover_color=DARK_PURPLE, fg_color=PURPLE, variable=self.file_string, onvalue='jpg', offvalue='png',
                                    command=lambda: self.click('jpg'))
        png_check.pack(side='left', fill='x', expand=True)
        jpg_check.pack(side='left', fill='x', expand=True)
        frame.pack(expand=True, fill='x', padx=20)

        self.output = ctk.CTkLabel(self, text='')
        self.output.pack()

    def click(self, value):
        self.file_string.set(value)

    def update_text(self, *args):
        if self.name_string.get():
            text = self.name_string.get().replace(' ', '_') + '.' + self.file_string.get()
            self.output.configure(text=text)
        else:
            self.output.configure(text='')


class FilePathPanel(Panel):
    def __init__(self, parent, path_string):
        super().__init__(parent=parent)

        self.path_string = path_string

        ctk.CTkButton(self, text='Ubicación de la Imagen', fg_color=PURPLE, hover_color=DARK_PURPLE, command=self.open_file_dialog).pack(pady=5)
        self.label = ctk.CTkLabel(self, text='')
        self.label.pack(expand=True, fill='both', padx=5, pady=5)

    def open_file_dialog(self):
        self.path_string.set(filedialog.askdirectory(title='Seleccione el directorio de salida'))
        self.label.configure(text=self.path_string.get())


class SaveButton(ctk.CTkButton):
    def __init__(self, parent, export, name_string, file_string, path_string):
        super().__init__(master=parent, text='Exportar', fg_color=PURPLE, hover_color=DARK_PURPLE, command=self.save)
        self.pack(side='bottom', pady=10)

        self.export = export
        self.file = file_string
        self.path = path_string
        self.name = name_string

    def save(self):
        self.export(self.name.get(), self.file.get(), self.path.get())
