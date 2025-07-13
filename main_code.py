from lib.comm.control import ProtoControl
from lib.comm.replacer import ReplacerComm
# from lib.core import data
from lib.comm.vision import ProtoVision
from lib.core.data import FieldData
from lib.core.data import EntityData
from lib.core.data import Pose2D

from control import Control
from navigation import Navigation

import logging
import numpy as np
import time
import json
import os
from queue import Queue
import threading
from interface_gui import start_gui  # importa a interface

class Main():
    def __init__(self):
        # Arrays e variáveis
        self.ball_coordinates = [None, None]
        self.allies_coordinates = [None, None, None]
        self.allies_direction = [None, None, None]
        self.allies_angles = [None, None, None]
        self.allies_angles_deg = [None, None, None]
        self.enemies_coordinates = [None, None, None]
        self.enemies_angles = [None, None, None]
        self.enemies_direction = [None, None, None]

        self.e_rho = 0
        self.e_alpha = 0
        self.e_beta = 0

        self.dist_rb = 0
        self.angle_rb = 0
        self.angle_rbg = 0

        self.kr = 0
        self.ka = 0
        self.kb = 0

        # JSON com os dados
        self.simulation_data = {
            "robot_blue_0": {"x": [], "y": [], "theta": []},
            "robot_yellow_0": {"x": [], "y": [], "theta": []},
            "robot_yellow_1": {"x": [], "y": [], "theta": []},
            "robot_yellow_2": {"x": [], "y": [], "theta": []},
            "ball": {"x": [], "y": []},
            "errors": {"e_rho": [], "e_alpha": [], "e_beta": []},
            "time": [],
            "constants": {"k_rho": self.kr, "k_alpha": self.ka, "k_beta": self.kb},
            "field_errors": {"dist_rb": [], "angle_rb": [], "angle_rbg": []},
        }

        # Ativa/Desativa o salvamento dos dados no JSON
        self.saving = True

        # Modo de simulação
        self.mode = 1 # 0 - controle | 1 - navegação
        self.enemies_actives = False

        # Ativa comunicação para controle dos robôs yellow e blue
        self.yellow_control = ProtoControl(team_color_yellow=True, control_ip="127.0.0.1", control_port=20011)
        self.blue_control = ProtoControl(team_color_yellow=False, control_ip="127.0.0.1", control_port=20011)

        # Ativa comunicação para pegar dados do campo e dos robôs
        self.test_field_data = FieldData()
        self.vision = ProtoVision(team_color_yellow=False, field_data=self.test_field_data)

        # Chama arquivo de controle
        self.control = Control(self)
        self.navigation = self.control.navigation

        # Interface para exibir os gráficos

        self.lock = threading.Lock()

        self.show_gui = False  # <- Flag para ativar/desativar GUI

        # Inicia a interface gráfica em uma thread separada
        if self.show_gui:
            gui_thread = threading.Thread(target=start_gui, args=(self,))
            gui_thread.daemon = True
            gui_thread.start()

        self.running = True  # Flag para manter execução
        self.pause = False

        # Chama funções de execução
        self.runEverything()

    # Funções de atualização

    # Funções de tratamento de dados
    def convertXValues(self, value):
        return ((0.75)+value)*100

    def convertYValues(self, value):
        return ((0.65)+value)*100

    def convertRad2Deg(self, value):
        return value*(180/(np.pi))

    def showFieldData(self):
        # Exibe os dados
        print("BALL: ", self.ball_coordinates)
        print("ROBOTS: ", self.allies_coordinates)
        print("ANGLES: ", self.allies_angles_deg)
        print("DIRECT: ", self.allies_direction)
        print("FOES: ", self.enemies_coordinates)

    def getFieldData(self):
            
            with self.lock:
                # Atualiza os dados do campo
                self.vision.update()

                # Converte e salva os dados nas variváveis
                self.ball_coordinates = [self.convertXValues(self.test_field_data.ball.position.x), self.convertYValues(self.test_field_data.ball.position.y)]
                # self.ball_coordinates = [self.test_field_data.ball.position.x, self.test_field_data.ball.position.y]

                for i in range(3):
                    self.allies_coordinates[i] = [self.convertXValues(self.test_field_data.robots[i].position.x), self.convertYValues(self.test_field_data.robots[i].position.y)]
                for i in range(3):
                    self.allies_angles[i] = self.test_field_data.robots[i].position.theta

                for i in range(3):
                    self.enemies_coordinates[i] = [self.convertXValues(self.test_field_data.foes[i].position.x), self.convertYValues(self.test_field_data.foes[i].position.y)]
                for i in range(3):
                    self.enemies_angles[i] = self.test_field_data.foes[i].position.theta

                for i in range(3):
                    self.allies_direction[i] = [np.cos(self.allies_angles[i]), (np.sin(self.allies_angles[i]))]

                for i in range(3):
                    self.enemies_direction[i] = [np.cos(self.enemies_angles[i]), (np.sin(self.enemies_angles[i]))]

                for i in range(3):
                    self.allies_angles_deg[i] = self.convertRad2Deg(self.allies_angles[i])

                # self.showFieldData()

    # Função para salvar dados
    def saveData(self):
        self.simulation_data["robot_blue_0"]["x"].append(self.allies_coordinates[0][0])
        self.simulation_data["robot_blue_0"]["y"].append(self.allies_coordinates[0][1])
        self.simulation_data["robot_blue_0"]["theta"].append(self.allies_direction[0])

        self.simulation_data["robot_yellow_0"]["x"].append(self.enemies_coordinates[0][0])
        self.simulation_data["robot_yellow_0"]["y"].append(self.enemies_coordinates[0][1])
        self.simulation_data["robot_yellow_0"]["theta"].append(self.enemies_direction[0])

        self.simulation_data["robot_yellow_1"]["x"].append(self.enemies_coordinates[1][0])
        self.simulation_data["robot_yellow_1"]["y"].append(self.enemies_coordinates[1][1])
        self.simulation_data["robot_yellow_1"]["theta"].append(self.enemies_direction[1])

        self.simulation_data["robot_yellow_2"]["x"].append(self.enemies_coordinates[2][0])
        self.simulation_data["robot_yellow_2"]["y"].append(self.enemies_coordinates[2][1])
        self.simulation_data["robot_yellow_2"]["theta"].append(self.enemies_direction[2])

        self.simulation_data["ball"]["x"].append(self.ball_coordinates[0])
        self.simulation_data["ball"]["y"].append(self.ball_coordinates[1])

        self.simulation_data["errors"]["e_rho"].append(self.e_rho)
        self.simulation_data["errors"]["e_alpha"].append(self.e_alpha)
        self.simulation_data["errors"]["e_beta"].append(self.e_beta)

        self.simulation_data["time"].append(self.current_time)

        if self.mode == 1:
            self.simulation_data["field_errors"]["dist_rb"].append(self.dist_rb)
            self.simulation_data["field_errors"]["angle_rb"].append(self.angle_rb)
            self.simulation_data["field_errors"]["angle_rbg"].append(self.angle_rbg)

    def generateFileName(self):
        i = 0
        while True:
            if i == 0:
                nome = "simulation_data.json"
            else:
                nome = "simulation_data-"+str(i)+".json"

            print(nome)
            caminho = os.path.join("./simulation_data", nome)
            print(caminho)
            if not os.path.exists(caminho):
                print(caminho)
                return caminho
            i += 1

    def saveDataToJson(self):

        file_name = self.generateFileName()

        with open(file_name, "w") as file:
            json.dump(self.simulation_data, file, indent=4)

    # CRIAÇÃO DAS FUNÇÕES

    def runEverything(self):

        self.start_time = time.time()

        try:
            while self.running:
                self.current_time = time.time() - self.start_time
                # print(self.current_time)

                if not self.pause:
                    # self.getFieldData()
                    wr, wl = self.control.processControl(robotId=0, mode=self.mode, func=self.getFieldData)
                    # print(f"wr = {round(wr, 2)}, wl = {round(wl, 2)}")

                    self.blue_control.transmit_robot(0, wl, wr)

                    # self.yellow_control.transmit_robot(0, -15, -15)
                    # self.yellow_control.transmit_robot(1, 10, 15)
                    # self.yellow_control.transmit_robot(2, 5, 12)

                    if self.enemies_actives:
                       self.yellow_control.transmit_robot(0, 0, 4)
                       self.yellow_control.transmit_robot(1, 8, 3)
                       self.yellow_control.transmit_robot(2, 6, 1)

                    # self.yellow_control.transmit_robot(0, 0, 4)

                    self.saveData()
                    time.sleep(0.01)

                else:
                    self.blue_control.stop_team()
                    self.yellow_control.stop_team()

        except KeyboardInterrupt:
            self.blue_control.stop_team()
            self.yellow_control.stop_team()

            
            logging.info("Ending")

            if self.saving:

                self.saveDataToJson()

                # self.control.saveData2JSON()
                # self.control.saveData2JSONErrors()
                # self.control.saveData2JSONConstants()
                # # self.control.saveData2JSONObjects()
                # self.navigation.saveData2JSON()

    def stop(self):
        print("Encerrando execução com segurança...")
        self.blue_control.stop_team()
        self.yellow_control.stop_team()

        self.running = False

if __name__ == '__main__':
    main = Main()