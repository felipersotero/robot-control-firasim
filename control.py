import numpy as np
import time
import csv
import json

from navigation import Navigation

class Control():
    def __init__(self, Main):

        self.main = Main
        # self.ball_coordinates = Main.ball_coordinates

        # self.ball_coordinates = Main.ball_coordinates

        # self.allies_coordinates = Main.allies_coordinates
        # self.allies_direction = Main.allies_direction
        # self.allies_angles = Main.allies_angles
        # self.allies_angles_deg = Main.allies_angles_deg
        # self.enemies_coordinates = Main.enemies_coordinates

        self.vision = Main.vision
        self.test_field_data = Main.test_field_data

        # self.getFieldData = Main.getFieldData
        self.saving = Main.saving

        # Instância da classe Navigation
        self.navigation = Navigation(self)

        # Dimensões do robo
        self.r = 1
        self.L = 7.5

        # Coordenadas do gol
        self.goal_coordinates = [0, 65]

        self.robot_positions = []  # Lista para armazenar os dados
        self.robot_errors = []  # Lista para armazenar os dados
        self.data = [None, None, None, None, None, None, None, None, None]
    # Funções de tratamento de dados

    def angleBetweenObjects(self, target_coordinates, source_coordinates, source_direction):
        v1 = source_direction
        v2 = np.array([target_coordinates[0]-source_coordinates[0], target_coordinates[1]-source_coordinates[1]])

        dot_product = np.dot(v1, v2)
        magnitude1 = np.linalg.norm(v1)
        magnitude2 = np.linalg.norm(v2)

        cosine_theta = dot_product / (magnitude1 * magnitude2)

        angle_rad = np.arccos(np.clip(cosine_theta, -1.0, 1.0))
        angle_deg = np.degrees(angle_rad)

    # Calcular o produto vetorial para determinar a direção
        cross_product = np.cross(v1, v2)

        # Se o produto vetorial for negativo, o objeto alvo está à esquerda
        if cross_product < 0:
            angle_rad *= -1

        return angle_rad

    def distanceBetweenObjects(self, target_coordinates, source_coordinates):
        dx = abs(target_coordinates[0] - source_coordinates[0])
        dy = abs(target_coordinates[1] - source_coordinates[1])
        distance = np.sqrt((dx**2)+(dy**2))

        return distance

    def showFieldData(self):
        # Exibe os dados
        print("BALL: ", self.main.ball_coordinates)
        print("ROBOTS: ", self.main.allies_coordinates)
        print("ANGLES: ", self.main.allies_angles_deg)
        print("DIRECT: ", self.main.allies_direction)
        print("FOES: ", self.main.enemies_coordinates)

    # Funções principais de controle
    def processControl(self, robotId, mode, func):
        func()
        
        # print("==================")
        # self.showFieldData()

        if mode == 0:
            # print("Modo apenas Controle")
            dist_ball = self.distanceBetweenObjects(self.main.ball_coordinates, self.main.allies_coordinates[robotId])
            angle_ball = self.angleBetweenObjects(self.main.ball_coordinates, self.main.allies_coordinates[robotId], self.main.allies_direction[robotId])

            dy_gamma = self.main.ball_coordinates[1] - self.main.allies_coordinates[robotId][1]
            dx_gamma = self.main.ball_coordinates[0] - self.main.allies_coordinates[robotId][0]
            gamma = np.arctan2(dy_gamma, dx_gamma)

            dy_theta_g = self.goal_coordinates[1] - self.main.ball_coordinates[1]
            dx_theta_g = self.goal_coordinates[0] - self.main.ball_coordinates[0]
            theta_g = np.arctan2(dy_theta_g, dx_theta_g)

            if (abs(gamma) + abs(theta_g)) > (np.pi):
                angle_to_goal = 2*(np.pi) - abs(gamma) - abs(theta_g)
            else:
                angle_to_goal = abs(gamma) + abs(theta_g)

            area = 1 # 1 - bola à frente | 2 - bola atrás

            if abs(angle_ball) > (np.pi)/2:
                area = 2
                if angle_ball >= 0:
                    angle_ball = np.pi - angle_ball
                else:
                    angle_ball = abs(angle_ball) - np.pi

            # print(f"rho: {round(dist_ball, 2)} cm || area: {area} || alpha: {round(self.convertRad2Deg(angle_ball), 2)} ° || beta: {round(self.convertRad2Deg(angle_to_goal), 2)} ° || gamma: {round(self.convertRad2Deg(gamma), 2)} ° || theta_g: {round(self.convertRad2Deg(theta_g), 2)} °")

            angle_to_goal = 0

            # print(self.main.convertRad2Deg(angle_to_goal))
            
            # Chama função para aplicar controle
            wr, wl = self.controlRobot(dist_ball, angle_ball, angle_to_goal, area)

            if (self.saving):
                self.savePosition(self.main.allies_coordinates[robotId][0], self.main.allies_coordinates[robotId][1], self.main.allies_direction[robotId])

                with self.main.lock:
                    self.main.e_rho = 0 - abs(dist_ball)
                    self.main.e_alpha = 0 - abs(angle_ball)
                    self.main.e_beta = 0 - abs(angle_to_goal)

                self.saveErrors(self.main.e_rho, self.main.e_alpha, self.main.e_beta)

                # Salvamento dos dados dos objetos
                self.saveDataObjects(0, self.main.allies_coordinates[robotId][0], self.main.allies_coordinates[robotId][1])
                self.saveDataObjects(1, self.main.ball_coordinates[0], self.main.ball_coordinates[1])

                for i, enemy in enumerate(self.main.enemies_coordinates, start=2):
                    self.saveDataObjects(i, enemy[0], enemy[1])
                
                self.saveDataObjects(5, np.cos(self.main.allies_angles[robotId]), np.sin(self.main.allies_angles[robotId])) # theta
                self.saveDataObjects(6, dist_ball*np.cos(angle_ball), dist_ball*np.sin(angle_ball)) # rho e alfa
                self.saveDataObjects(7, np.cos(angle_to_goal), np.sin(angle_to_goal)) # beta

        elif mode == 1:
            # print("Modo com Navegação")
            vector = self.navigation.createPotentialField(robotId=robotId)

            mod = np.linalg.norm(vector)
            angle = self.angleBetweenObjects(self.main.allies_coordinates[robotId] + vector, self.main.allies_coordinates[robotId], self.main.allies_direction[robotId])

            area = 1 # 1 - alvo à frente | 2 - alvo atrás

            if abs(angle) > (np.pi)/2:
                area = 2
                if angle >= 0:
                    angle = np.pi - angle
                else:
                    angle = abs(angle) - np.pi

            wr, wl = self.controlRobot(mod, angle, 0, area)

            if (self.saving):
                self.savePosition(self.main.allies_coordinates[robotId][0], self.main.allies_coordinates[robotId][1], self.main.allies_direction[robotId])

                with self.main.lock:
                    self.main.e_rho = 0 - abs(mod)
                    self.main.e_alpha = 0 - abs(angle)
                    self.main.e_beta = 0

                self.saveErrors(self.main.e_rho, self.main.e_alpha, self.main.e_beta)

                # Salvamento dos dados dos objetos
                self.saveDataObjects(0, self.main.allies_coordinates[robotId][0], self.main.allies_coordinates[robotId][1])
                self.saveDataObjects(1, self.main.ball_coordinates[0], self.main.ball_coordinates[1])

                for i, enemy in enumerate(self.main.enemies_coordinates, start=2):
                    self.saveDataObjects(i, enemy[0], enemy[1])
                
                self.saveDataObjects(5, np.cos(self.main.allies_angles[robotId]), np.sin(self.main.allies_angles[robotId])) # theta
                # self.saveDataObjects(6, dist_ball*np.cos(angle_ball), dist_ball*np.sin(angle_ball)) # rho e alfa
                # self.saveDataObjects(7, np.cos(angle_to_goal), np.sin(angle_to_goal)) # beta

        return wr, wl

    def controlRobot(self, rho, alpha, beta, area):
        self.kr = 0.8
        self.ka = 14
        self.kb = -1.5

        if abs(alpha) > ((np.pi)/4):
            self.kr = 0.2
            self.ka = 5
            self.kb = 0

        if area == 2:
            self.kr = -self.kr
            self.ka = -self.ka
            self.kb = -self.kb

        # if rho < 8:
        #     kr = 3
        #     ka = 1
        #     kb = -2.5

        v = self.kr*rho
        w = self.ka*alpha + self.kb*beta

        # print(f"v = {v} || w = {w}")

        if (self.main.ball_coordinates[0] > 150) or (self.main.ball_coordinates[0] < 0): # or rho < 9:
            wr = 0
            wl = 0
        else:
            wr = (v/self.r) + ((w*self.L)/(2*self.r))
            wl = (v/self.r) - ((w*self.L)/(2*self.r))

        return wr, wl

    # Funções para salvar dados
    def savePosition(self, x, y, theta):
        self.robot_positions.append({"x": x, "y": y, "theta": theta})

    def saveErrors(self, e_rho, e_alpha, e_beta):
        self.robot_errors.append({"e_rho": e_rho, "e_alpha": e_alpha, "e_beta": e_beta})

    def saveData2JSON(self):
        # Salvar em arquivo JSON ao final da execução
        with open("simulation_data/robot_data.json", "w") as file:
            json.dump(self.robot_positions, file, indent=4)

    def saveData2JSONErrors(self):
        # Salvar em arquivo JSON ao final da execução
        with open("simulation_data/errors_data.json", "w") as file:
            json.dump(self.robot_errors, file, indent=4)

    def saveData2JSONConstants(self):
        with open("simulation_data/constants_data.json", "w") as file:
            json.dump({"kr": self.kr, "ka": self.ka, "kb": self.kb}, file, indent=4)

    # Funções para salvar dados
    def saveDataObjects(self, i, x, y):
        self.data[i] = {"x": x, "y": y}
        # print(f"Salvando dados... {x}, {y}")
        # print(self.data)

    def saveData2JSONObjects(self):
        # Salvar em arquivo JSON ao final da execução
        with open("simulation_data/field_data.json", "w") as file:
            json.dump(self.data, file, indent=4)
            # print("Dados salvos!")
            # print(self.data)