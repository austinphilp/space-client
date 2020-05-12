from time import sleep

from models.base import BaseRemoteObject
from models.components import (
    ReactionWheel,
    Reactor,
    Sensor,
    Thruster
)
from utils import coord_equals, rotate_vector, thrust_vector


class Ship(BaseRemoteObject):
    def get_reaction_wheel(self, axis, rotation):
        for wheel in self.reaction_wheels:
            if wheel.axis == axis and wheel.rotation == rotation:
                return wheel

    def get_thruster(self, direction):
        for thruster in self.thrusters:
            if thruster.direction == direction:
                return thruster

    def kill_throttle(self):
        for thruster in self.thrusters:
            thruster.throttle = 0

    def kill_rotational_throttle(self):
        for wheel in self.reaction_wheels:
            wheel.throttle = 0

    def apply_thrust_for_vector(self, vector, anti=True):
        vector = thrust_vector(
            rotate_vector(
                vector,
                self.orientation,
                anti=anti
            )
        )
        print(vector)
        if vector.x < 0:
            self.get_thruster("forward").throttle = 0
            self.get_thruster("aft").throttle = abs(vector.x)
        elif vector.x > 0:
            self.get_thruster("aft").throttle = 0
            self.get_thruster("forward").throttle = abs(vector.x)
        else:
            self.get_thruster("forward").throttle = 0
            self.get_thruster("aft").throttle = 0

        if vector.y < 0:
            self.get_thruster("starboard").throttle = 0
            self.get_thruster("port").throttle = abs(vector.y)
        elif vector.y > 0:
            self.get_thruster("port").throttle = 0
            self.get_thruster("starboard").throttle = abs(vector.y)
        else:
            self.get_thruster("port").throttle = 0
            self.get_thruster("starboard").throttle = 0

        if vector.z < 0:
            self.get_thruster("overhead").throttle = 0
            self.get_thruster("deck").throttle = abs(vector.z)
        elif vector.z > 0:
            self.get_thruster("deck").throttle = 0
            self.get_thruster("overhead").throttle = abs(vector.z)
        else:
            self.get_thruster("deck").throttle = 0
            self.get_thruster("overhead").throttle = 0

    def set_rotational_speed(self, pitch, roll, yaw, wait=True):
        moved = False
        yaw_speed, pitch_speed, roll_speed = (
            round(self.orientation_speed["yaw_speed"], 5),
            round(self.orientation_speed["pitch_speed"], 5),
            round(self.orientation_speed["roll_speed"], 5),
        )
        while yaw_speed != round(yaw, 5) \
                or pitch_speed != round(pitch, 5) \
                or roll_speed != round(roll, 5):
            yaw_discrepency = yaw - yaw_speed
            moved = True
            if yaw_discrepency > 0:
                self.get_reaction_wheel("yaw", "CW").throttle = min(
                    abs(yaw_discrepency),
                    1
                )
                self.get_reaction_wheel("yaw", "CCW").throttle = 0
            elif yaw_speed > yaw:
                self.get_reaction_wheel("yaw", "CCW").throttle = min(
                    abs(yaw_discrepency),
                    1
                )
                self.get_reaction_wheel("yaw", "CW").throttle = 0
            else:
                self.get_reaction_wheel("yaw", "CCW").throttle = 0
                self.get_reaction_wheel("yaw", "CW").throttle = 0

            pitch_discrepency = abs(pitch - pitch_speed)
            if pitch_speed < pitch:
                self.get_reaction_wheel("pitch", "CW").throttle = min(
                    abs(pitch_discrepency),
                    1
                )
                self.get_reaction_wheel("pitch", "CCW").throttle = 0
            elif pitch_speed > pitch:
                self.get_reaction_wheel("pitch", "CCW").throttle = min(
                    abs(pitch_discrepency),
                    1
                )
                self.get_reaction_wheel("pitch", "CW").throttle = 0
            else:
                self.get_reaction_wheel("pitch", "CCW").throttle = 0
                self.get_reaction_wheel("pitch", "CW").throttle = 0

            roll_discrepency = abs(roll - roll_speed)
            if roll_speed < roll:
                self.get_reaction_wheel("roll", "CW").throttle = min(
                    abs(roll_discrepency),
                    1
                )
                self.get_reaction_wheel("roll", "CCW").throttle = 0
            elif roll_speed > roll:
                self.get_reaction_wheel("roll", "CCW").throttle = min(
                    abs(roll_discrepency),
                    1
                )
                self.get_reaction_wheel("roll", "CW").throttle = 0
            else:
                self.get_reaction_wheel("roll", "CCW").throttle = 0
                self.get_reaction_wheel("roll", "CW").throttle = 0
            if wait is False:
                break
            sleep(0.1)
            yaw_speed, pitch_speed, roll_speed = (
                round(self.orientation_speed["yaw_speed"], 5),
                round(self.orientation_speed["pitch_speed"], 5),
                round(self.orientation_speed["roll_speed"], 5),
            )
        self.kill_rotational_throttle()
        return moved

    def rotate_to_orientation(self, pitch, roll, yaw, max_speed=1.0):
        def get_target_speed(current, target):
            # TODO (Austin) - Unintended consequences when target = 0
            if current <= target:
                if (target - current) <= 180:
                    return target - current
                else:
                    return -(360 + current - target)
            else:
                if (target - current) >= -180:
                    return target - current
                else:
                    return -(360 - (current - target))

        yaw_degrees, pitch_degrees, roll_degrees = (
            round(self.orientation['yaw_degrees'], 2),
            round(self.orientation['pitch_degrees'], 2),
            round(self.orientation['roll_degrees'], 2)
        )
        while yaw_degrees != round(yaw, 2) \
                or pitch_degrees != round(pitch, 2) \
                or roll_degrees != round(roll, 2):
            yaw_speed = min(
                get_target_speed(yaw_degrees, yaw)/(180) * 3,
                max_speed
            )
            roll_speed = min(
                get_target_speed(roll_degrees, roll)/(180) * 3,
                max_speed
            )
            pitch_speed = min(
                get_target_speed(pitch_degrees, pitch)/(180) * 3,
                max_speed
            )
            if not self.set_rotational_speed(pitch_speed, roll_speed,
                    yaw_speed, wait=False):  # noqa
                sleep(0.01)
            yaw_degrees, pitch_degrees, roll_degrees = (
                round(self.orientation['yaw_degrees'], 2),
                round(self.orientation['pitch_degrees'], 2),
                round(self.orientation['roll_degrees'], 2)
            )
        self.set_rotational_speed(0, 0, 0)

    def kill_velocity(self):
        while self.vector.magnitude() > 0.001:
            antivector = rotate_vector(
                self.vector.multiply(-1),
                {**self.orientation,
                    "yaw_degrees": self.orientation["yaw_degrees"] + 180},
                anti=True
            )
            self.apply_thrust_for_vector(antivector, anti=False)
            sleep(0.001)
        self.kill_throttle()

    def kill_velocity_old(self):
        while not coord_equals(self.vector, {'x': 0, 'y': 0, 'z': 0}):
            # X Axis (Forward/Aft)
            if self.vector['x'] < 0:
                self.get_thruster("forward").throttle = (
                    min(1, -self.vector['x']/10)
                )
                self.get_thruster("aft").throttle = 0
            elif self.vector['x'] > 0:
                self.get_thruster("forward").throttle = 0
                self.get_thruster("aft").throttle = (
                    min(1, self.vector['x']/10)
                )
                self.get_thruster("forward").throttle = 0
            elif round(self.vector['x'], 2) == 0.00:
                self.get_thruster("forward").throttle = 0
                self.get_thruster("aft").throttle = 0
            # Y Axis (Forward/Aft)
            if self.vector['y'] > 0:
                self.get_thruster("starboard").throttle = 0
                self.get_thruster("port").throttle = (
                    min(1, self.vector['y']/10)
                )
            elif self.vector['y'] < 0:
                self.get_thruster("starboard").throttle = (
                    min(1, -self.vector['y']/10)
                )
                self.get_thruster("port").throttle = 0
            elif round(self.vector['y'], 2) == 0.00:
                self.get_thruster("port").throttle = 0
                self.get_thruster("starboard").throttle = 0
            # Z Axis (Overhead/Deck)
            if self.vector['z'] > 0:
                self.get_thruster("overhead").throttle = 0
                self.get_thruster("deck").throttle = (
                    min(1, self.vector['z']/10)
                )
            elif self.vector['z'] < 0:
                self.get_thruster("overhead").throttle = (
                    min(1, -self.vector['z']/10)
                )
                self.get_thruster("deck").throttle = 0
            elif round(self.vector['z'], 2) == 0.00:
                self.get_thruster("deck").throttle = 0
                self.get_thruster("overhead").throttle = 0
            sleep(0.01)
        self.kill_throttle()

    COMPLEX_ATTRIBUTES = {
        "thrusters": Thruster,
        "reaction_wheels": ReactionWheel,
        "reactors": Reactor,
        "sensors": Sensor
    }
