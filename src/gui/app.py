import customtkinter as ctk
from PIL import Image, ImageTk

from src.gui.components.close_output import CloseOutput
from src.gui.components.import_image import ImportImage
from src.gui.components.output_image import OutputImage


class App(ctk.CTk):
    def __init__(self):
        # setup
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.geometry('1000x600+30+30')
        self.title('PyImageEditor')
        self.minsize(800, 500)

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=6)

        # widgets
        self.image_import = ImportImage(self, self.import_image)

        # run
        self.mainloop()

    def import_image(self, path):
        self.image = Image.open(path)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_ratio = self.image.size[0] / self.image.size[1]

        self.image_import.grid_forget()
        self.image_output = OutputImage(self, self.resize_image)
        self.close_button = CloseOutput(self, self.close_edit)

    def resize_image(self, event):
        canvas_ratio = event.width / event.height
        image_width = 0
        image_height = 0
        if canvas_ratio > self.image_ratio:
            image_height = int(event.height)
            image_width = int(image_height * self.image_ratio)
        else:
            image_width = int(event.width)
            image_height = int(image_width / self.image_ratio)
        self.image_output.delete('all')
        resized_image = self.image.resize((image_width, image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(event.width / 2, event.height / 2, image = self.image_tk)

    def close_edit(self):
        self.image_output.grid_forget()
        self.close_button.place_forget()
        self.image_import = ImportImage(self, self.import_image)


if __name__ == '__main__':
    App()
