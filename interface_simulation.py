import os
import json
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Pasta onde estão os arquivos JSON
PASTA_DADOS = "./simulation_data"
# PASTA_DADOS = "./final_simulation_data"

def listar_arquivos_json():
    return [f for f in os.listdir(PASTA_DADOS) if f.endswith(".json")]

def modo_1(canvas_frame, slider_frame, arquivo_json, controles_frame):
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    for widget in slider_frame.winfo_children():
        widget.destroy()
    for widget in controles_frame.winfo_children():
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
    ax.set_aspect('equal', adjustable='box')
    # ax.set_aspect(150 / 130)
    ax.set_title("Modo 1 - Trajetória do Robô Azul 0")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    ax.plot(x_rb, y_rb, color='blue', label="Trajetória Robô")

    if x_ball and y_ball:
        ax.plot(x_ball[0], y_ball[0], 'o', color='darkorange', markersize=8, label="Bola")

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

def modo_2(canvas_frame, slider_frame, arquivo_json, controles_frame):
    import numpy as np
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    for widget in canvas_frame.winfo_children():
        widget.destroy()
    for widget in slider_frame.winfo_children():
        widget.destroy()
    for widget in controles_frame.winfo_children():
        widget.destroy()

    caminho = os.path.join(PASTA_DADOS, arquivo_json)
    with open(caminho, "r") as f:
        data = json.load(f)

    tempos = data["time"]
    e_rho = data["errors"]["e_rho"]
    e_alpha = [v * 180 / np.pi for v in data["errors"]["e_alpha"]]
    e_beta = [v * 180 / np.pi for v in data["errors"]["e_beta"]]

    fig, axs = plt.subplots(3, 1, figsize=(15, 4))
    titles = ["Erro ρ (cm)", "Erro α (graus)", "Erro β (graus)"]
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

    # Ajusta espaçamento para evitar sobreposição
    fig.tight_layout(pad=0.1)

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

def modo_3(canvas_frame, slider_frame, arquivo_json, controles_frame):
    import numpy as np
    from matplotlib.patches import Rectangle
    from matplotlib.transforms import Affine2D
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    for widget in canvas_frame.winfo_children():
        widget.destroy()
    for widget in slider_frame.winfo_children():
        widget.destroy()
    for widget in controles_frame.winfo_children():
        controles_frame.pack(side="left", fill="y", padx=10, pady=10)
        widget.destroy()

    # Criar variáveis de controle
    yellow0_var = tk.BooleanVar(value=True)
    yellow1_var = tk.BooleanVar(value=True)
    yellow2_var = tk.BooleanVar(value=True)

    # Adicionar checkboxes ao painel lateral
    ttk.Label(controles_frame, text="Exibir Robôs Amarelos").pack(anchor="w")
    ttk.Checkbutton(controles_frame, text="0", variable=yellow0_var).pack(anchor="w")
    ttk.Checkbutton(controles_frame, text="1", variable=yellow1_var).pack(anchor="w")
    ttk.Checkbutton(controles_frame, text="2", variable=yellow2_var).pack(anchor="w")

    def atualizar_amarelos():
        i = slider.get()  # posição atual do slider
        visiveis = [yellow0_var.get(), yellow1_var.get(), yellow2_var.get()]
        for j in range(3):
            if visiveis[j] and yellow_data[j]:
                x_ = yellow_data[j]["x"][:i+1]
                y_ = yellow_data[j]["y"][:i+1]
                trajetorias_amarelos[j].set_data(x_, y_)
            else:
                trajetorias_amarelos[j].set_data([], [])

        canvas.draw()

    ttk.Button(controles_frame, text="Atualizar", command=atualizar_amarelos).pack(pady=10)

    # Leitura do arquivo
    caminho = os.path.join(PASTA_DADOS, arquivo_json)
    with open(caminho, "r") as f:
        data = json.load(f)

    x_rb = data["robot_blue_0"]["x"]
    y_rb = data["robot_blue_0"]["y"]
    theta_rb = data["robot_blue_0"]["theta"]

    yellow_data = []
    for i in range(3):
        try:
            yellow_data.append({
                "x": data[f"robot_yellow_{i}"]["x"],
                "y": data[f"robot_yellow_{i}"]["y"],
                "theta": data[f"robot_yellow_{i}"]["theta"]
            })
        except KeyError:
            yellow_data.append(None)

    x_ball = data["ball"]["x"]
    y_ball = data["ball"]["y"]
    tempos = data["time"]

    lado = 7.5  # tamanho do quadrado

    fig, ax = plt.subplots(figsize=(7.5, 6))
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 130)
    ax.set_aspect('equal', adjustable='box')
    # ax.set_aspect(150/130)
    ax.set_title("Modo 3 - Trajetória dos Obstáculos")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # Trajetória do robô azul
    trajetoria_azul, = ax.plot([], [], color='blue', label="Trajetória Robô Azul")

    trajetoria_bola, = ax.plot([], [], color='darkorange', linestyle='--', label="Trajetória Bola")

    trajetorias_amarelos = []
    for i in range(3):
        line, = ax.plot([], [], color='goldenrod', linestyle='-', label=f"Trajetória Amarelo {i}")
        trajetorias_amarelos.append(line)

    # Bola (posição inicial)
    if x_ball and y_ball:
        ax.plot(x_ball[0], y_ball[0], 'o', color='darkorange', markersize=8, label="Bola")

    from matplotlib.patches import Circle

    bola_raio = 2.5
    bola_circulo = Circle((x_ball[0], y_ball[0]), radius=bola_raio,
                        color='darkorange', ec='black', zorder=5)
    ax.add_patch(bola_circulo)

    # Robôs amarelos (posição inicial)
    visiveis_iniciais = [yellow0_var.get(), yellow1_var.get(), yellow2_var.get()]

    for i in range(3):
        if not visiveis_iniciais[i]:
            continue
        try:
            x_y = data[f"robot_yellow_{i}"]["x"][0], data[f"robot_yellow_{i}"]["y"][0]
            theta = data[f"robot_yellow_{i}"]["theta"][0]
            dx, dy = theta
            angle_rad = np.arctan2(dy, dx)
            t = Affine2D().rotate_around(x_y[0], x_y[1], angle_rad)
            rect = Rectangle((x_y[0] - lado / 2, x_y[1] - lado / 2), lado, lado,
                            transform=t + ax.transData, color='yellow', alpha=0.8)
            ax.add_patch(rect)
        except KeyError:
            continue

    # Robô azul (pose inicial fixo e mais transparente)
    x0, y0 = x_rb[0], y_rb[0]
    dx0, dy0 = theta_rb[0]
    ang0 = np.arctan2(dy0, dx0)

    trans_init = Affine2D().rotate_around(x0, y0, ang0)
    azul_fixo = Rectangle((x0 - lado / 2, y0 - lado / 2), lado, lado,
                        transform=trans_init + ax.transData, color='blue', alpha=0.3)
    ax.add_patch(azul_fixo)

    # Robô azul (quadrado inicial)
    trans = Affine2D().rotate_around(x0, y0, ang0)
    azul_quad = Rectangle((x0 - lado / 2, y0 - lado / 2), lado, lado,
                          transform=trans + ax.transData, color='blue', alpha=0.8, label="Robô Azul")
    ax.add_patch(azul_quad)
    legend = ax.legend()
    legend.remove()

    # Robôs amarelos (quadrados móveis)
    amarelos_quads = []

    for i in range(3):
        if yellow_data[i]:
            x_am = yellow_data[i]["x"][0]
            y_am = yellow_data[i]["y"][0]
            dx_am, dy_am = yellow_data[i]["theta"][0]
            angle_am = np.arctan2(dy_am, dx_am)

            trans = Affine2D().rotate_around(x_am, y_am, angle_am)
            rect = Rectangle((x_am - lado / 2, y_am - lado / 2), lado, lado,
                            transform=trans + ax.transData, color='yellow', alpha=0.8)
            ax.add_patch(rect)
            amarelos_quads.append(rect)
        else:
            amarelos_quads.append(None)

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # SLIDER
    ttk.Label(slider_frame, text=f"{tempos[0]:.2f}").pack(side="left", padx=5)
    slider_val = ttk.Label(slider_frame, text=f"t = {tempos[0]:.2f} s")
    slider_val.pack(side="left")

    def on_slider_move(val):
        i = int(val)
        if i >= len(x_rb): return

        # Atualiza posição e orientação do robô azul
        x, y = x_rb[i], y_rb[i]
        dx, dy = theta_rb[i]
        angle = np.arctan2(dy, dx)
        azul_quad.set_xy((x - lado / 2, y - lado / 2))
        azul_quad.set_transform(Affine2D().rotate_around(x, y, angle) + ax.transData)

        # print(f"angle_az: {angle}")

        for j in range(3):
            if amarelos_quads[j] and yellow_data[j] and yellow0_var.get() + yellow1_var.get() + yellow2_var.get():
                if [yellow0_var, yellow1_var, yellow2_var][j].get():
                    x_am = yellow_data[j]["x"][i]
                    y_am = yellow_data[j]["y"][i]
                    dx_am, dy_am = yellow_data[j]["theta"][i]
                    angle_am = np.arctan2(dy_am, dx_am)

                    # if j == 0: print(f"angle_am[0]: {angle_am}")

                    amarelos_quads[j].set_xy((x_am - lado / 2, y_am - lado / 2))
                    amarelos_quads[j].set_transform(Affine2D().rotate_around(x_am, y_am, angle_am) + ax.transData)
                else:
                    amarelos_quads[j].set_visible(False)
            elif amarelos_quads[j]:
                amarelos_quads[j].set_visible(False)

        # Atualiza trajetória do azul até índice i
        trajetoria_azul.set_data(x_rb[:i+1], y_rb[:i+1])

        # Atualiza trajetória da bola
        trajetoria_bola.set_data(x_ball[:i+1], y_ball[:i+1])

        bola_circulo.center = (x_ball[i], y_ball[i])

        visiveis = [yellow0_var.get(), yellow1_var.get(), yellow2_var.get()]
        for j in range(3):
            if visiveis[j] and yellow_data[j]:
                x_ = yellow_data[j]["x"][:i+1]
                y_ = yellow_data[j]["y"][:i+1]
                trajetorias_amarelos[j].set_data(x_, y_)                
            else:
                trajetorias_amarelos[j].set_data([], [])


        slider_val.config(text=f"t = {tempos[i]:.2f} s")
        canvas.draw()

    # ax.legend(loc="upper right")

    slider = tk.Scale(slider_frame, from_=0, to=len(tempos) - 1,
                      orient="horizontal", length=500,
                      command=on_slider_move, showvalue=False)
    slider.pack(side="left", fill="x", expand=True)
    ttk.Label(slider_frame, text=f"{tempos[-1]:.2f}").pack(side="left", padx=5)

def modo_4(canvas_frame, slider_frame, controles_frame, arquivo_json):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from mpl_toolkits.mplot3d import Axes3D

    # Limpa canvas
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    for widget in controles_frame.winfo_children():
        widget.destroy()
    for widget in slider_frame.winfo_children():
        widget.destroy()

    # Carrega dados
    caminho = os.path.join(PASTA_DADOS, arquivo_json)
    with open(caminho, "r") as f:
        data = json.load(f)

    azul = (data["robot_blue_0"]["x"][0], data["robot_blue_0"]["y"][0])
    bola = (data["ball"]["x"][0], data["ball"]["y"][0])
    amarelos = []
    for i in range(3):
        try:
            amarelo = (data[f"robot_yellow_{i}"]["x"][0], data[f"robot_yellow_{i}"]["y"][0])
            amarelos.append(amarelo)
        except:
            continue

    # Constantes
    k_attr = 1.0
    k_rep = 100
    fator_proximidade = 1

    # Malha do campo
    x = np.linspace(0, 150, 100)
    y = np.linspace(0, 130, 100)
    X, Y = np.meshgrid(x, y)

    # Campo atrativo
    def campo_atrativo(X, Y):
        dist = np.sqrt((X - bola[0])**2 + (Y - bola[1])**2)
        campo = np.where(dist > 20, k_attr * dist, k_attr * 20)
        return campo

    # Gera o campo atrativo uma vez
    campoA = campo_atrativo(X, Y)
    max_campoA = np.max(campoA)  # valor máximo permitido para o campo repulsivo

    # Campo repulsivo
    def campo_repulsivo(X, Y):
        campo = np.zeros_like(X)
        for ox, oy in amarelos:
            d = np.sqrt((X - ox)**2 + (Y - oy)**2)
            efeito = np.where(d < 40, k_rep / (d**2 + 1e-5), 0)
            campo += efeito

        # Limita a altura do campo repulsivo
        campo = np.clip(campo, 0, max_campoA)
        return campo


    # Checkboxes para controle
    usar_attr = tk.BooleanVar(value=True)
    usar_rep = tk.BooleanVar(value=True)

    ttk.Checkbutton(controles_frame, text="Campo Atrativo", variable=usar_attr).pack(anchor="w")
    ttk.Checkbutton(controles_frame, text="Campo Repulsivo", variable=usar_rep).pack(anchor="w")

    def atualizar_campo():
        Z = np.zeros_like(X)
        if usar_attr.get():
            Z += campo_atrativo(X, Y)
        if usar_rep.get():
            Z += campo_repulsivo(X, Y)

        ax.cla()
        ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.9, edgecolor='none')

        # Pontos dos robôs e bola
        ax.scatter(azul[0], azul[1], 0, c='blue', s=50, label='Aliado')
        ax.scatter(bola[0], bola[1], 0, c='darkorange', s=50, label='Bola')
        for i, (x_am, y_am) in enumerate(amarelos):
            ax.scatter(x_am, y_am, 0, c='yellow', edgecolor='black', s=50, label=f'Rival {i}')

        ax.set_xlim(0, 150)
        ax.set_ylim(0, 130)
        ax.set_zlim(0, None)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Potencial")
        ax.set_title("Campo Potencial Virtual")
        ax.view_init(elev=40, azim=210)
        ax.legend(loc='upper right')
        canvas.draw()

    # Botão para aplicar
    ttk.Button(controles_frame, text="Atualizar Campo", command=atualizar_campo).pack(pady=10)

    # Criação da figura
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    atualizar_campo()

def modo_5(canvas_frame, controles_frame, arquivo_json):
    import os
    import json
    import numpy as np
    import tkinter as tk
    from tkinter import ttk

    # Limpar área
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    for widget in controles_frame.winfo_children():
        widget.destroy()

    caminho = os.path.join(PASTA_DADOS, arquivo_json)
    with open(caminho, "r") as f:
        data = json.load(f)

    # Pegar dados necessários
    tempos = data["time"]
    e_rho = np.array(data["errors"]["e_rho"])
    e_alpha = np.array(data["errors"]["e_alpha"])
    e_beta = np.array(data["errors"]["e_beta"])
    x_rb = np.array(data["robot_blue_0"]["x"])
    y_rb = np.array(data["robot_blue_0"]["y"])

    def rad2deg(rad):
        return rad * (180 / np.pi)

    # 1 - Tempo de percurso até |e_rho| <= 8
    perc_index = next((i for i, e in enumerate(np.abs(e_rho)) if e <= 8), len(e_rho)-1)
    tempo_percurso = tempos[perc_index]

    # 2 - Distância inicial robô–bola
    distancia_inicial = abs(e_rho[0])

    # 3 - Distância total percorrida
    distancia = 0.0
    for i in range(perc_index):
        dx = x_rb[i+1] - x_rb[i]
        dy = y_rb[i+1] - y_rb[i]
        distancia += np.sqrt(dx**2 + dy**2)

    # 4 - Velocidade angular máxima
    max_dalpha = max(abs(e_alpha[i+1] - e_alpha[i]) for i in range(len(e_alpha)-1))
    intervalo_tempo = tempos[1] - tempos[0] if len(tempos) > 1 else 1e-3
    vel_ang_max = max_dalpha / intervalo_tempo  # rad/s

    # 5 - Valor final de e_alpha
    valor_final_alpha = e_alpha[perc_index]

    # 6 - Valor final de e_beta
    valor_final_beta = e_beta[perc_index]

    # Layout
    ttk.Label(canvas_frame, text="🧮 Resultados da Simulação", font=("Arial", 14, "bold")).pack(pady=(10, 15))

    resultados = [
        f"1 - Tempo de percurso: {tempo_percurso:.2f} s",
        f"2 - Distância inicial robô-bola: {distancia_inicial:.2f} cm",
        f"3 - Distância percorrida pelo robô: {distancia:.2f} cm",
        f"4 - Velocidade angular máxima: {vel_ang_max:.2f} rad/s ({rad2deg(vel_ang_max):.2f} °/s)",
        f"5 - Valor final de e_alpha: {valor_final_alpha:.2f} rad ({rad2deg(valor_final_alpha):.2f}°)",
        f"6 - Valor final de e_beta: {valor_final_beta:.2f} rad ({rad2deg(valor_final_beta):.2f}°)"
    ]

    for r in resultados:
        ttk.Label(canvas_frame, text=r, font=("Arial", 12)).pack(anchor="w", padx=20, pady=2)

def modo_6(canvas_frame, controles_frame, arquivo_json):
    import os
    import json
    import numpy as np
    import tkinter as tk
    from tkinter import ttk

    # Limpar área
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    for widget in controles_frame.winfo_children():
        widget.destroy()

    caminho = os.path.join(PASTA_DADOS, arquivo_json)
    with open(caminho, "r") as f:
        data = json.load(f)

    # Pegar dados necessários
    tempos = data["time"]
    e_rho = np.array(data["field_errors"]["dist_rb"])
    e_alpha = np.array(data["field_errors"]["angle_rb"])
    e_beta = np.array(data["field_errors"]["angle_rbg"])
    x_rb = np.array(data["robot_blue_0"]["x"])
    y_rb = np.array(data["robot_blue_0"]["y"])

    def rad2deg(rad):
        return rad * (180 / np.pi)

    # 1 - Tempo de percurso até |e_rho| <= 8
    perc_index = next((i for i, e in enumerate(np.abs(e_rho)) if e <= 8), len(e_rho)-1)
    tempo_percurso = tempos[perc_index]

    # 2 - Distância inicial robô–bola
    distancia_inicial = abs(e_rho[0])

    # 3 - Distância total percorrida
    distancia = 0.0
    for i in range(perc_index):
        dx = x_rb[i+1] - x_rb[i]
        dy = y_rb[i+1] - y_rb[i]
        distancia += np.sqrt(dx**2 + dy**2)

    # 4 - Velocidade angular máxima
    max_dalpha = max(abs(e_alpha[i+1] - e_alpha[i]) for i in range(len(e_alpha)-1))
    intervalo_tempo = tempos[1] - tempos[0] if len(tempos) > 1 else 1e-3
    vel_ang_max = max_dalpha / intervalo_tempo  # rad/s

    # 5 - Valor final de e_alpha
    valor_final_alpha = e_alpha[perc_index]


    # Layout
    ttk.Label(canvas_frame, text="🧮 Resultados da Simulação", font=("Arial", 14, "bold")).pack(pady=(10, 15))

    resultados = [
        f"1 - Tempo de percurso: {tempo_percurso:.2f} s",
        f"2 - Distância inicial robô-bola: {distancia_inicial:.2f} cm",
        f"3 - Distância percorrida pelo robô: {distancia:.2f} cm",
        f"4 - Velocidade angular máxima: {vel_ang_max:.2f} rad/s ({rad2deg(vel_ang_max):.2f} °/s)",
        f"5 - Valor final de e_alpha: {valor_final_alpha:.2f} rad ({rad2deg(valor_final_alpha):.2f}°)",
    ]

    for r in resultados:
        ttk.Label(canvas_frame, text=r, font=("Arial", 12)).pack(anchor="w", padx=20, pady=2)

def criar_interface():
    root = tk.Tk()
    root.title("Visualização de Simulações")
    root.geometry("900x750")

    top_frame = ttk.Frame(root)
    top_frame.pack(side="top", fill="x", padx=10, pady=5)

    ttk.Label(top_frame, text="Selecione o arquivo:").pack(side="left", padx=5)
    arquivos = sorted(listar_arquivos_json())
    # print(sorted(arquivos))
    arquivo_var = tk.StringVar(value=arquivos[0] if arquivos else "")
    arquivo_menu = ttk.OptionMenu(top_frame, arquivo_var, arquivo_var.get(), *arquivos)
    arquivo_menu.pack(side="left", padx=5)

    ttk.Label(top_frame, text="Modo:").pack(side="left", padx=5)
    modo_var = tk.StringVar(value="modo 1")
    modo_menu = ttk.OptionMenu(top_frame, modo_var, "modo 1", "modo 1", "modo 2", "modo 3", "modo 4", "modo 5", "modo 6")
    modo_menu.pack(side="left", padx=5)

    def rodar_simulacao():
        modo = modo_var.get()
        arq = arquivo_var.get()

        if modo == "modo 1":
            modo_1(canvas_frame, slider_frame, arq, controles_frame)
        elif modo == "modo 2":
            modo_2(canvas_frame, slider_frame, arq, controles_frame)
        elif modo == "modo 3":
            modo_3(canvas_frame, slider_frame, arq, controles_frame)
        elif modo == "modo 4":
            modo_4(canvas_frame, slider_frame, controles_frame, arq)
        elif modo == "modo 5":
            modo_5(canvas_frame, controles_frame, arq)
        elif modo == "modo 6":
            modo_6(canvas_frame, controles_frame, arq)

    ttk.Button(top_frame, text="Rodar Simulação", command=rodar_simulacao).pack(side="left", padx=10)

    canvas_frame = ttk.Frame(root)
    canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

    slider_frame = ttk.Frame(root)
    slider_frame.pack(fill="x", padx=10, pady=5)

    # Frame lateral para controles adicionais
    # Frame lateral para controles adicionais
    controles_frame = ttk.Frame(root)
    controles_frame.pack(side="left", fill="y", padx=5, pady=5)

    root.mainloop()

criar_interface()
