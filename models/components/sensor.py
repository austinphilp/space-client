from utils import print_vector, vector_from_proto


class Sensor():
    pass


class PingSummary(object):
    def __init__(self, pb_ping_summary):
        self.readings = [
            SensorReading(reading) for reading in
            pb_ping_summary.readings]

    def __str__(self):
        return "\n".join([f"{i} | {x}" for i, x in enumerate(self.readings)][:10])


class SensorReading(object):
    def __init__(self, pb_sensor_reading):
        self.object_id = pb_sensor_reading.object_id
        self.object_type = pb_sensor_reading.object_type
        self.position = vector_from_proto(pb_sensor_reading.position)
        self.velocity = vector_from_proto(pb_sensor_reading.velocity)
        self.acceleration = vector_from_proto(pb_sensor_reading.acceleration)
        self.distance = pb_sensor_reading.distance
        self.radius = pb_sensor_reading.radius

    def __str__(self):
        if self.distance > 999:
            dist_str = f"{self.distance/1000:.2f}km"
        else:
            dist_str = f"{self.distance:.2f}m"
        radius_str = f"{self.radius}m"
        return f"{self.object_type} {dist_str} {radius_str} {print_vector(self.position)}"
