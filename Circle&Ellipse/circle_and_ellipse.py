from sys import path
from PIL import Image, ImageDraw
from numpy.linalg import norm
from math import sqrt, cos, sin, pi
path.append('..')
import skeleton
import discrete_utils

class CircleDrawer(skeleton.ImageProvider):
    def __init__(self):
        super().__init__()
        self.__drawer = ImageDraw.Draw(self.get_image(resize=False))
        self.__points_queue = []

    def __symmetric_transform(self, point_to_rotate):
        x, y = point_to_rotate
        return [
            (x, -y),
            (y, -x),
            (y, x),
            (x, y),
            (-x, y),
            (-y, x),
            (-y, -x),
            (-x, -y),
        ]


    def init_drawing(self, centre, release_buff_points=True):
        self.__centre = self.transform_coords_to_grid(centre)
        if release_buff_points:
            self.__points_queue.clear()

    def draw_circle_interactive(self, clicked_point, undo_last):
        clicked_point = self.transform_coords_to_grid(clicked_point)
        r = sqrt((clicked_point[0] - self.__centre[0]) ** 2 + (clicked_point[1] - self.__centre[1])**2)
        if undo_last:
            self.undo_last_call()
        self.__draw_circle(self.__centre, int(r))


    def __draw_circle(self, centre, radius):
        

        def process_vars(d, u, v, x, y):
            return (
                (d + u, u + 4, v + 4, x + 1, y)
                if d < 0 else
                (d + v, u + 4, v + 8, x + 1, y + 1)
            )

        x, y = 0, -radius
        d, u, v = 3 - 2 * radius, 6, 10 - 4 * radius
        self.__points_queue.clear()

        while v <= 10:
            for coord_pair in self.__symmetric_transform((x,y)):
                self.__points_queue.append(coord_pair)
            d, u, v, x, y = process_vars(d, u, v, x, y)

        self.__points_queue = list(map(lambda x : discrete_utils.add(x, self.__centre), self.__points_queue))
        for p in self.__points_queue:
            self.__drawer.point(p, fill='black')


    def undo_last_call(self):
        if self.__points_queue:
            for p in self.__points_queue:
                self.__drawer.point(p, fill='white')

        super().undo_last_call()


def start_new_circle_handler(event):
    global circle_drawer
    circle_drawer.init_drawing((event.x, event.y))


def redraw_circle_border_on_moving(event):
    global circle_drawer
    circle_drawer.draw_circle_interactive((event.x, event.y), True)


def finish_circle_drawing(event):
    global circle_drawer
    circle_drawer.draw_circle_interactive((event.x, event.y), False)

if __name__ == '__main__':
    circle_drawer = CircleDrawer()
    lab_frame = skeleton.get_frame(circle_drawer)
    lab_frame.bind_handlers(
        keys_set=[skeleton.LMB_PRESS, skeleton.GRAG_LMB_PRESSED, skeleton.LMB_RELEASED],
        handle_funcs=[
            start_new_circle_handler ,
            redraw_circle_border_on_moving ,
            finish_circle_drawing
        ]
    )
    lab_frame.start()