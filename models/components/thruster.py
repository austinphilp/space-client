from models.base import BaseRemoteObject
from mixins import SetThrottleMixin, SetPowerMixin


class Thruster(BaseRemoteObject, SetThrottleMixin, SetPowerMixin):
    def __repr__(self):
        return F"<Thruster {self.direction} {self.throttle}>"
