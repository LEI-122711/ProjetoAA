import tkinter as tk
from Agentes.Agent_Interface import Agente_Interface
from PIL import ImageGrab
import platform  # Para detetar se é Mac


class Visualizador:
    def __init__(self, ambiente, max_tamanho_janela=800, gravar_gif=False):
        self.ambiente = ambiente
        self.gravar_gif = gravar_gif
        self.frames = []

        # Dimensões do mapa
        self.cols = getattr(ambiente, 'width', 10)
        self.rows = getattr(ambiente, 'height', 10)

        # CÁLCULO DINÂMICO DA CÉLULA
        cell_w = max_tamanho_janela // self.cols
        cell_h = max_tamanho_janela // self.rows
        self.tamanho_celula = min(cell_w, cell_h)
        self.tamanho_celula = max(10, self.tamanho_celula)

        largura = self.cols * self.tamanho_celula
        altura = self.rows * self.tamanho_celula

        self.root = tk.Tk()
        self.root.title(f"Simulador SMA - Mapa {self.cols}x{self.rows}")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=largura, height=altura, bg="white")
        self.canvas.pack()

        # Força a atualização da geometria da janela para termos coordenadas corretas
        self.root.update_idletasks()
        self.root.update()

    def desenhar(self):
        self.canvas.delete("all")

        tem_mapa = hasattr(self.ambiente, 'mapa') and self.ambiente.mapa is not None

        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.tamanho_celula
                y1 = r * self.tamanho_celula
                x2 = x1 + self.tamanho_celula
                y2 = y1 + self.tamanho_celula

                self.canvas.create_rectangle(x1, y1, x2, y2, outline="lightgray")

                if tem_mapa and self.ambiente.mapa[r][c] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="gray")

        # Desenhar Objetivo
        alvo = None
        if hasattr(self.ambiente, 'farol'):
            alvo = self.ambiente.farol
        elif hasattr(self.ambiente, 'fim'):
            alvo = self.ambiente.fim

        if alvo:
            fx, fy = alvo
            self._desenhar_circulo(fx, fy, "gold", "orange")

        # Desenhar Agentes
        for objeto, pos in self.ambiente.posicoes.items():
            ax, ay = pos
            if isinstance(objeto, Agente_Interface):
                self._desenhar_quadrado(ax, ay, "red")

        self.root.update()

        # --- CAPTURAR FRAME PARA GIF (CORRIGIDO PARA RETINA/MAC) ---
        if self.gravar_gif:
            try:
                # 1. Obter coordenadas da janela no ecrã (Lógicas)
                x = self.root.winfo_rootx() + self.canvas.winfo_x()
                y = self.root.winfo_rooty() + self.canvas.winfo_y()
                w = self.canvas.winfo_width()
                h = self.canvas.winfo_height()

                x1 = x + w
                y1 = y + h

                # 2. Correção para ecrãs Retina (Mac)
                # O ImageGrab usa pixeis físicos, o Tkinter usa pontos lógicos.
                # Normalmente a escala é 2x.
                if platform.system() == "Darwin":
                    x *= 1
                    y *= 1
                    x1 *= 1
                    y1 *= 1

                # Captura
                imagem = ImageGrab.grab(bbox=(x, y, x1, y1))
                self.frames.append(imagem)
            except Exception as e:
                print(f"Erro ao capturar frame: {e}")

    def _desenhar_circulo(self, x, y, cor, outline):
        padding = self.tamanho_celula * 0.1
        pixel_x = y * self.tamanho_celula
        pixel_y = x * self.tamanho_celula
        x1 = pixel_x + padding
        y1 = pixel_y + padding
        x2 = pixel_x + self.tamanho_celula - padding
        y2 = pixel_y + self.tamanho_celula - padding
        self.canvas.create_oval(x1, y1, x2, y2, fill=cor, outline=outline, width=2)

    def _desenhar_quadrado(self, x, y, cor):
        padding = self.tamanho_celula * 0.2
        pixel_x = y * self.tamanho_celula
        pixel_y = x * self.tamanho_celula
        x1 = pixel_x + padding
        y1 = pixel_y + padding
        x2 = pixel_x + self.tamanho_celula - padding
        y2 = pixel_y + self.tamanho_celula - padding
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="black")

    def salvar_gif(self, nome_ficheiro="simulacao.gif"):
        if not self.frames:
            print("Nenhum frame capturado para salvar.")
            return

        print(f"A guardar GIF: {nome_ficheiro} ({len(self.frames)} frames)...")
        self.frames[0].save(
            nome_ficheiro,
            save_all=True,
            append_images=self.frames[1:],
            optimize=True,
            duration=100,  # 100ms por frame = 10fps
            loop=0
        )
        print("GIF guardado com sucesso!")

    def fechar(self):
        self.root.destroy()