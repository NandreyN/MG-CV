from sys import path
from PIL import Image, ImageDraw
from numpy.linalg import norm
from math import sqrt, cos, sin, pi
path.append('..')
import skeleton

class CircleDrawer(skeleton.ImageProvider):
    def __init__(self):
        super().__init__()
        self.__drawer = ImageDraw.Draw(self.get_image(resize=False))

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


    def set_centre(self, centre):
        self.__centre = (centre[0] // self.per_cell_x,  centre[1] // self.per_cell_y)


    def draw_circle_interactive(self, clicked_point):
        clicked_point = (clicked_point[0] // self.per_cell_x, clicked_point[1] // self.per_cell_y)
        r = sqrt((clicked_point[0] - self.__centre[0]) ** 2 + (clicked_point[1] - self.__centre[1])**2)
        self.__draw_circle(self.__centre, int(r))


    def __draw_circle(self, centre, radius):
        

        def transform_coordinates(to_transform):
            return (self.__centre[0] + to_transform[0], self.__centre[1] + to_transform[1])


        def process_vars(d, u, v, x, y):
            return (
                (d + u, u + 4, v + 4, x + 1, y)
                if d < 0 else
                (d + v, u + 4, v + 8, x + 1, y + 1)
            )

        x, y = 0, -radius
        d, u, v = 3 - 2 * radius, 6, 10 - 4 * radius
        points_queue = []

        while v <= 10:
            for coord_pair in self.__symmetric_transform((x,y)):
                points_queue.append(coord_pair)
            d, u, v, x, y = process_vars(d, u, v, x, y)

        for p in points_queue:
            self.__drawer.point(transform_coordinates(p), fill='black')
        

if __name__ == '__main__':
    circle_drawer = CircleDrawer()
    lab_frame = skeleton.get_frame(circle_drawer)
    lab_frame.bind_handlers(
        keys_set=[skeleton.LMB_PRESS, skeleton.LMB_RELEASED],
        handle_funcs=[
            lambda event : circle_drawer.set_centre((event.x, event.y)),
            lambda event : circle_drawer.draw_circle_interactive((event.x, event.y))
        ]
    )
    lab_frame.start()