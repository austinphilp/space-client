from commands import (
    set_throttle,
    set_power,
    set_focus,
    set_rotation,
)


class SetThrottleMixin(object):
    @property
    def WRITABLE_FIELDS(self):
        return ['throttle'] + getattr(super(), 'WRITABLE_FIELDS', [])

    @property
    def throttle(self):
        return self._throttle

    @throttle.setter
    def throttle(self, value):
        return self.set_throttle(value)

    def set_throttle(self, throttle):
        res = set_throttle(self.object_id, throttle)
        self._load_status_report()
        return res

    def _load_status_report(self, status_report=None):
        return super()._load_status_report(status_report)


class SetFocusMixin(object):
    @property
    def WRITABLE_FIELDS(self):
        return ['focus'] + getattr(super(), 'WRITABLE_FIELDS', [])

    @property
    def focus(self):
        return self._focus

    @focus.setter
    def focus(self, value):
        return self.set_focus(value)

    def set_focus(self, focus):
        res = set_focus(self.object_id, focus)
        self._load_status_report()
        return res

    def _load_status_report(self, status_report=None):
        return super()._load_status_report(status_report)


class SetPowerMixin(object):
    @property
    def WRITABLE_FIELDS(self):
        return ['powered_on'] + getattr(super(), 'WRITABLE_FIELDS', [])

    @property
    def powered_on(self):
        return self._powered_on

    @powered_on.setter
    def powered_on(self, value):
        return self.set_power(value)

    def set_power(self, power):
        return set_power(self.object_id, power)

    def _load_status_report(self, status_report=None):
        return super()._load_status_report(status_report)


class SetRotationMixin(object):
    @property
    def WRITABLE_FIELDS(self):
        return [
            'pitch_degrees',
            'yaw_degrees',
            'pitch_radians',
            'yaw_radians',
        ] + getattr(super(), 'WRITABLE_FIELDS', [])

    @property
    def pitch(self):
        return self._pitch_degrees

    @pitch.setter
    def pitch(self, value):
        return set_rotation(self, pitch=value, yaw=self.yaw)

    @property
    def yaw(self):
        return self._yaw_degrees

    @yaw.setter
    def yaw(self, value):
        return set_rotation(self, pitch=self.pitch, yaw=value)

    def set_rotation(self, pitch, yaw):
        return set_rotation(self.object_id, pitch, yaw)

    def _load_status_report(self, status_report=None):
        return super()._load_status_report(status_report)
