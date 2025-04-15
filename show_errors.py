import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

# Função para converter radianos para graus
def convertRad2Deg(value):
    return value * (180 / np.pi)

# === Carregar os dados ===
with open("simulation_data/errors_data.json", "r") as f1, open("simulation_data/robot_data.json", "r") as f2:
    error_data = json.load(f1)
    robot_data = json.load(f2)

# === Extrair erros ===
y_rho = [p["e_rho"] for p in error_data]
y_alpha = [convertRad2Deg(p["e_alpha"]) for p in error_data]
y_beta = [convertRad2Deg(p["e_beta"]) for p in error_data]
x_indices = list(range(len(y_rho)))

# === Extrair posição do robô ===
x_robot = [p["x"] for p in robot_data]
y_robot = [p["y"] for p in robot_data]

# === Criar layout com GridSpec ===
fig = plt.figure(figsize=(14, 8))
gs = GridSpec(3, 2, width_ratios=[2, 1], height_ratios=[1, 1, 1])

# === Gráficos dos erros ===
axes_errors = [fig.add_subplot(gs[i, 0]) for i in range(3)]
curves = [
    axes_errors[0].plot(x_indices, y_rho, 'r', label="e_rho")[0],
    axes_errors[1].plot(x_indices, y_alpha, 'b', label="e_alpha")[0],
    axes_errors[2].plot(x_indices, y_beta, 'g', label="e_beta")[0]
]
y_labels = ["rho", "alpha (°)", "beta (°)"]

for ax, label, curve in zip(axes_errors, y_labels, curves):
    ax.set_ylabel(label)
    ax.legend()
axes_errors[2].set_xlabel("Tempo (índice)")

# === Cursor vertical e textos flutuantes ===
cursor_lines = [ax.axvline(x=0, color='k', linestyle='--') for ax in axes_errors]
value_texts = [ax.text(0.02, 0.95, '', transform=ax.transAxes, va='top', fontsize=9,
                       bbox=dict(facecolor='white', alpha=0.7)) for ax in axes_errors]

# === Gráfico da trajetória do robô ===
ax_traj = fig.add_subplot(gs[:, 1])
traj_line, = ax_traj.plot(x_robot, y_robot, '-', label="Trajetória do Robô")
robot_marker, = ax_traj.plot([], [], 'ro', markersize=8, label="Posição no instante")
ax_traj.set_xlim(0, 150)
ax_traj.set_ylim(0, 130)
ax_traj.set_aspect(150/130, adjustable='box')  # Mantém a proporção 150:130
ax_traj.set_title("Trajetória do Robô")
ax_traj.set_xlabel("X")
ax_traj.set_ylabel("Y")
ax_traj.legend()
ax_traj.grid(True)

# === Controle de clique e movimento ===
dragging = {"active": False}

def update_all(x):
    index = int(round(x))
    if 0 <= index < len(x_indices):
        # Atualizar cursores e labels
        for i, (line, text, curve) in enumerate(zip(cursor_lines, value_texts, curves)):
            y_val = curve.get_ydata()[index]
            line.set_xdata(index)
            text.set_text(f"x = {index}, y = {y_val:.2f}")

        # Atualizar marcador de posição na trajetória
        if index < len(x_robot):
            robot_marker.set_data(x_robot[index], y_robot[index])
        fig.canvas.draw_idle()

def on_click(event):
    if event.inaxes in axes_errors:
        dragging["active"] = True
        update_all(event.xdata)

def on_motion(event):
    if dragging["active"] and event.inaxes in axes_errors:
        update_all(event.xdata)

def on_release(event):
    dragging["active"] = False

# === Conectar eventos ===
fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

# === Exibir tudo ===
plt.tight_layout()
plt.show()




# import json
# import matplotlib.pyplot as plt
# import numpy as np

# # 1. Ler o arquivo JSON
# with open("errors_data.json", "r") as file:
#     data = json.load(file)

# def convertRad2Deg(value):
#     return value * (180 / np.pi)

# # 2. Extrair os dados
# y_data1 = [ponto["e_rho"] for ponto in data]
# y_data2 = [convertRad2Deg(ponto["e_alpha"]) for ponto in data]
# y_data3 = [convertRad2Deg(ponto["e_beta"]) for ponto in data]
# x_data = list(range(len(y_data1)))

# # 3. Criar figuras empilhadas
# fig, axes = plt.subplots(3, 1, sharex=True, figsize=(10, 8))
# fig.suptitle("Erros de Controle com Cursor e Labels", fontsize=14)

# # 4. Plotar os dados em cada eixo
# curves = [
#     axes[0].plot(x_data, y_data1, 'r', label="e_rho")[0],
#     axes[1].plot(x_data, y_data2, 'b', label="e_alpha")[0],
#     axes[2].plot(x_data, y_data3, 'g', label="e_beta")[0]
# ]
# y_labels = ["rho", "alpha (°)", "beta (°)"]

# for ax, ylab, curve in zip(axes, y_labels, curves):
#     ax.set_ylabel(ylab)
#     ax.legend()
# axes[2].set_xlabel("Tempo (índice)")

# # 5. Linha vertical e labels flutuantes
# cursor_lines = [ax.axvline(x=0, color='k', linestyle='--') for ax in axes]
# value_texts = [ax.text(0.02, 0.95, '', transform=ax.transAxes, va='top', fontsize=9,
#                        bbox=dict(facecolor='white', alpha=0.7)) for ax in axes]

# # 6. Controle do arrasto
# dragging = {"active": False}

# def update_cursor(x):
#     index = int(round(x))
#     if 0 <= index < len(x_data):
#         for i, (line, text, curve) in enumerate(zip(cursor_lines, value_texts, curves)):
#             y_val = curve.get_ydata()[index]
#             line.set_xdata(index)
#             text.set_text(f"x = {index}, y = {y_val:.2f}")
#         fig.canvas.draw_idle()

# def on_click(event):
#     if event.inaxes in axes:
#         dragging["active"] = True
#         update_cursor(event.xdata)

# def on_motion(event):
#     if dragging["active"] and event.inaxes in axes:
#         update_cursor(event.xdata)

# def on_release(event):
#     dragging["active"] = False

# # 7. Conectar eventos
# fig.canvas.mpl_connect('button_press_event', on_click)
# fig.canvas.mpl_connect('motion_notify_event', on_motion)
# fig.canvas.mpl_connect('button_release_event', on_release)

# # 8. Mostrar
# plt.tight_layout(rect=[0, 0, 1, 0.97])
# plt.show()

# ===================================================================================

# import json
# import matplotlib.pyplot as plt
# import numpy as np

# # 1. Ler o arquivo JSON
# with open("errors_data.json", "r") as file:
#     data = json.load(file)

# def convertRad2Deg(value):
#     return value*(180/(np.pi))

# # 2. Extrair os valores de y e gerar um eixo x com a contagem de índices
# y_data1 = [ponto["e_rho"] for ponto in data]
# y_data2 = [convertRad2Deg(ponto["e_alpha"]) for ponto in data]
# y_data3 = [convertRad2Deg(ponto["e_beta"]) for ponto in data]
# x_data = list(range(len(y_data1)))

# # 3. Criar o gráfico
# plt.figure(figsize=(8, 5))
# plt.plot(x_data, y_data1, 'r', label="Variação de Y (rho)")
# plt.plot(x_data, y_data2, 'b', label="Variação de Y (alpha)")
# plt.plot(x_data, y_data3, 'y', label="Variação de Y (beta)")

# # 4. Configuração do gráfico
# plt.xlabel("Tempo (índices)")
# plt.ylabel("Posição Y")
# plt.title("Variação da Coordenada Y ao Longo do Tempo")
# plt.legend()
# plt.grid()

# # 5. Exibir o gráfico
# plt.show()
