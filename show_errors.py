import json
import matplotlib.pyplot as plt

# 1. Ler o arquivo JSON
with open("errors_data.json", "r") as file:
    data = json.load(file)

# 2. Extrair os valores de y e gerar um eixo x com a contagem de índices
y_data1 = [ponto["e_rho"] for ponto in data]
y_data2 = [ponto["e_alpha"] for ponto in data]
y_data3 = [ponto["e_beta"] for ponto in data]
x_data = list(range(len(y_data1)))  # Criar eixo X como sequência de índices (0, 1, 2, ...)

# 3. Criar o gráfico
plt.figure(figsize=(8, 5))
plt.plot(x_data, y_data1, 'r-o', label="Variação de Y (rho)")  # Linha vermelha com pontos
plt.plot(x_data, y_data2, 'b-o', label="Variação de Y (alpha)")  # Linha vermelha com pontos
plt.plot(x_data, y_data3, 'y-o', label="Variação de Y (beta)")  # Linha vermelha com pontos

# 4. Configuração do gráfico
plt.xlabel("Tempo (índices)")
plt.ylabel("Posição Y")
plt.title("Variação da Coordenada Y ao Longo do Tempo")
plt.legend()
plt.grid()

# 5. Exibir o gráfico
plt.show()
