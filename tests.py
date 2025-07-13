from lib.comm.control import ProtoControl
from lib.comm.replacer import ReplacerComm
# from lib.core import data
from lib.comm.vision import ProtoVision
from lib.core.data import FieldData
from lib.core.data import EntityData
from lib.core.data import Pose2D

import time

import numpy as np

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

def noise():
    # Vetor resultante
    F = [1, 0]
    # ruido_magnitude = 0.01 * np.linalg.norm(F)

    # # Ruído (pequeno vetor aleatório)
    # ruido = np.random.uniform(-1, 1, size=2)
    # ruido = ruido / np.linalg.norm(ruido) * ruido_magnitude  # normaliza e escala

    # # Novo vetor resultante com ruído
    # F_mod = F + ruido

    # # print(F_mod)

    resulting_force_mod = np.linalg.norm(F)
    resulting_force_angle = np.arccos(np.clip(np.dot(F,[1,0])/np.linalg.norm(F), -1.0, 1.0))

    print(f"F = {np.round(resulting_force_mod, 2)} | {np.round(np.degrees(resulting_force_angle), 2)}°")

    # noise = np.random.uniform(0, (np.pi/4))/10

    resulting_force_angle = resulting_force_angle*1.1 # + (0.01*np.sign(resulting_force_angle)) # noise*np.sign(resulting_force_angle)

    print(f"F = {np.round(resulting_force_mod, 2)} | {np.round(np.degrees(resulting_force_angle), 2)}°")

    dx = np.cos(resulting_force_angle)
    dy = np.sin(resulting_force_angle)

    resulting_force = [resulting_force_mod*1.5*dx, resulting_force_mod*1.5*dy]

    resulting_force_mod = np.linalg.norm(resulting_force)
    resulting_force_angle = np.arccos(np.clip(np.dot(resulting_force,[1,0])/np.linalg.norm(resulting_force), -1.0, 1.0))

    print(f"F = {np.round(resulting_force_mod, 2)} | {np.round(np.degrees(resulting_force_angle), 2)}°")

def vector():

    vector = [3, 4]

    mod = np.linalg.norm(vector)
    angle_vec = np.arccos(np.clip(np.dot(vector,[1,0])/np.linalg.norm(vector), -1.0, 1.0))

    print(vector)
    print(f"{mod} | {np.degrees(angle_vec)}°")

    print("########## ALTERAÇÕES ##########")

    angle_vec = angle_vec*1.1
    # mod = mod*1.5
    print(f"{mod} | {np.degrees(angle_vec)}°")
    vector_2 = [mod*np.cos(angle_vec), mod*np.sin(angle_vec)]
    print(vector_2)

def vectorAgain():
    vector = [-4.36369149e+01, -1.71283586e-03]

    mod = np.linalg.norm(vector)
    angle_vec = np.arctan2(vector[1], vector[0])  # Usa arctan2!

    print(f"vetor antes:  {vector}")
    vector = [mod*np.cos(angle_vec), mod*np.sin(angle_vec)]
    print(f"vetor depois: {vector}")
    
def main():

    print("Hello World!")
    vectorAgain()

if __name__ == '__main__':
    main()

