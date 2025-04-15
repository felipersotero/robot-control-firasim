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

        self.e_rho = 0
        self.e_alpha = 0
        self.e_beta = 0
        
        # Ativa/Desativa o salvamento dos dados no JSON
        self.saving = True

        # Modo de simulação
        self.mode = 0 # 0 - controle | 1 - navegação
        self.enemies_actives = False

        # Ativa comunicação para controle dos robôs yellow e blue
        self.yellow_control = ProtoControl(team_color_yellow=True, control_ip="127.0.0.1", control_port=20011)
        self.blue_control = ProtoControl(team_color_yellow=False, control_ip="127.0.0.1", control_port=20011)

        # self.yellow_replacer = ReplacerComm(team_color_yellow=True, replacer_ip="127.0.0.1", replacer_port=20011)
        # self.blue_replacer = ReplacerComm(team_color_yellow=False, replacer_ip="127.0.0.1", replacer_port=20011)

        self.yellow_replacer = ReplacerComm(team_color_yellow=True)
        self.blue_replacer = ReplacerComm(team_color_yellow=False)

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

        self.robot_set = EntityData()

        self.robot_set.position.x = 0.1
        self.robot_set.position.y = 0.1
        self.robot_set.position.theta = 0.0

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
                    self.allies_direction[i] = [np.cos(self.allies_angles[i]), (np.sin(self.allies_angles[i]))]

                for i in range(3):
                    self.allies_angles_deg[i] = self.convertRad2Deg(self.allies_angles[i])

                # self.showFieldData()

    # CRIAÇÃO DAS FUNÇÕES

    def runEverything(self):
        try:
            while self.running:
                if not self.pause:
                    # self.getFieldData()
                    # print(f"{self.ball_coordinates}")
                    # print(f"{self.allies_coordinates[0]}")

                    wr, wl = self.control.processControl(robotId=0, mode=self.mode, func=self.getFieldData)
                    # print(f"wr = {round(wr, 2)}, wl = {round(wl, 2)}")
                    self.blue_control.transmit_robot(0, wl, wr)

                    # wr1, wl1 = self.control.processControl(robotId=1, mode=self.mode, func=self.getFieldData)
                    # self.blue_control.transmit_robot(1, wl1, wr1)

                    # wr2, wl2 = self.control.processControl(robotId=2, mode=self.mode, func=self.getFieldData)
                    # self.blue_control.transmit_robot(2, wl2, wr2)

                    if self.enemies_actives:
                       self.yellow_control.transmit_robot(0, 0, 2)
                       self.yellow_control.transmit_robot(1, 5, 2)
                       self.yellow_control.transmit_robot(2, 4, 0)

                    # else:
                    #     self.yellow_replacer.place_team([(self.robot_set, 0)])

                    time.sleep(0.01)

                else:
                    self.blue_control.stop_team()
                    self.yellow_control.stop_team()

        except KeyboardInterrupt:
            self.blue_control.stop_team()
            self.yellow_control.stop_team()
            
            logging.info("Ending")

            if self.saving:
                self.control.saveData2JSON()
                self.control.saveData2JSONErrors()
                self.control.saveData2JSONConstants()
                # self.control.saveData2JSONObjects()
                self.navigation.saveData2JSON()

    def stop(self):
        print("Encerrando execução com segurança...")
        self.blue_control.stop_team()
        self.yellow_control.stop_team()

        self.running = False

if __name__ == '__main__':
    main = Main()