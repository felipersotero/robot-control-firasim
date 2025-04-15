from lib.comm.control import ProtoControl
from lib.comm.replacer import ReplacerComm
# from lib.core import data
from lib.comm.vision import ProtoVision
from lib.core.data import FieldData
from lib.core.data import EntityData
from lib.core.data import Pose2D

def main():

    yellow_replacer = ReplacerComm(team_color_yellow=True, replacer_ip="127.0.0.1", replacer_port=20011)
    blue_replacer = ReplacerComm(team_color_yellow=False, replacer_ip="127.0.0.1", replacer_port=20011)

    # obj = EntityData()

    # obj.position = Pose2D(0.5, 0.5, 0)

    # print(obj.position)

    # yellow_replacer.place_team([(obj, 0)])

    robot_set = EntityData()

    robot_set.position.x = 0.1
    robot_set.position.y = 0.1
    robot_set.position.theta = 0.0

    # yellow_replacer.place_team([(robot_set, 0)])

    print(robot_set)

    blue_replacer.place_team([(robot_set, 0)])

if __name__ == '__main__':
    main()