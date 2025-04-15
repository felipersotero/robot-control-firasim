import json
import matplotlib.pyplot as plt

# 1. Ler o arquivo JSON
with open("simulation_data/robot_data.json", "r") as file:
    data = json.load(file)  # Carrega os dados do JSON

# 2. Extrair listas de coordenadas X e Y
x_data = [ponto["x"] for ponto in data]
y_data = [ponto["y"] for ponto in data]

# 3. Criar o gráfico
plt.figure(figsize=(8, 6))
plt.plot(x_data, y_data, '-', label="Trajetória do Robô")  # Linha azul com pontos

# 4. Configuração do gráfico
plt.xlim(0, 150)  # Limite fixo do eixo X
plt.ylim(0, 130)  # Limite fixo do eixo Y
plt.xlabel("Posição X")
plt.ylabel("Posição Y")
plt.title("Trajetória do Robô")
plt.legend()
plt.grid()

# 5. Exibir o gráfico
plt.show()
