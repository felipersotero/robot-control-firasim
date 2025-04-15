import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from threading import Thread
import time
import numpy as np

class InterfaceGUI:
    def __init__(self, master, data_source):
        self.master = master
        self.master.title("Monitoramento em Tempo Real")
        self.master.protocol("WM_DELETE_WINDOW", self.safe_exit)

        self.data_source = data_source  # <- recebe o objeto Main

        self.array_ally_coords_x = []
        self.array_ally_coords_y = []

        self.e_rho_array = []
        self.e_alpha_array = []
        self.e_beta_array = []

        # Criação das figuras
        self.fig1, self.ax1 = plt.subplots(figsize=(3.5, 2.5))
        self.fig2, self.ax2 = plt.subplots(figsize=(3.5, 2.5))

        # Embedding no Tkinter
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.master)
        self.canvas1.get_tk_widget().pack(side="top", fill="both", expand=True)
        
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.master)
        self.canvas2.get_tk_widget().pack(side="top", fill="both", expand=True)

        # Área de botões
        self.controls_frame = ttk.Frame(self.master)
        self.controls_frame.pack(side="bottom", fill="x")

        # ttk.Button(self.controls_frame, text="Pausar", command=self.pause).pack(side="left", padx=5)
        self.pause_button = tk.Button(self.controls_frame, text="⏸️ Pausar", command=self.toggle_pause)
        self.pause_button.pack(side=tk.LEFT, padx=10)

        ttk.Button(self.controls_frame, text="Limpar", command=self.clear).pack(side="left", padx=5)

        self.quit_button = tk.Button(self.controls_frame, text="❌ Encerrar", bg="red", fg="white", command=self.safe_exit)
        self.quit_button.pack(side=tk.RIGHT, padx=10)

        # Iniciar atualização
        self.running = True
        self.update_loop()

    def pause(self):
        self.running = not self.running

    def toggle_pause(self):
        self.running = not self.running

        if self.running == False:
            self.pause_button.config(text="▶️ Retomar", bg="gray")
            with self.data_source.lock:
                self.data_source.pause = True
        else:
            self.pause_button.config(text="⏸️ Pausar", bg="SystemButtonFace")  # Cor padrão do botão
            with self.data_source.lock:
                self.data_source.pause = False

    def clear(self):
        self.array_ally_coords_x = []
        self.array_ally_coords_y = []
        self.e_rho_array = []
        self.e_alpha_array = []
        self.e_beta_array = []
        self.ax1.cla()
        self.ax2.cla()

    def update_loop(self):

        if self.running:
            # Gráfico dos jogadores

            with self.data_source.lock:
                ball_coords = self.data_source.ball_coordinates
                ally_coords = self.data_source.allies_coordinates

            self.array_ally_coords_x.append(ally_coords[0][0])
            self.array_ally_coords_y.append(ally_coords[0][1])

            self.ax1.cla()
            self.ax1.set_xlim(0, 150)
            self.ax1.set_ylim(0, 130)

            self.ax1.set_title("Objetos")
            # self.ax1.plot(1, 1, 'ro')
            
            if ally_coords:
                self.ax1.plot(self.array_ally_coords_x, self.array_ally_coords_y, '-')

            if ball_coords[0] is not None:
                self.ax1.plot(ball_coords[0], ball_coords[1], 'ro')

            with self.data_source.lock:
                self.e_rho_array.append(self.data_source.e_rho)
                self.e_alpha_array.append(self.data_source.e_alpha*(180/(np.pi)))
                self.e_beta_array.append(self.data_source.e_beta)

            self.ax2.set_title("Erros")
            # for ally in ally_coords:
                # if ally:
                    # self.ax2.plot(ally[0], ally[1], 'bo')
            
            self.ax2.plot(self.e_rho_array, 'b-')
            self.ax2.plot(self.e_alpha_array, 'r-')

            self.canvas1.draw()
            self.canvas2.draw()

        # Atualiza a cada 200 ms
        self.master.after(50, self.update_loop)

    def safe_exit(self):
        self.data_source.stop()
        # self.master.quit()
        # self.master.destroy()
        self.master.after(100, self.master.destroy)


def start_gui(main_obj):
    root = tk.Tk()
    app = InterfaceGUI(root, main_obj)
    root.mainloop()



