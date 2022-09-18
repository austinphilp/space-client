from os import path

from client import SwarmServerClient
from models.ship import Ship
from vectors import Vector


ROOT_DIR = path.dirname(path.abspath(__file__))

if __name__ == "__main__":
    client = SwarmServerClient()
    ships = client.list_ships()
    if len(ships.ships) == 0:
        print("No ships found")
        exit(1)
    ship = Ship(client.get_ship(ships.ships[0].id), client)
