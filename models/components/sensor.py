from ..base import BaseRemoteObject
from commands import sensor_ping
from mixins import SetFocusMixin, SetRotationMixin, SetPowerMixin


class Sensor(BaseRemoteObject, SetFocusMixin, SetRotationMixin, SetPowerMixin):
    def ping(self):
        self._last_ping_results = sensor_ping(self.object_id)
        return self._last_ping_results

    def __repr__(self):
        return F"<Sensor {self.focus}º {round(self.current_range, 2)} range>"
