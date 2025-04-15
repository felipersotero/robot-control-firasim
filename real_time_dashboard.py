import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading
import random
import time

class RealTimeDashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Visualização em Tempo Real")
        self.master.geometry("900x700")

        # Dados simulados
        self.data1 = []
        self.data2 = []
        self.time_data = []

        # Criar figuras
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 6))
        self.line1, = self.ax1.plot([], [], 'b-')
        self.line2, = self.ax2.plot([], [], 'r-')

        self.ax1.set_title("Gráfico 1")
        self.ax2.set_title("Gráfico 2")

        self.ax1.set_xlim(0, 100)
        self.ax1.set_ylim(0, 100)

        self.ax2.set_xlim(0, 100)
        self.ax2.set_ylim(0, 100)

        # Embed da figura no Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Área de botões
        self.controls_frame = ttk.Frame(self.master)
        self.controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.pause_button = ttk.Button(self.controls_frame, text="⏸ Pausar", command=self.toggle_pause)
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = ttk.Button(self.controls_frame, text="🧹 Limpar", command=self.clear_data)
        self.clear_button.pack(side=tk.LEFT, padx=10)

        self.running = True
        self.paused = False

        # Iniciar thread de atualização
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_button.config(text="▶ Continuar" if self.paused else "⏸ Pausar")

    def clear_data(self):
        self.data1.clear()
        self.data2.clear()
        self.time_data.clear()
        self.line1.set_data([], [])
        self.line2.set_data([], [])
        self.canvas.draw()

    def update_loop(self):
        while self.running:
            if not self.paused:
                # Aqui você pode substituir pelos dados do simulador
                new_value1 = random.randint(0, 100)
                new_value2 = random.randint(0, 100)
                t = len(self.time_data)

                self.time_data.append(t)
                self.data1.append(new_value1)
                self.data2.append(new_value2)

                # Manter os últimos 100 pontos no gráfico
                self.time_data = self.time_data[-100:]
                self.data1 = self.data1[-100:]
                self.data2 = self.data2[-100:]

                self.line1.set_data(self.time_data, self.data1)
                self.line2.set_data(self.time_data, self.data2)

                self.ax1.set_xlim(max(0, t - 100), t + 10)
                self.ax2.set_xlim(max(0, t - 100), t + 10)

                self.canvas.draw()

            time.sleep(0.5)  # atualiza a cada 0.5s

    def on_close(self):
        self.running = False
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimeDashboard(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
