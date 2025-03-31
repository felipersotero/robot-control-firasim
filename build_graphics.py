import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation

class BuildGraphics():
    def __init__(self, Main):
        self.Main = Main  # Referência à classe principal
        self.x_data, self.y_data = [], []
        self.buildFigureAndAxes()  # Criar figura ao inicializar a classe

    def buildFigureAndAxes(self):
        """Cria a figura e os eixos do gráfico."""
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'bo-', label="Trajetória do Robô")  # Linha azul com bolinhas

        # Configurar limites do gráfico
        self.ax.set_xlim(0, 150)  # Ajuste conforme o tamanho do campo
        self.ax.set_ylim(0, 130)
        self.ax.set_xlabel("Posição X")
        self.ax.set_ylabel("Posição Y")
        self.ax.legend()

    def update(self, frame):
        """Função chamada a cada intervalo para atualizar os dados."""
        # Pega dados reais do robô

        # if self.Main.allies_coordinates[0] is not None:
        #     x = self.Main.allies_coordinates[0][0]
        #     y = self.Main.allies_coordinates[0][1]  # Supondo que seja um array com as coordenadas do robô
        
        # else:
        #     x, y = [0, 0]

        x = random.randint(0, 100)  # Simulação de coordenada X
        y = random.randint(0, 100)  # Simulação de coordenada Y

        # Adicionar os novos dados às listas
        self.x_data.append(x)
        self.y_data.append(y)

        # Atualizar a linha do gráfico
        self.line.set_data(self.x_data, self.y_data)
        
        return self.line,

    def animateGraph(self):
        """Cria a animação e exibe o gráfico."""
        ani = FuncAnimation(self.fig, self.update, interval=500, blit=False, cache_frame_data=False)
        plt.show()  # Mostrar a animação na tela
        return ani  # Retornar para evitar que o Python "mate" a animação

        # print("ANIMANDO O GRÁFICOOOOOOOOO")
