from models.base import BaseRemoteObject
from models.components.thruster import Thruster
from models.components.reaction_wheel import ReactionWheel
from models.components.sensor import Sensor
from mixins import SetThrottleMixin, SetPowerMixin


class Panel(BaseRemoteObject, SetThrottleMixin, SetPowerMixin):
    COMPLEX_ATTRIBUTES = {
        "thrusters": Thruster,
        "reaction_wheels": ReactionWheel,
        "sensors": Sensor,
    }

    def __repr__(self):
        return F"<Panel {self.side}>"
