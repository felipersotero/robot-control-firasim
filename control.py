import numpy as np
import time
import csv
import json

from navigation import Navigation

class Control():
    def __init__(self, Main):

        self.main = Main

        self.vision = Main.vision
        self.test_field_data = Main.test_field_data
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

        # Constantes de controle
        # self.kr = self.main.kr

    # Funções de tratamento de dados

    def angleBetweenObjects(self, target_coordinates, source_coordinates, source_direction):
        v1 = source_direction
        v2 = np.array([target_coordinates[0]-source_coordinates[0], target_coordinates[1]-source_coordinates[1]])

        dot_product = np.dot(v1, v2)
        magnitude1 = np.linalg.norm(v1)
        magnitude2 = np.linalg.norm(v2)

        # print(f"{magnitude1} | {magnitude2}")

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

    def speedLimiter(self, wr, wl):
        w_lim = 40
        w_max = max(abs(wr), abs(wl))

        # Sempre mantendo velocidade máxima
        # if w_max < (w_lim):
        #     w_lim = w_max

        # if w_max == 0:
        #     wr = 0
        #     wl = 0
        # else:
        #     wr = (wr/w_max)*w_lim
        #     wl = (wl/w_max)*w_lim

        # Limitando apenas para velocidades mais altas
        if w_max > w_lim:
            wr = (wr/w_max)*w_lim
            wl = (wl/w_max)*w_lim

        return wr, wl
    
    # Funções principais de controle
    def processControl(self, robotId, mode, func):
        func()
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

            # if (abs(gamma) + abs(theta_g)) > (np.pi):
            #     angle_to_goal = 2*(np.pi) - abs(gamma) - abs(theta_g)
            # else:
            #     angle_to_goal = abs(gamma) + abs(theta_g)

            angle_to_goal = theta_g - gamma
            angle_to_goal = (angle_to_goal + np.pi) % (2 * np.pi) - np.pi

            area = 1 # 1 - bola à frente | 2 - bola atrás

            if abs(angle_ball) > (np.pi)/2:
                area = 2
                if angle_ball >= 0:
                    angle_ball = -(np.pi - angle_ball)
                    # angle_ball = abs(angle_ball) - np.pi
                else:
                    # angle_ball = abs(angle_ball) - np.pi
                    angle_ball = np.pi - abs(angle_ball)

            if area == 2:
                dist_ball = -dist_ball
                # angle_to_goal = -angle_to_goal
            
            # print(f"rho: {round(dist_ball, 2)} cm || area: {area} || alpha: {round(self.main.convertRad2Deg(angle_ball), 2)} ° || beta: {round(self.main.convertRad2Deg(angle_to_goal), 2)} ° || gamma: {round(self.main.convertRad2Deg(gamma), 2)} ° || theta_g: {round(self.main.convertRad2Deg(theta_g), 2)} °")
            print(f"rho: {round(dist_ball, 2)} cm || area: {area} || alpha: {round(self.main.convertRad2Deg(angle_ball), 2)} ° || beta: {round(self.main.convertRad2Deg(angle_to_goal), 2)} °")
            # angle_to_goal = 0
            # print(self.main.convertRad2Deg(angle_ball))
            # print(self.main.convertRad2Deg(angle_to_goal))
            
            # Chama função para aplicar controle
            wr, wl = self.controlRobot(dist_ball, angle_ball, angle_to_goal, area)

            if (self.saving):
                self.main.e_rho = 0 - abs(dist_ball)
                self.main.e_alpha = 0 - abs(angle_ball)
                self.main.e_beta = 0 - abs(angle_to_goal)

        elif mode == 1:
            # print("Modo com Navegação")
            vector = self.navigation.createPotentialField(robotId=robotId, activeEnemies = [1, 0, 0])

            mod = np.linalg.norm(vector)
            angle_vec = np.arctan2(vector[1], vector[0])

            # print(f"vetor antes:  {vector}")

            # if(abs(mod) <= 3):
            #     print("MÓDULO PEQUENO <= 1")
            #     angle_vec += np.random.uniform(0, np.pi/72)
            #     mod = max(mod, 3)
            #     vector = [np.round(mod*np.cos(angle_vec), 8), np.round(mod*np.sin(angle_vec), 8)]
            #     print(f"vetor depois: {vector}")

            coord_plus_vec = [self.main.allies_coordinates[robotId][0] + vector[0], self.main.allies_coordinates[robotId][1] + vector[1]]

            # print(f"coord    :{self.main.allies_coordinates[robotId]}")
            # print(f"coord + v:{coord_plus_vec}")
            
            angle = self.angleBetweenObjects(coord_plus_vec, self.main.allies_coordinates[robotId], self.main.allies_direction[robotId])

            dist_ball = self.distanceBetweenObjects(self.main.ball_coordinates, self.main.allies_coordinates[robotId])
            angle_ball = self.angleBetweenObjects(self.main.ball_coordinates, self.main.allies_coordinates[robotId], self.main.allies_direction[robotId])

            # Ajuste do ângulo robô⁻bola

            if abs(angle_ball) > (np.pi)/2:
                if angle_ball >= 0:
                    angle_ball = -(np.pi - angle_ball)
                else:
                    angle_ball = np.pi - abs(angle_ball)

            area = 1 # 1 - alvo à frente | 2 - alvo atrás

            if abs(angle) > (np.pi)/2:
                area = 2
                if angle >= 0:
                    angle = -(np.pi - angle)
                else:
                    angle = np.pi - abs(angle)
            if area == 2:
                mod = -mod
            
            # print(f"F = {np.round(mod, 1)} | {np.round(np.degrees(angle_vec), 1)}° | a = {np.round(np.degrees(angle), 1)}°")

            wr, wl = self.controlRobot(mod, angle, 0, area)

            if (self.saving):
                self.main.e_rho = 0 - abs(mod)
                self.main.e_alpha = 0 - abs(angle)
                self.main.e_beta = 0

                self.main.dist_rb = 0 - abs(dist_ball)
                self.main.angle_rb = 0 - abs(angle_ball)
                self.main.angle_rbg = 0

        return wr, wl

    def controlRobot(self, rho, alpha, beta, area):
        self.kr = 0.8
        self.ka = 10
        # self.kb = -3
        self.kb = 0

        # if abs(alpha) > ((np.pi)/4):
        #     self.kr = 0.4
        #     self.ka = 4
        #     self.kb = -1

        # if abs(alpha) > ((np.pi)/4):
        #     self.kr = self.kr / 3
        #     self.ka = self.ka * 1.5
        #     self.kb = 0

        # if abs(alpha) > ((np.pi)/4):
        #     self.kr = 0.4
        #     self.ka = 15
        #     self.kb = 0

        v = self.kr*rho
        w = self.ka*alpha + self.kb*beta

        # print(f"v = {v} || w = {w}")

        if (self.main.ball_coordinates[0] > 150) or (self.main.ball_coordinates[0] < 0): # or abs(rho) < 8:
            wr = 0
            wl = 0
        else:
            wr = (v/self.r) + ((w*self.L)/(2*self.r))
            wl = (v/self.r) - ((w*self.L)/(2*self.r))

        wr, wl = self.speedLimiter(wr, wl)

        return wr, wl