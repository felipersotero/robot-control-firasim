import numpy as np
import json

class Navigation():
    def __init__(self, Control):
        self.ball_coordinates = Control.ball_coordinates
        self.allies_coordinates = Control.allies_coordinates
        self.allies_direction = Control.allies_direction
        self.allies_angles = Control.allies_angles
        self.allies_angles_deg = Control.allies_angles_deg
        self.enemies_coordinates = Control.enemies_coordinates

        self.vision = Control.vision
        self.test_field_data = Control.test_field_data

        self.data = [None, None, None, None, None, None]

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

    def calculateAttractiveForce(self, gain, source_coordinates, target_coordinates):

        vector = [target_coordinates[0] - source_coordinates[0], target_coordinates[1] - source_coordinates[1]]
        mod = np.linalg.norm(vector)
        vector_norm = vector/mod

        vector_result = gain*mod*vector_norm

        return vector_result

    def calculateRepulsiveForces(self, gain, area, source_coordinates, obstacles_coordinates):

        vector_result = [0, 0]
        for obstacle in obstacles_coordinates:
            vector = [obstacle[0] - source_coordinates[0], obstacle[1] - source_coordinates[1]]
            mod = np.linalg.norm(vector)
            vector_norm = vector/mod

            if mod <= area:
               vector_result = vector_result + (gain*(1/(mod**2))*vector_norm)

        return vector_result

    def createPotentialField(self, robotId):
        
        self.getFieldData()

        obstacles_coordinates = []

        attractiveForce = self.calculateAttractiveForce(0.5, self.allies_coordinates[robotId], self.ball_coordinates)

        self.saveData(0, self.allies_coordinates[robotId][0], self.allies_coordinates[robotId][1])
        self.saveData(1, self.ball_coordinates[0], self.ball_coordinates[1])

        for i, enemy in enumerate(self.enemies_coordinates, start=2):
            obstacles_coordinates.append(enemy)
            self.saveData(i, enemy[0], enemy[1])

        repulsiveForce = self.calculateRepulsiveForces(10000, 50, self.allies_coordinates[robotId], obstacles_coordinates)

        resulting_force = attractiveForce - repulsiveForce

        self.saveData(5, resulting_force[0], resulting_force[1])
        # self.saveData(5, 1, 1)

        return resulting_force

    # Funções para salvar dados
    def saveData(self, i, x, y):
        self.data[i] = {"x": x, "y": y}
        print(f"Salvando dados... {x}, {y}")
        print(self.data)

    def saveData2JSON(self):
        # Salvar em arquivo JSON ao final da execução
        with open("field_data.json", "w") as file:
            json.dump(self.data, file, indent=4)
            print("Dados salvos!")
            print(self.data)

