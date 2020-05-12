from os import path

import commands
from models.ship import Ship


ROOT_DIR = path.dirname(path.abspath(__file__))

if __name__ == "__main__":
    system = commands.status_report()
    ship = Ship(status_report=system['ships'][0])
