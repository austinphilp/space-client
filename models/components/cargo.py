class Cargo(object):
    def __init__(self, cargoProto):
        self.items = [CargoItem(iProto) for iProto in cargoProto.items]
        self.volume_used = cargoProto.volume_used
        self.volume_capacity = cargoProto.volume_capacity

    def __repr__(self):
        return f"<Cargo {len(self.items)} items {self.volume_used}m^3/{self.volume_capacity}m^3>"  # noqa


class CargoItem(object):
    def __init__(self, cargoItemProto):
        self.object_id = cargoItemProto.object_id
        self.object_type = cargoItemProto.object_type
        self.volume = cargoItemProto.volume
        self.mass = cargoItemProto.mass

    def __repr__(self):
        return f"<CargoItem {self.object_type} {self.volume}m^3"  # noqa
