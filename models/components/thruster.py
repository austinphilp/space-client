class Thruster(object):
    def __init__(self, thottleProto):
        self.mass = thottleProto.mass
        self.max_force = thottleProto.max_force
        self.integrity = thottleProto.integrity
        self.max_integrity = thottleProto.max_integrity

    def __repr__(self, thottleProto):
        return "<Thruster>"
