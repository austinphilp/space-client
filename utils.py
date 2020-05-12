import math
import socket
from time import time

from vectors import Vector


def inv_vector(vector):
    return Vector(
        -vector.x,
        -vector.y,
        -vector.z,
    )


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


def rotate_vector(vec, orientation, anti=False):
    # Rotate by Roll
    roll = orientation['roll_radians']
    yaw = orientation['yaw_radians']
    pitch = orientation['pitch_radians']
    vec = round_point(vec.rotate(-roll if anti else roll, (1, 0, 0)))
    # Rotate by Pitch
    vec = round_point(vec.rotate(-pitch if anti else pitch, (0, 1, 0)))
    # Rotate by Yaw
    vec = round_point(vec.rotate(-yaw if anti else yaw, (0, 0, 1)))
    return vec


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


def send_command(command_name, object_id, *args, port=None):
    # TODO(Austin) - Refactor to send multiple commands over a single
    # connection
    if port is None:
        port = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        port.connect("/home/austin/uds_socket")
    port.send(
        # TODO(Austin) - Dynamically decide system decoding
        bytes(object_id or "", "utf-8").ljust(8, b"\0")
        + bytes(command_name, "utf-8").ljust(24, b"\0")
        + bytes(','.join(str(a) for a in args), "utf-8").ljust(224, b"\0")
    )
    command_id = port.recv(8).decode().rstrip("\0")  # noqa
    payload_len = int(port.recv(8).decode().rstrip("\0"))
    payload = b""
    while payload_len > 0:
        payload += port.recv(1024 if payload_len >= 1024 else payload_len)
        payload_len -= 1024
    port.close()
    return payload.decode()


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
