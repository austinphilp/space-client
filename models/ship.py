import time

from models.components import (
    Thruster,
    Cargo,
)

from utils import print_vector, vector_from_proto


class Ship(object):
    def __init__(self, shipProto, client):
        self._client = client
        self.id = shipProto.id
        self.mass = shipProto.mass
        self.thrusters = Thruster(shipProto.thrusters)
        self.position = vector_from_proto(shipProto.position)
        self.velocity = vector_from_proto(shipProto.velocity)
        self.acceleration = vector_from_proto(shipProto.acceleration)
        self.integrity = shipProto.integrity
        self.max_integrity = shipProto.max_integrity
        self.cargo = Cargo(shipProto.cargo)

    def move_to(self, position):
        future = self._client.move_to(self.id, position)
        while not future.done():
            print(self.vector_info())
            time.sleep(1)
            print("\033[A                             \033[A" * 2)
        else:
            print(self.vector_info())
        print("Movement complete")

    def vector_info(self):
        return (f"Pos: {print_vector(self.position)}\n"
                f"Vel {print_vector(self.velocity)}\n"
                f"Acc {print_vector(self.acceleration)}")

    def sensor_ping(self):
        return self._client.sensor_ping(self.id)

    def stow(self, target_id):
        return self._client.stow(self.id, target_id)

    def __getattribute__(self, name):
        # This is to avoid recursion hell. Basically all the attributes below
        # are used by this override of getattribute, so if you don't explitly
        # avoid using them as _load_status_report triggers, it'll infinitely
        # recurse.
        BLACKLIST = ['id', '_client', '__init__']
        if not ('set_' in name or name in BLACKLIST):
            self.__init__(self._client.get_ship(self.id), self._client)
        return super().__getattribute__(name)
