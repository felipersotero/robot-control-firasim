import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def compute_potential_field(origin, destination, obstacles, k_attr=1, k_rep=200):
    x_range = np.linspace(0, 150, 100)
    y_range = np.linspace(0, 130, 100)
    X, Y = np.meshgrid(x_range, y_range)
    Z = np.zeros_like(X)
    
    # Campo atrativo
    d_attr = np.sqrt((X - destination[0])**2 + (Y - destination[1])**2)
    Z += k_attr * d_attr  # Criando um vale no destino
    
    # Campo repulsivo
    for obs in obstacles:
        d_rep = np.sqrt((X - obs[0])**2 + (Y - obs[1])**2)
        d_rep[d_rep < 1] = 1  # Evitar divisão por zero
        Z += k_rep * (1 / d_rep**2)  # Criando picos nos obstáculos
    
    return X, Y, Z

def plot_potential_field(X, Y, Z, origin, destination, obstacles):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.8)
    
    # Plotar origem, destino e obstáculos
    ax.scatter(*origin, 0, color='blue', s=100, label='Origem')
    ax.scatter(*destination, 0, color='red', s=100, label='Destino')
    for obs in obstacles:
        ax.scatter(*obs, 0, color='black', s=100, label='Obstáculo')
    
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Campo Potencial")
    ax.set_title("Campo Potencial 3D")
    plt.legend()
    plt.show()

# Carregar dados do JSON
data = load_json("simulation_data/field_data.json")

# Extrair coordenadas
origin = (data[0]["x"], data[0]["y"])  # Ponto de origem
destination = (data[1]["x"], data[1]["y"])  # Ponto de destino
obstacles = [(data[i]["x"], data[i]["y"]) for i in range(2, 5)]  # Obstáculos

# Calcular campo potencial
X, Y, Z = compute_potential_field(origin, destination, obstacles)

# Plotar campo potencial
plot_potential_field(X, Y, Z, origin, destination, obstacles)
