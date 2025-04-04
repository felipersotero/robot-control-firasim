from lib.comm.control import ProtoControl
# from lib.core import data
from lib.comm.vision import ProtoVision
from lib.core.data import FieldData

from control import Control
from navigation import Navigation
from build_graphics import BuildGraphics

import logging
import numpy as np
import time
import threading

class Main():
    def __init__(self):
        # Arrays e variáveis
        self.ball_coordinates = [None, None]
        self.allies_coordinates = [None, None, None]
        self.allies_direction = [None, None, None]
        self.allies_angles = [None, None, None]
        self.allies_angles_deg = [None, None, None]
        self.enemies_coordinates = [None, None, None]

        # Ativa/Desativa o salvamento dos dados no JSON
        self.saving = False

        '''
            Modos de controle:
                0 - sem navegação
                1 - com navegação
        '''
        self.mode = 1

        # Ativa comunicação para controle dos robôs yellow e blue
        self.yellow_control = ProtoControl(team_color_yellow=True, control_ip="127.0.0.1", control_port=20011)
        self.blue_control = ProtoControl(team_color_yellow=False, control_ip="127.0.0.1", control_port=20011)

        # Ativa comunicação para pegar dados do campo e dos robôs
        self.test_field_data = FieldData()
        self.vision = ProtoVision(team_color_yellow=False, field_data=self.test_field_data)

        # Chama arquivo de controle
        self.control = Control(self)
        self.navigation = self.control.navigation

        # Chama funções de execução
        self.runEverything()

    # CRIAÇÃO DAS FUNÇÕES

    def runEverything(self):
        try:
            while True:
                wr, wl = self.control.processControl(robotId=0, mode=self.mode)
                # print(f"wr = {round(wr, 2)}, wl = {round(wl, 2)}")
                self.blue_control.transmit_robot(0, wl, wr)

                # Controle rivais (yellow)
                # self.yellow_control.transmit_robot(0, 5, 10)
                # self.yellow_control.transmit_robot(1, 10, 5)
                # self.yellow_control.transmit_robot(2, 1, 3)

                self.yellow_control.transmit_robot(0, 0, 0)
                self.yellow_control.transmit_robot(1, 0, 0)
                self.yellow_control.transmit_robot(2, 0, 0)

        except KeyboardInterrupt:
            logging.info("Ending")
            if self.saving:
                if self.mode == 0:
                    self.control.saveData2JSON()
                    self.control.saveData2JSONErrors()
                    # self.control.saveData2JSONObjects()
                elif self.mode == 1:
                    self.navigation.saveData2JSON()

if __name__ == '__main__':
    main = Main()