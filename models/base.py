import commands
from utils import throttle

from vectors import Vector


class BaseRemoteObject(object):
    COMPLEX_ATTRIBUTES = []

    def __init__(self, status_report):
        self._status_report = status_report
        self.object_id = self._status_report.get('object_id')

    @property
    def WRITABLE_FIELDS(self):
        return super().WRITABLE_FIELDS

    @property
    @throttle
    def status_report(self):
        self._status_report = commands.status_report(self.object_id)
        return self._status_report

    @throttle
    def _load_status_report(self):
        self.object_id = self.status_report.get('object_id')
        for key, value in self._status_report.items():
            if key in getattr(self, 'WRITABLE_FIELDS', []):
                key = "_" + key
            if key in self.COMPLEX_ATTRIBUTES:
                if isinstance(value, list):
                    value = [
                        self.COMPLEX_ATTRIBUTES[key](status_report=val)
                        for val in value
                    ]
                else:
                    value = self.COMPLEX_ATTRIBUTES[key](status_report=value)
            if key == "vector":
                value = Vector(value['x'], value['y'], value['z'])
            setattr(self, key, value)

    def __getattribute__(self, name):
        # This is to avoid recursion hell. Basically all the attributes below
        # are used by this override of getattribute, so if you don't explitly
        # avoid using them as _load_status_report triggers, it'll infinitely
        # recurse.
        BLACKLIST = [
            'object_id', 'status_report', '_load_status_report', '__class__',
            'COMPLEX_ATTRIBUTES', 'WRITABLE_FIELDS', '_status_report',
        ]
        if not ('set_' in name or name in BLACKLIST or '_last_ran_on' in name):
            self._load_status_report()
        return super().__getattribute__(name)
