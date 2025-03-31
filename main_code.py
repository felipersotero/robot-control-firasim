from lib.comm.control import ProtoControl
# from lib.core import data
from lib.comm.vision import ProtoVision
from lib.core.data import FieldData

from control import Control
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
        self.saving = True

        # Ativa comunicação para controle dos robôs yellow e blue
        self.yellow_control = ProtoControl(team_color_yellow=True, control_ip="127.0.0.1", control_port=20011)
        self.blue_control = ProtoControl(team_color_yellow=False, control_ip="127.0.0.1", control_port=20011)

        # Ativa comunicação para pegar dados do campo e dos robôs
        self.test_field_data = FieldData()
        self.vision = ProtoVision(team_color_yellow=False, field_data=self.test_field_data)

        # Chama arquivo de controle
        self.control = Control(self)

        # self.control.loadCSVWriter()

        # self.graphics = BuildGraphics(self)
        # # self.graphics.animateGraph()  # Chama a animação corretamente

        # self.graphics_thread = threading.Thread(target=self.graphics.animateGraph)
        # self.graphics_thread.daemon = True  # Para garantir que a thread seja encerrada quando o programa terminar
        # self.graphics_thread.start()

        # # Flag para controle da thread
        # self.running = True

        # # Inicia a thread de atualização de dados
        # self.data_thread = threading.Thread(target=self.updateDataLoop, daemon=True)
        # self.data_thread.start()

        # Chama funções de execução
        self.runEverything()

    # CRIAÇÃO DAS FUNÇÕES

    def runEverything(self):
        try:
            while True:

                wr, wl = self.control.processControl()

                # print(f"wr = {round(wr, 2)}, wl = {round(wl, 2)}")

                # self.blue_control.transmit_robot(robot_id, left_wheel, right_wheel)
                self.blue_control.transmit_robot(0, wl, wr)
                # self.yellow_control.transmit_robot(0, wl, wr)
                # self.blue_control.transmit_robot(1, 0, 0)
        
        except KeyboardInterrupt:
            logging.info("Ending")

            if self.saving:
                self.control.saveData2JSON()
                self.control.saveData2JSONErrors()

            # self.running = False  # Para a thread de atualização de dados
            # self.data_thread.join()  # Aguarda a thread encerrar corretamente
    
    # def updateDataLoop(self):
    #     while self.running:
    #         self.control.getFieldData()
    #         time.sleep(0.5)  # Delay fixo para a atualização

if __name__ == '__main__':
    main = Main()