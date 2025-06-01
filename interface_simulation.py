import os
import json
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Pasta onde estão os arquivos JSON
PASTA_DADOS = "./simulation_data"

def listar_arquivos_json():
    return [f for f in os.listdir(PASTA_DADOS) if f.endswith(".json")]

def modo_1(canvas_frame, slider_frame, arquivo_json):
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    for widget in slider_frame.winfo_children():
        widget.destroy()

    caminho = os.path.join(PASTA_DADOS, arquivo_json)
    with open(caminho, "r") as f:
        data = json.load(f)

    x_rb = data["robot_blue_0"]["x"]
    y_rb = data["robot_blue_0"]["y"]
    theta = data["robot_blue_0"]["theta"]
    x_ball = data["ball"]["x"]
    y_ball = data["ball"]["y"]
    tempos = data["time"]

    inverter_orientacao = tk.BooleanVar(value=False)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 130)
    ax.set_aspect(150 / 130)
    ax.set_title("Modo 1 - Trajetória do Robô Azul 0")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    ax.plot(x_rb, y_rb, color='blue', label="Trajetória Robô Azul 0")

    if x_ball and y_ball:
        ax.plot(x_ball[0], y_ball[0], 'o', color='darkorange', markersize=8, label="Início Bola")

    # Desenha seta inicial
    escala = 5
    seta = ax.annotate("",
        xy=(x_rb[0] + theta[0][0] * escala, y_rb[0] + theta[0][1] * escala),
        xytext=(x_rb[0], y_rb[0]),
        arrowprops=dict(arrowstyle="-|>", color="navy", lw=1.5),
        label="Robô Azul"
    )

    seta_obj = [ax.annotate(
        "",
        xy=(x_rb[0] + theta[0][0] * escala, y_rb[0] + theta[0][1] * escala),
        xytext=(x_rb[0], y_rb[0]),
        arrowprops=dict(arrowstyle="-|>", color="navy", lw=1.5),
        label="Robô Azul"
    )]

    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # CHECK BOX

    check = ttk.Checkbutton(slider_frame, text="Inverter orientação",
                            variable=inverter_orientacao,
                            onvalue=True, offvalue=False)
    check.pack(side="left", padx=10)

    # SLIDER
    ttk.Label(slider_frame, text=f"{tempos[0]:.2f}").pack(side="left", padx=5)

    slider_value_label = ttk.Label(slider_frame, text=f"t = {tempos[0]:.2f} s")
    slider_value_label.pack(side="left")

    def on_slider_move(val):
        i = int(val)
        if i >= len(x_rb):
            return
        x, y = x_rb[i], y_rb[i]
        dx, dy = theta[i]
        if inverter_orientacao.get():
            dx *= -1
            dy *= -1
        seta_obj[0].remove()
        seta_obj[0] = ax.annotate("",
            xy=(x + dx * escala, y + dy * escala),
            xytext=(x, y),
            arrowprops=dict(arrowstyle="-|>", color="navy", lw=1.5)
        )

        slider_value_label.config(text=f"t = {tempos[i]:.2f} s")
        canvas.draw()

    slider = tk.Scale(slider_frame, from_=0, to=len(tempos) - 1,
                      orient="horizontal", length=500,
                      command=on_slider_move, showvalue=False)
    slider.pack(side="left", fill="x", expand=True)

    ttk.Label(slider_frame, text=f"{tempos[-1]:.2f}").pack(side="left", padx=5)

def modo_2(canvas_frame, slider_frame, arquivo_json):
    import numpy as np
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    for widget in canvas_frame.winfo_children():
        widget.destroy()
    for widget in slider_frame.winfo_children():
        widget.destroy()

    caminho = os.path.join(PASTA_DADOS, arquivo_json)
    with open(caminho, "r") as f:
        data = json.load(f)

    tempos = data["time"]
    e_rho = data["errors"]["e_rho"]
    e_alpha = [v * 180 / np.pi for v in data["errors"]["e_alpha"]]
    e_beta = [v * 180 / np.pi for v in data["errors"]["e_beta"]]

    fig, axs = plt.subplots(1, 3, figsize=(15, 4))
    titles = ["Erro ρ", "Erro α (graus)", "Erro β (graus)"]
    dados = [e_rho, e_alpha, e_beta]
    marcadores = []

    for i in range(3):
        axs[i].plot(tempos, dados[i], color='blue')
        axs[i].set_title(titles[i])
        axs[i].set_xlabel("Tempo (s)")
        axs[i].set_ylabel("Erro")
        axs[i].grid(True)
        # Adiciona ponto marcador inicial
        marcador, = axs[i].plot(tempos[0], dados[i][0], 'ro')
        marcadores.append(marcador)

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Criação do slider e rótulos
    ttk.Label(slider_frame, text=f"{tempos[0]:.2f}").pack(side="left", padx=5)
    slider_val = ttk.Label(slider_frame, text=f"t = {tempos[0]:.2f} s")
    slider_val.pack(side="left")

    def on_slider_move(val):
        i = int(val)
        slider_val.config(text=f"t = {tempos[i]:.2f} s")
        for j in range(3):
            marcadores[j].set_data(tempos[i], dados[j][i])
        canvas.draw()

    slider = tk.Scale(slider_frame, from_=0, to=len(tempos) - 1,
                      orient="horizontal", length=500,
                      command=on_slider_move, showvalue=False)
    slider.pack(side="left", fill="x", expand=True)

    ttk.Label(slider_frame, text=f"{tempos[-1]:.2f}").pack(side="left", padx=5)

def criar_interface():
    root = tk.Tk()
    root.title("Visualização de Simulações")
    root.geometry("900x750")

    top_frame = ttk.Frame(root)
    top_frame.pack(side="top", fill="x", padx=10, pady=5)

    ttk.Label(top_frame, text="Selecione o arquivo:").pack(side="left", padx=5)
    arquivos = listar_arquivos_json()
    arquivo_var = tk.StringVar(value=arquivos[0] if arquivos else "")
    arquivo_menu = ttk.OptionMenu(top_frame, arquivo_var, arquivo_var.get(), *arquivos)
    arquivo_menu.pack(side="left", padx=5)

    ttk.Label(top_frame, text="Modo:").pack(side="left", padx=5)
    modo_var = tk.StringVar(value="modo 1")
    modo_menu = ttk.OptionMenu(top_frame, modo_var, "modo 1", "modo 1", "modo 2", "modo 3")
    modo_menu.pack(side="left", padx=5)

    def rodar_simulacao():
        modo = modo_var.get()
        arq = arquivo_var.get()

        if modo == "modo 1":
            modo_1(canvas_frame, slider_frame, arq)
        elif modo == "modo 2":
            modo_2(canvas_frame, slider_frame, arq)

    ttk.Button(top_frame, text="Rodar Simulação", command=rodar_simulacao).pack(side="left", padx=10)

    canvas_frame = ttk.Frame(root)
    canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

    slider_frame = ttk.Frame(root)
    slider_frame.pack(fill="x", padx=10, pady=5)

    root.mainloop()

criar_interface()
