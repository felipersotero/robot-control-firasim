import json
import matplotlib.pyplot as plt

def carregar_dados_json(arquivo):
    """Carrega os dados de um arquivo JSON"""
    with open(arquivo, 'r') as f:
        return json.load(f)

def exibir_objetos(dados):
    """Exibe os objetos como círculos e o último como um vetor"""
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
    if len(dados) > tamanho:
        x0, y0 = dados[0]["x"], dados[0]["y"]  # Origem do vetor (primeiro objeto)
        x1, y1 = dados[-1]["x"], dados[-1]["y"]  # Destino do vetor
        ax.arrow(x0, y0, x1, y1 , head_width=3, head_length=3, fc='red', ec='red', label="Vetor final")
        print(f"x0 = {x0}, y0 = {y0}, x1 = {x1}, y1 = {y1}")

    ax.legend()
    plt.grid()
    plt.show()

# Carregar e exibir os dados
dados = carregar_dados_json("field_data.json")
exibir_objetos(dados)
