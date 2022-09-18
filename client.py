import grpc

from models.components.sensor import PingSummary
from ship.v1.ship_pb2_grpc import ShipServiceStub
from ship.v1.ship_pb2 import (
    GetShipRequest,
    MoveToRequest,
    Empty,
    SensorPingRequest,
    StowRequest,
)
from util.v1.util_pb2 import Vector


class SwarmServerClient(object):
    def __init__(self):
        self._channel = grpc.insecure_channel('localhost:8000')
        self.ship_stub = ShipServiceStub(self._channel)

    def list_ships(self):
        return self.ship_stub.GetShips(Empty())

    def get_ship(self, ship_id):
        return self.ship_stub.GetShip(GetShipRequest(ship_id=ship_id))

    def move_to(self, ship_id, position):
        return self.ship_stub.MoveTo.future(
            MoveToRequest(ship_id=ship_id,
                          target_position=Vector(
                              x=position.x,
                              y=position.y,
                              z=position.z)))

    def sensor_ping(self, ship_id):
        return PingSummary(
            self.ship_stub.SensorPing(SensorPingRequest(ship_id=ship_id))
        )

    def stow(self, ship_id, target_id):
        self.ship_stub.Stow(StowRequest(ship_id=ship_id, target_id=target_id))
