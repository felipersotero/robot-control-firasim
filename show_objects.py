import json
import matplotlib.pyplot as plt


''' Estrutura dos dados:
    0 - aliado
    1 - bola
    2, 3, 4 - inimigos
    5 - rho e alpha
    6 - beta 
'''
def carregar_dados_json(arquivo):
    with open(arquivo, 'r') as f:
        return json.load(f)

def exibir_objetos(dados):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 130)
    ax.set_xlabel("Posição X")
    ax.set_ylabel("Posição Y")

    cores = ["blue", "orange", "yellow", "yellow", "yellow"]  # Definição das cores
    tamanho = min(len(dados), len(cores))  # Garante que temos cores suficientes

    # Plota os primeiros objetos como círculos
    for i in range(tamanho):
        x, y = dados[i]["x"], dados[i]["y"]
        ax.add_patch(plt.Circle((x, y), 2, color=cores[i], label=f"Objeto {i+1}"))

    # Plota o último objeto como um vetor a partir do primeiro ponto
    # if len(dados) > tamanho:

    x0, y0 = dados[0]["x"], dados[0]["y"]  # Origem do vetor (primeiro objeto)
    x1, y1 = dados[5]["x"], dados[5]["y"]  # Destino do vetor
    ax.arrow(x0, y0, x1, y1 , head_width=3, head_length=3, fc='red', ec='red', label="Vetor final")
    print(f"x0 = {x0}, y0 = {y0}, x1 = {x1}, y1 = {y1}")

    # x0, y0 = dados[0]["x"], dados[0]["y"]  # Origem do vetor (primeiro objeto)
    # x1_t, y1_t = dados[6]["x"], dados[6]["y"]  # Destino do vetor
    # ax.arrow(x0, y0, x1_t, y1_t , head_width=3, head_length=3, fc='red', ec='red', label="Vetor final")


    ax.legend()
    plt.grid()
    plt.show()

# Carregar e exibir os dados
dados = carregar_dados_json("simulation_data/field_data.json")
exibir_objetos(dados)
