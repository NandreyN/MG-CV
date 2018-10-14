import operator


def add(tuple1, tuple2):
    return tuple(map(operator.add, tuple1, tuple2)) 


def sub(tuple1, tuple2):
    return tuple(map(operator.sub, tuple1, tuple2))


def div(tuple1, tuple2):
    return tuple(map(operator.floordiv, tuple1, tuple2))


def mul(tuple1, tuple2):
    return tuple(map(operator.mul, tuple1, tuple2))


def abs_to_grid_ratio(grid_size, absolute_size):
    return div(absolute_size, grid_size)


def absolute_to_grid(abs_to_grid_rat, coordinate):
    return div(coordinate, abs_to_grid_rat)