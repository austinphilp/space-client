from ..base import BaseRemoteObject
from mixins import SetThrottleMixin, SetPowerMixin


class ReactionWheel(BaseRemoteObject, SetThrottleMixin, SetPowerMixin):
    pass
