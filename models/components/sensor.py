from ..base import BaseRemoteObject
from mixins import SetFocusMixin, SetRotationMixin, SetPowerMixin


class Sensor(BaseRemoteObject, SetFocusMixin, SetRotationMixin, SetPowerMixin):
    pass
