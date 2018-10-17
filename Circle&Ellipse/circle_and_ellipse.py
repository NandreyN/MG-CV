from sys import path
from PIL import Image, ImageDraw
from numpy.linalg import norm
from math import sqrt, cos, sin, pi
path.append('..')
import skeleton
import discrete_utils

class CircleDrawer(skeleton.GridImageProvider):
    def __init__(self):
        super().__init__()
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
            super().get_drawer().point(p, fill='black')


    def undo_last_call(self):
        if self.__points_queue:
            for p in self.__points_queue:
                super().get_drawer().point(p, fill='white')


class EllipseDrawer(skeleton.GridImageProvider):
    def __init__(self):
        super().__init__()
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
        self.__centre = super().transform_coords_to_grid(centre)
        if release_buff_points:
            self.__points_queue.clear()

    def draw_ellipse_interactive(self, clicked_point, undo_last):
        clicked_point = super().transform_coords_to_grid(clicked_point)
        
        if undo_last:
            self.undo_last_call()

        v = discrete_utils.sub(clicked_point, self.__centre)
        v = (v[0] * 0.5, v[1] * 0.5)

        middle_point = discrete_utils.add(self.__centre, v)
        self.__draw_ellipse(middle_point, int(abs(v[0])), int(abs(v[1])))


    def __draw_ellipse(self, centre, A, B):
        if any([A == 0, B == 0]):
            return

        A2, B2 = A**2, B**2
        fa2, fb2 = 4 * A2, 4 * B2
        x, y, sigma = 0, B, 2 * B2 + A2 *(1 - 2*B)
        self.__points_queue.clear()

        self.__points_queue.append((x, y))
        self.__points_queue.append((-x, -y))
        self.__points_queue.append((-x, y))
        self.__points_queue.append((x, -y))

        while B2 * x <= A2 * y:
            self.__points_queue.append((x, y))
            self.__points_queue.append((-x, -y))
            self.__points_queue.append((-x, y))
            self.__points_queue.append((x, -y))
            if sigma >= 0:
                sigma += fa2 * (1 - y)
                y -= 1
            sigma += B2 * (4*x + 6)
            x += 1

        x, y, sigma = A, 0, 2 * A2 + B2 * (1 - 2*A)


        self.__points_queue.append((x, y))
        self.__points_queue.append((-x, -y))
        self.__points_queue.append((-x, y))
        self.__points_queue.append((x, -y))

        while A2 * y <= B2 * x:
            self.__points_queue.append((x, y))
            self.__points_queue.append((-x, -y))
            self.__points_queue.append((-x, y))
            self.__points_queue.append((x, -y))
            if sigma >= 0:
                sigma += fb2 * (1 - x)
                x -= 1
            sigma += A2 * (4 * y + 6)
            y += 1

        
        self.__points_queue = list(map(lambda x : discrete_utils.add(x, centre), self.__points_queue))
        for p in self.__points_queue:
            super().get_drawer().point(p, fill='black')


    def undo_last_call(self):
        if self.__points_queue:
            for p in self.__points_queue:
                super().get_drawer().point(p, fill='white')


def call_circle_drawer_window():

    def start_new_circle_handler(event):
        circle_drawer.init_drawing((event.x, event.y))


    def redraw_circle_border_on_moving(event):
        circle_drawer.draw_circle_interactive((event.x, event.y), True)


    def finish_circle_drawing(event):
        circle_drawer.draw_circle_interactive((event.x, event.y), False)


    circle_drawer = CircleDrawer()
    lab_frame = skeleton.get_frame('Circles', circle_drawer)
    lab_frame.bind_handlers(
        keys_set=[skeleton.LMB_PRESS, skeleton.GRAG_LMB_PRESSED, skeleton.LMB_RELEASED],
        handle_funcs=[
            start_new_circle_handler ,
            redraw_circle_border_on_moving ,
            finish_circle_drawing
        ]
    )
    lab_frame.start()


def call_ellipse_drawer_window():

    def start_new_ellipse_handler(event):
        ellipse_drawer.init_drawing((event.x, event.y))


    def redraw_ellipse_border_on_moving(event):
        ellipse_drawer.draw_ellipse_interactive((event.x, event.y), True)


    def finish_ellipse_drawing(event):
        ellipse_drawer.draw_ellipse_interactive((event.x, event.y), False)


    ellipse_drawer = EllipseDrawer()
    lab_frame = skeleton.get_frame('Ellipse', ellipse_drawer)
    lab_frame.bind_handlers(
        keys_set=[skeleton.LMB_PRESS, skeleton.GRAG_LMB_PRESSED, skeleton.LMB_RELEASED],
        handle_funcs=[
            start_new_ellipse_handler ,
            redraw_ellipse_border_on_moving,
            finish_ellipse_drawing
        ]
    )
    lab_frame.start()


if __name__ == '__main__':
    call_ellipse_drawer_window()