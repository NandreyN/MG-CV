import tkinter
import discrete_utils
from PIL import Image, ImageTk, ImageDraw
from itertools import product

LMB_PRESS, GRAG_LMB_PRESSED, LMB_RELEASED = '<Button-1>', '<B1-Motion>', '<ButtonRelease-1>'

class ImageProvider():
    IMAGE_SIZE = (500, 500)
    IMAGE_CELLS = (30, 30)

    def __init__(self):
        self.__img = Image.new('RGB', self.IMAGE_CELLS, color='white')
        self.per_cell_x, self.per_cell_y = discrete_utils.abs_to_grid_ratio(
            self.IMAGE_CELLS,
            self.IMAGE_SIZE
        ) 

    def get_image(self, resize=True):
        return self.__img
    
class GridImageProvider(ImageProvider):
    def __init__(self):
        super().__init__()
        self.__drawer = ImageDraw.Draw(self.get_image(resize=False))

    def transform_coords_to_grid(self, absolute_coords):
        return discrete_utils.absolute_to_grid(
            (self.per_cell_x, self.per_cell_y),
            absolute_coords
        )


    def get_drawer(self):
        return self.__drawer

    
    def get_image(self, resize=True):
        return (
            super().get_image().resize(self.IMAGE_SIZE, Image.NEAREST)
            if resize else
            super().get_image()
        )


class GridUndoableImageProvider(GridImageProvider):
    def __init__(self):
        super().__init__()
        self.__points_queue = []

    def add_to_storage(self, *point):
        self.__points_queue.append(*point)

    def undo(self):
        for p in self.__points_queue:
            super().get_drawer().point(p, fill='white')

    def clear_storage(self):
        self.__points_queue.clear()

    def storage_generator(self):
        yield from self.__points_queue


class LabFrame():
    def __init__(self, frame_title, image_repo, master):
        if not isinstance(image_repo, ImageProvider):
            raise TypeError('image_repo must inherit ImageProvider class')

        master.winfo_toplevel().title(frame_title)
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

        
def get_frame(frame_title, image_keeper):
    return LabFrame(frame_title, image_keeper, tkinter.Tk())
