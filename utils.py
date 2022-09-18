from time import time

from vectors import Vector


def inv_vector(vector):
    return Vector(
        -vector.x,
        -vector.y,
        -vector.z,
    )


def vector_from_proto(vector):
    return Vector(
        vector.x,
        vector.y,
        vector.z,
    )


def print_vector(vector):
    return f"({vector.x:.2f}, {vector.y:.2f}, {vector.z:.2f})"


def thrust_vector(vector):
    if vector.x >= 0:
        vector.x = min(vector.x, 1)
    else:
        vector.x = max(vector.x, -1)
    if vector.y >= 0:
        vector.y = min(vector.y, 1)
    else:
        vector.y = max(vector.y, -1)
    if vector.z >= 0:
        vector.z = min(vector.z, 1)
    else:
        vector.z = max(vector.z, -1)
    return vector


def deg_to_rad(deg):
    return deg * 0.0174533


def dict_to_vector(vec_dict):
    return Vector(vec_dict['x'], vec_dict['y'], vec_dict['z'])


def round_point(point):
    point.x = round(point.x, 4)
    point.y = round(point.y, 4)
    point.z = round(point.z, 4)
    return point


def coord_equals(coord_1, coord_2):
    return (
        round(coord_1['x'], 3) == round(coord_2['x'], 3)
        and round(coord_1['y'], 3) == round(coord_2['y'], 3)
        and round(coord_1['z'], 3) == round(coord_2['z'], 3)
    )


class throttle(object):
    THROTTLE = 0.25

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        self.obj = obj
        return self

    def __call__(self, *args, **kwargs):
        tracker_name = F"_{self.func.__name__}_last_ran_on"
        # calling object will either be self.obj (if called as method) or
        # args[0] if called from within an @property decorator
        obj = getattr(self, 'obj', None) or args[0]
        if getattr(obj, tracker_name, 0) + self.THROTTLE <= time():
            setattr(obj, tracker_name, time())
            if len(args) == 0 or args[0] != obj:
                args = (obj, *args)
            return self.func(*args, **kwargs)
