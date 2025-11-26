import tkinter as tk
from Agentes.Agent_Interface import Agente_Interface


class Visualizador:
    def __init__(self, ambiente, tamanho_celula=50):
        self.ambiente = ambiente
        self.tamanho_celula = tamanho_celula

        # Tenta obter width/height, assume nomes padrão se falhar
        self.cols = getattr(ambiente, 'width', 10)
        self.rows = getattr(ambiente, 'height', 10)

        largura = self.cols * tamanho_celula
        altura = self.rows * tamanho_celula

        # Configuração da Janela Principal
        self.root = tk.Tk()
        self.root.title("Simulador SMA - Unificado")
        self.root.resizable(False, False)

        # Criar o Canvas (a tela de desenho)
        self.canvas = tk.Canvas(self.root, width=largura, height=altura, bg="white")
        self.canvas.pack()

        # Inicializar o desenho
        self.root.update()

    def desenhar(self):
        # 1. Limpar o desenho anterior
        self.canvas.delete("all")

        # 2. Desenhar a Grelha e OBSTÁCULOS
        # Verifica se o ambiente tem a matriz 'mapa'
        tem_mapa = hasattr(self.ambiente, 'mapa') and self.ambiente.mapa is not None

        for r in range(self.rows):  # x (height)
            for c in range(self.cols):  # y (width)
                x1 = c * self.tamanho_celula
                y1 = r * self.tamanho_celula
                x2 = x1 + self.tamanho_celula
                y2 = y1 + self.tamanho_celula

                # Desenha o quadrado base (grelha)
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray")

                # Se houver mapa e a célula for 1, pinta de PRETO (Parede)
                # Nota: A matriz costuma ser mapa[x][y], onde x=rows e y=cols
                if tem_mapa and self.ambiente.mapa[r][c] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="gray")

        # 3. Desenhar o Objetivo (Farol ou Saída)
        # Tenta encontrar onde está o objetivo procurando pelos nomes comuns
        alvo = None
        if hasattr(self.ambiente, 'farol'):
            alvo = self.ambiente.farol
        elif hasattr(self.ambiente, 'fim'):
            alvo = self.ambiente.fim

        if alvo:
            fx, fy = alvo
            # Desenha Círculo Amarelo
            self._desenhar_circulo(fx, fy, "yellow", "orange")

        # 4. Desenhar os Agentes
        # Percorre o dicionário de posições
        for objeto, pos in self.ambiente.posicoes.items():
            ax, ay = pos

            # Verifica se é um Agente (para pintar de vermelho)
            if isinstance(objeto, Agente_Interface):
                self._desenhar_quadrado(ax, ay, "red")

            # Se quiseres desenhar outros objetos no futuro, adiciona 'elif' aqui

        # 5. Atualizar a interface gráfica
        self.root.update()

    def _desenhar_circulo(self, x, y, cor, outline):
        # x é a linha (altura), y é a coluna (largura) ou vice-versa?
        # ATENÇÃO: No Tkinter, x é horizontal (coluna), y é vertical (linha).
        # Mas na tua matriz self.mapa[x][y], x costuma ser a linha e y a coluna.
        # Vamos assumir: self.posicoes[(linha, coluna)] -> Tkinter(coluna, linha)

        padding = 5
        # Troca de coordenadas para desenhar: pixel_x = coluna * tamanho, pixel_y = linha * tamanho
        pixel_x = y * self.tamanho_celula
        pixel_y = x * self.tamanho_celula

        x1 = pixel_x + padding
        y1 = pixel_y + padding
        x2 = pixel_x + self.tamanho_celula - padding
        y2 = pixel_y + self.tamanho_celula - padding

        self.canvas.create_oval(x1, y1, x2, y2, fill=cor, outline=outline, width=2)

    def _desenhar_quadrado(self, x, y, cor):
        padding = 10
        # Troca de coordenadas: input x,y (linha,coluna) -> desenho pixel_x, pixel_y (coluna, linha)
        pixel_x = y * self.tamanho_celula
        pixel_y = x * self.tamanho_celula

        x1 = pixel_x + padding
        y1 = pixel_y + padding
        x2 = pixel_x + self.tamanho_celula - padding
        y2 = pixel_y + self.tamanho_celula - padding

        self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="black")

    def fechar(self):
        self.root.destroy()