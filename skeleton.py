import tkinter
from PIL import Image, ImageTk

LMB_PRESS, GRAG_LMB_PRESSED, LMB_RELEASED = '<Button-1>', '<B1-Motion>', '<ButtonRelease-1>'

class ImageProvider():
    IMAGE_SIZE = (500, 500)
    IMAGE_CELLS = (40, 40)

    def __init__(self):
        self.__img = Image.new('RGB', self.IMAGE_CELLS, color='white')
        self.per_cell_x = self.IMAGE_SIZE[0] // self.IMAGE_CELLS[0]
        self.per_cell_y = self.IMAGE_SIZE[1] // self.IMAGE_CELLS[1]

    def get_image(self, resize=True):
        return (
            self.__img.resize(self.IMAGE_SIZE, Image.NEAREST)
            if resize else
            self.__img
        )


class LabFrame():
    def __init__(self, image_repo, master):
        if not isinstance(image_repo, ImageProvider):
            raise TypeError('image_repo must inherit ImageProvider class')

        self.__image_repo = image_repo
        image_pil = self.__extract_image()
        
        self.__master = master
        self.__image = image_pil
        self.__canvas = tkinter.Canvas(
            master,
            width = image_pil.size[0],
            height = image_pil.size[1]
        )
        self.__canvas.pack()

        master.image_tk = self.__image_tk = ImageTk.PhotoImage(self.__image)        
        self.__image_area = self.__canvas.create_image(
            self.__image.size[0] // 2,
            self.__image.size[1] // 2,
            image = self.__image_tk
        )
        self.__canvas.image = self.__image_tk
        
    
    def bind_handlers(self,keys_set, handle_funcs):
        for key, handler in zip(keys_set, handle_funcs):
            self.__canvas.bind(key, handler)
        
        self.__canvas.after(50, self.__update_canvas_image)

            
    def __extract_image(self):
        return self.__image_repo.get_image()

    
    def __reset_repo_image(self):
        self.__image_repo.reset_image()
    
    
    def __update_canvas_image(self):
        self.__image_tk = ImageTk.PhotoImage(self.__extract_image())
        self.__canvas.itemconfig(self.__image_area, image = self.__image_tk)
        self.__canvas.after(50, self.__update_canvas_image)


    def start(self):
        tkinter.mainloop()

        
def get_frame(image_keeper):
    return LabFrame(image_keeper, tkinter.Tk())
