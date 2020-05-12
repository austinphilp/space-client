from os import path

import commands
from models.ship import Ship


ROOT_DIR = path.dirname(path.abspath(__file__))


def position_desc():
    _str = "({})".format(
        ', '.join("{:.2f}".format(v) for v in ship.position.values())
    )
    return F"Pos: {_str}"


def velocity_desc():
    _str = "({})".format(
        ', '.join("{:.2f}".format(v) for v in ship.vector.to_list())
    )
    return F"Vec: {_str}"


def acceleration_desc():
    _str = "({})".format(
        ', '.join("{:.5f}".format(v) for v in ship.acceleration.values())
    )
    return F"Acc: {_str}"


def orientation_desc():
    _str = "({})".format(
        ', '.join("{:.2f}".format(v) for v in ship.orientation.values())
    )
    return F"Orientation: {_str}"


def orientation_speed_desc():
    _str = "({})".format(
        ', '.join("{:.2f}".format(v) for v in ship.orientation_speed.values())
    )
    return F"Or. Speed: {_str}"


def power_consumption_desc():
    return "Power: {:.2f}%".format(
        ship.power_consumption/ship.power_available
    )


def performance_desc():
    return "Perf: {:.2f}%".format(100 * ship.performance_modifier)


def mass_desc():
    return "Mass: {:.2f}".format(ship.mass)


def integrity_desc():
    return "Integrity: {:.2f}%".format(100 * ship.integrity)


BOX = {
    "HOR": u"\u2501",
    "VER": u"\u2503",
    "TOP_T": u"\u253B",
    "MIDDLE_T": u"\u254B",
    "BOTTOM_T": u"\u2533",
    "LEFT_T": u"\u252B",
    "RIGHT_T": u"\u2523",
    "TOPLEFT_CORN": u"\u250F",
    "TOPRIGHT_CORN": u"\u2513",
    "BOTTOMLEFT_CORN": u"\u2517",
    "BOTTOMRIGHT_CORN": u"\u251B",
}


def get_top_row():
    return (
        BOX["TOPLEFT_CORN"]
        + BOX["HOR"] * (len(POS_INFO["POS"]) + 2)
        + BOX["BOTTOM_T"] + BOX["HOR"] * (len(POS_INFO["VEL"]) + 2)
        + BOX["HOR"] * 18 + BOX["TOPRIGHT_CORN"]
    )


def get_pos_row():
    return (
        F"{BOX['VER']} {POS_INFO['POS']} {BOX['VER']}"
        F" {POS_INFO['VEL']} {BOX['VER']} {POS_INFO['ACC']} "
    )


def get_ori_row():
    return (
        F"{BOX['VER']} {POS_INFO['ORI']}"
        F"{BOX['VER']} {POS_INFO['ORISPD']} "
        F"{BOX['VER']}"
    )


def get_2nd_row():
    return (
        BOX["BOTTOMLEFT_CORN"]
        + BOX["HOR"] * (len(POS_INFO["POS"]) + 2)
        + BOX["TOP_T"] + BOX["HOR"] * (len(POS_INFO["VEL"]) + 2)
        + BOX["BOTTOMRIGHT_CORN"]
    )


def get_ship_row():
    return (
        F"{BOX['VER']} {SHIP_INFO['PWR']} {BOX['VER']} "
        F"{SHIP_INFO['EFF']} {BOX['VER']} {SHIP_INFO['MSS']} "
        F"{BOX['VER']} {SHIP_INFO['INT']}"
    )


def get_thruster_rows():
    thrusters = ship.thrusters
    reaction_wheels = ship.reaction_wheels
    header = (
        F"{BOX['VER']} Power {BOX['VER']} Name {BOX['VER']} Throttle"
    )
    rows = []
    thruster_info = [
        {
            "power": '√' if ship.thrusters[i].powered_on else 'X',
            "name": F"{ship.thrusters[i].direction.title()} Thruster ({i})",
            "throttle": '{:.2f}%'.format(ship.thrusters[i].throttle * 100),
            "force": '{:.2f}/{:.2f}'.format(
                ship.thrusters[i].current_force,
                ship.thrusters[i].max_force
            ),
            "integrity": '{:.2f}%'.format(ship.thrusters[i].integrity * 100),
        }
        for i in range(max(len(thrusters), len(reaction_wheels)))
    ]
    reaction_wheel_info = [
        {
            "power": '√' if ship.reaction_wheels[i].powered_on else 'X',
            "name": (
                F"{ship.reaction_wheels[i].rotation.upper()} "
                F"{ship.reaction_wheels[i].axis.title()} Wheel ({i})"
            ),
            "throttle": '{:.2f}%'.format(
                ship.reaction_wheels[i].throttle * 100
            ),
            "force": '{:.2f}/{:.2f}'.format(
                ship.reaction_wheels[i].current_force,
                ship.reaction_wheels[i].max_force
            ),
            "integrity": '{:.2f}%'.format(
                ship.reaction_wheels[i].integrity * 100
            ),
        }
        for i in range(len(reaction_wheels))
    ]
    # get the max width for every column
    ti_max = {
        key: len(max(thruster_info, key=lambda t: len(t[key]))[key])
        for key in thruster_info[0].keys()
    }
    # Ensure label isn't larger than any value in the table
    ti_max = {key: max(len(key), value) for key, value in ti_max.items()}

    rows = [
        F"{BOX['VER']} {thruster['power'].center(ti_max['power'])} "
        F"{BOX['VER']} {thruster['name'].center(ti_max['name'])} "
        F"{BOX['VER']} {thruster['throttle'].center(ti_max['throttle'])} "
        F"{BOX['VER']} {thruster['force'].center(ti_max['force'])} "
        F"{BOX['VER']} {thruster['integrity'].center(ti_max['integrity'])} "
        F"{BOX['VER']}"
        for thruster in thruster_info + reaction_wheel_info
    ]

    header = (
        F"{BOX['VER']} Power {BOX['VER']} "
        F"{' Name '.center(ti_max['name'])} {BOX['VER']} "
        F"{'Throttle'.center(ti_max['throttle'])} {BOX['VER']}"
        F"{'Force'.center(ti_max['force']+2)}{BOX['VER']}"
        F"{'Integrity'.center(ti_max['integrity']+2)}{BOX['VER']}"
    )
    return [header, ] + rows


if __name__ == "__main__":
    system = commands.status_report()
    ship = Ship(status_report=system['ships'][0])
    POS_INFO = {
        "POS": position_desc(),
        "VEL": velocity_desc(),
        "ACC": acceleration_desc(),
        "ORI": orientation_desc(),
        "ORISPD": orientation_speed_desc()
    }
    SHIP_INFO = {
        "PWR": power_consumption_desc(),
        "EFF": performance_desc(),
        "MSS": mass_desc(),
        "INT": integrity_desc()
    }

    print(get_top_row())
    print(get_pos_row())
    print(get_2nd_row())
    print(get_ori_row())
    print(get_2nd_row())
    print(get_ship_row())
    print(BOX["HOR"] * 71)
    print('\n'.join(get_thruster_rows()))
    print(BOX["HOR"] * 71)
    # print(get_comp_row_2())
