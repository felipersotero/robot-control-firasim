import numpy as np
import json

class Navigation():
    def __init__(self, Control):
        # self.ball_coordinates = Control.ball_coordinates
        self.allies_coordinates = Control.main.allies_coordinates
        self.allies_direction = Control.main.allies_direction
        self.allies_angles = Control.main.allies_angles
        self.allies_angles_deg = Control.main.allies_angles_deg
        self.enemies_coordinates = Control.main.enemies_coordinates

        self.vision = Control.vision
        self.test_field_data = Control.test_field_data

        self.saving = Control.saving

        self.data = [None, None, None, None, None, None]

        # Dimensões do campo
        self.field_x = 150
        self.field_y = 130

        self.consider_walls = True
        self.noise_added = False


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
            # Atualiza os dados do campo
            self.vision.update()

            # Converte e salva os dados nas variváveis
            self.ball_coordinates = [self.convertXValues(self.test_field_data.ball.position.x), self.convertYValues(self.test_field_data.ball.position.y)]

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

    # FUNÇÕES DE NAVEGAÇÃO POR CAMPOS POTENCIAIS
    def calculateAttractiveForce(self, gain, source_coordinates, target_coordinates):
        vector = [target_coordinates[0] - source_coordinates[0], target_coordinates[1] - source_coordinates[1]]
        mod = np.linalg.norm(vector)
        vector_norm = vector/mod

        # Goodrich
        # vector_result = gain*200*vector_norm

        # if mod <= 50:
        #     vector_result = gain*mod*vector_norm

        # Goodrich adaptado
        vector_result = gain*mod*vector_norm
        if mod <= 20:
            vector_result = gain*20*vector_result

        return vector_result

    def calculateRepulsiveForces(self, gain, area, source_coordinates, obstacles_coordinates, activeEnemies, ball_coords):
        vector_result = [0, 0]

        robot_x = source_coordinates[0]
        robot_y = source_coordinates[1]

        ball_x = ball_coords[0]
        ball_y = ball_coords[1]

        distance_rb = np.linalg.norm([ball_x - source_coordinates[0], ball_y - source_coordinates[1]])
        factor = 1

        for i, obstacle in enumerate(obstacles_coordinates):
            if activeEnemies[i] == 1:
                # print(f"inimigo {i}")
                vector = [obstacle[0] - robot_x, obstacle[1] - robot_y]
                mod = np.linalg.norm(vector)
                vector_norm = vector/mod

                # Goodrich adaptado
                if mod <= area:
                   vector_result = vector_result + (gain*(1/(mod**2))*vector_norm)
                   if distance_rb >= 80:
                       factor = 0.6

                if mod <= (10):
                   vector_result = vector_result + (gain*1000*(1/(mod**2))*vector_norm)

                # if mod <= area:
                #    vector_result = vector_result + (80-mod)*vector_norm

        # if self.consider_walls:
        #     if robot_x < 10 and robot_x != 0:
        #         vector_result[0] = vector_result[0] - 15
        #     elif robot_x > (self.field_x - 10):
        #         vector_result[0] = vector_result[0] + 15

        #     if robot_y < 10:
        #         vector_result[1] = vector_result[1] - 15
        #     elif robot_y > (self.field_y - 10):
        #         vector_result[1] = vector_result[1] + 15

        # Desvio das paredes NOVO
        if self.consider_walls:
            if robot_x < 10 and robot_x != 0:
                if not(ball_x < 10):
                    vector_result[0] = vector_result[0] - 15
                else:
                    vector_result[0] = vector_result[0] - 5
            elif robot_x > (self.field_x - 10):
                if not(ball_x > (self.field_x - 10)):
                    vector_result[0] = vector_result[0] + 15
                else:
                    vector_result[0] = vector_result[0] + 5

            if robot_y < 10:
                if not(ball_y < 10):
                    vector_result[1] = vector_result[1] - 15
                else:
                    vector_result[1] = vector_result[1] - 5
            elif robot_y > (self.field_y - 10):
                if not(ball_y > (self.field_y - 10)):
                    vector_result[1] = vector_result[1] + 15
                else:
                    vector_result[1] = vector_result[1] + 5
        
        return vector_result, factor

    def createPotentialField(self, robotId, activeEnemies):
        
        self.getFieldData()

        obstacles_coordinates = []

        attractiveForce = self.calculateAttractiveForce(0.6, self.allies_coordinates[robotId], self.ball_coordinates)
        factor = 1

        if (self.saving): self.saveData(0, self.allies_coordinates[robotId][0], self.allies_coordinates[robotId][1])
        if (self.saving): self.saveData(1, self.ball_coordinates[0], self.ball_coordinates[1])

        for i, enemy in enumerate(self.enemies_coordinates, start=2):
            obstacles_coordinates.append(enemy)
            if (self.saving): self.saveData(i, enemy[0], enemy[1])

        repulsiveForce, factor = self.calculateRepulsiveForces(4500, 40, self.allies_coordinates[robotId], obstacles_coordinates, activeEnemies, self.ball_coordinates, )
        factor = 1 # retirar isso se quiser evitar problema de campo atrativo alto e colisões
        resulting_force = factor*attractiveForce - repulsiveForce
        
        print(factor)
        print(resulting_force)
        resulting_force_mod = np.linalg.norm(resulting_force)
        resulting_force_angle = np.arccos(np.clip(np.dot(resulting_force,[1,0])/np.linalg.norm(resulting_force), -1.0, 1.0))

        # if resulting_force_mod <= 3:
        #     # resulting_force = 5*attractiveForce - repulsiveForce
        #     print("MÓDULO PEQUENO <= 1")
        #     resulting_force_angle += np.random.uniform(0, np.pi/72)

        #     resulting_force_mod = max(resulting_force_mod, 3)
        #     resulting_force = [np.round(resulting_force_mod*np.cos(resulting_force_angle), 8), np.round(resulting_force_mod*np.sin(resulting_force_angle), 8)]

        
        # if resulting_force_mod <= 1:
        #     resulting_force_angle = resulting_force_angle*1.1 # + (0.01*np.sign(resulting_force_angle)) # noise*np.sign(resulting_force_angle)

        #     print(f"F = {np.round(resulting_force_mod, 2)} | {np.round(np.degrees(resulting_force_angle), 2)}°")

        #     dx = np.cos(resulting_force_angle)
        #     dy = np.sin(resulting_force_angle)

        #     resulting_force = [resulting_force_mod*1.5*dx, resulting_force_mod*1.5*dy]

        #     resulting_force_mod = np.linalg.norm(resulting_force)
        #     resulting_force_angle = np.arccos(np.clip(np.dot(resulting_force,[1,0])/np.linalg.norm(resulting_force), -1.0, 1.0))

        #     print(f"F = {np.round(resulting_force_mod, 2)} | {np.round(np.degrees(resulting_force_angle), 2)}°")

        #     noise = np.random.uniform(0, (np.pi/4))/10

        #     resulting_force_angle = resulting_force_angle + (0.01*np.sign(resulting_force_angle)) # noise*np.sign(resulting_force_angle)

        #     dx = np.cos(resulting_force_angle)
        #     dy = np.sin(resulting_force_angle)

        #     resulting_force = [resulting_force_mod*dx, resulting_force_mod*dy]

        # print("#####################################")
        # print(f"F = {np.round(resulting_force_mod, 1)} | {np.round(np.degrees(resulting_force_angle), 1)}°")


        # Adição de ruídos angulares
        # if not self.noise_added:
        #     if resulting_force_mod <= 1:
        #         self.noise_added = True

        #         ruido_magnitude = 0.01 * np.linalg.norm(resulting_force)
        #         # Ruído (pequeno vetor aleatório)
        #         ruido = np.random.uniform(-1, 1, size=2)
        #         ruido = ruido / np.linalg.norm(ruido) * ruido_magnitude  # normaliza e escala

        #         # Novo vetor resultante com ruído
        #         resulting_force = resulting_force + ruido

        # if resulting_force_mod > 1:
        #     self.noise_added = False

        return resulting_force

    # FUNÇÕES DE NAVEGAÇÃO POR GRIDS

    # Funções para salvar dados
    def saveData(self, i, x, y):
        self.data[i] = {"x": x, "y": y}
        # print(f"Salvando dados... {x}, {y}")
        # print(self.data)

    def saveData2JSON(self):
        # Salvar em arquivo JSON ao final da execução
        with open("simulation_data/field_data.json", "w") as file:
            json.dump(self.data, file, indent=4)
            # print("Dados salvos!")
            # print(self.data)

