from os import path

import commands
from models.ship import Ship


ROOT_DIR = path.dirname(path.abspath(__file__))


def print_report(body):
    pos = body['position']
    dimmensions = body['dimmensions'].values()
    vec = body["vector"]
    dim = body["dimmensions"]
    print(F"======= {body['object_id']} =======")
    print(
        "Position: " +
        F"{round(pos['x'], 2)}, {round(pos['y'], 2)}, {round(pos['z'], 2)}"
    )
    print("Dimmensions: " + ' x '.join(str(round(x, 2)) for x in dimmensions))
    print(
        "Vector: " +
        F"{round(vec['x'], 2)}, {round(vec['y'], 2)}, {round(vec['z'], 2)}"
    )
    print(
        "Dimmensions: " +
        F"{round(dim['height'], 2)}, {round(dim['width'], 2)}, {round(dim['depth'], 2)}"  # noqa
    )


if __name__ == "__main__":
    system = commands.status_report()
    ship = Ship(status_report=system['ships'][0])
    bodies = set()
    for panel in ship.panels:
        ping_results = panel.sensors[0].ping()
        for body in ping_results.get('detectable_bodies', []):
            if body['object_id'] not in bodies:
                print_report(body)
            bodies.add(body['object_id'])
    if not bodies:
        _range = max(panel.sensors[0].current_range for panel in ship.panels)
        print(F"Nothing detected within range ({_range})")
