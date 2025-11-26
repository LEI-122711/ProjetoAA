import tkinter as tk
import time
from Agentes.Agent_Interface import Agente_Interface


class Visualizador:
    def __init__(self, ambiente, tamanho_celula=50):
        self.ambiente = ambiente
        self.tamanho_celula = tamanho_celula

        largura = ambiente.width * tamanho_celula
        altura = ambiente.height * tamanho_celula

        # Configuração da Janela Principal
        self.root = tk.Tk()
        self.root.title("Simulador SMA - Farol")
        self.root.resizable(False, False)

        # Criar o Canvas (a tela de desenho)
        self.canvas = tk.Canvas(self.root, width=largura, height=altura, bg="white")
        self.canvas.pack()

        # Inicializar o desenho
        self.root.update()

    def desenhar(self):
        self.canvas.delete("all")

        rows = self.ambiente.height
        cols = self.ambiente.width

        for r in range(rows):
            for c in range(cols):
                x1 = c * self.tamanho_celula
                y1 = r * self.tamanho_celula
                x2 = x1 + self.tamanho_celula
                y2 = y1 + self.tamanho_celula

                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray")

        # 3. Desenhar o Farol (Círculo Amarelo)
        fx, fy = self.ambiente.farol
        self._desenhar_circulo(fx, fy, "yellow", "orange")

        # 4. Desenhar os Agentes (Quadrados Vermelhos)
        # Assumindo que self.ambiente.posicoes é {agente: (x,y)}
        for objeto, pos in self.ambiente.posicoes.items():
            ax, ay = pos

            if isinstance(objeto, Agente_Interface):
                self._desenhar_quadrado(ax, ay, "red")

        # 5. Atualizar a interface gráfica
        self.root.update()

    def _desenhar_circulo(self, x, y, cor, outline):
        padding = 5
        x1 = x * self.tamanho_celula + padding
        y1 = y * self.tamanho_celula + padding
        x2 = (x + 1) * self.tamanho_celula - padding
        y2 = (y + 1) * self.tamanho_celula - padding
        self.canvas.create_oval(x1, y1, x2, y2, fill=cor, outline=outline, width=2)

    def _desenhar_quadrado(self, x, y, cor):
        padding = 10
        x1 = x * self.tamanho_celula + padding
        y1 = y * self.tamanho_celula + padding
        x2 = (x + 1) * self.tamanho_celula - padding
        y2 = (y + 1) * self.tamanho_celula - padding
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="black")

    def fechar(self):
        self.root.destroy()