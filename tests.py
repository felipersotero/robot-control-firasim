from lib.comm.control import ProtoControl
from lib.comm.replacer import ReplacerComm
# from lib.core import data
from lib.comm.vision import ProtoVision
from lib.core.data import FieldData
from lib.core.data import EntityData
from lib.core.data import Pose2D

import time

def replacer_attempt():
    yellow_replacer = ReplacerComm(team_color_yellow=True, replacer_ip='224.0.0.1', replacer_port=20011) #10004)
    blue_replacer = ReplacerComm(team_color_yellow=False, replacer_ip="127.0.0.1", replacer_port=20011)

    # obj = EntityData()

    # obj.position = Pose2D(0.5, 0.5, 0)

    # print(obj.position)

    # yellow_replacer.place_team([(obj, 0)])

    robot_set = EntityData()

    robot_set.position.x = 0.1
    robot_set.position.y = 0.1
    robot_set.position.theta = 0.5

    # yellow_replacer.place_team([(robot_set, 0)])

    print(robot_set)

    yellow_replacer.place_team([(robot_set, 0)])
    blue_replacer.place_team([(robot_set, 0)])

def control():
    blue_control = ProtoControl(team_color_yellow=False, control_ip="127.0.0.1", control_port=20011)

    wl, wr = 40, 40

    blue_control.transmit_robot(0, wl, wr)
    time.sleep(2)

    blue_control.transmit_robot(0, 0, 0)

def json_read():
    data = {
        "robot_blue_0": {
            "x": [0, 1, 2],
            "y": [0, 1, 2],
            "theta": [[0, 0], [1, 1], [2, 2]],
            "time": [0, 1, 2]
        },
        "robot_yellow_0": {
            "x": [0, 1, 2],
            "y": [0, 1, 2],
            "theta": [[0, 0], [1, 1], [2, 2]],
            "time": [0, 1, 2]
        },
        "robot_yellow_1": {
            "x": [0, 1, 2],
            "y": [0, 1, 2],
            "theta": [[0, 0], [1, 1], [2, 2]],
            "time": [0, 1, 2]
        },
        "robot_yellow_2": {
            "x": [0, 1, 2],
            "y": [0, 1, 2],
            "theta": [[0, 0], [1, 1], [2, 2]],
            "time": [0, 1, 2]
        },
        "ball": {
            "x": [0, 1, 2],
            "y": [0, 1, 2],
            "time": [0, 1, 2]
        },
        "errors": {
            "e_rho": [0, 1, 2],
            "e_alpha": [0, 1, 2],
            "e_beta": [0, 1, 2],
            "time": [0, 1, 2]
        },
        "constants": {
            "k_rho": 1,
            "k_alpha": 1,
            "k_beta": 1
        }
    }

    value = data["ball"]["x"][0]
    print(value)

def main():

    print("Hello World!")
    json_read()

if __name__ == '__main__':
    main()

