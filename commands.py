import json

from utils import send_command


def set_throttle(object_id, target_throttle):
    return send_command('set_throttle', object_id, target_throttle)


def set_power(object_id, power_toggle):
    if isinstance(power_toggle, bool):
        power_toggle = 1 if power_toggle else 0
    return send_command('set_power', object_id, power_toggle)


def set_rotation(object_id, target_pitch, target_yaw):
    return send_command('set_rotation', object_id, target_pitch, target_yaw)


def set_focus(object_id, target_focus):
    return send_command('set_focus', object_id, target_focus)


def status_report(object_id=None):
    response = send_command('status_report', object_id=object_id)
    return json.loads(response)


def sensor_ping(object_id):
    response = send_command('sensor_ping', object_id=object_id)
    return json.loads(response)
