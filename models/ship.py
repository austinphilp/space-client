from models.components import (
    Thruster
)

from utils import vector_from_proto


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

    def move_to(self, position):
        self.client.move_to(self.id, position)
