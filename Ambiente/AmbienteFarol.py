from Ambiente.Ambient_Interface import Ambient_Interface
from Observacao import Observacao
from Acao import Acao
import random


class AmbienteFarol(Ambient_Interface):

    def __init__(self, height=10, width=10):
        self.height = height
        self.width = width
        self.farol = (8, 8)

        self.mapa = [[0 for _ in range(width)] for _ in range(height)]

        self.posicoes = {}
        self.agentes = []
        self.time = 0

    def add_agente(self, agente, x=None, y=None):
        if x is None or y is None:
            x, y = 0, 0

        if self.mapa[x][y] == 1:
            print(f"não começar aqui, isto é um obstáculo({x},{y})")

        self.posicoes[agente] = (x, y)
        self.agentes.append(agente)

    def add_obstaculo(self, x, y):
        if 0 <= x < self.height and 0 <= y < self.width:
            if (x, y) != self.farol:
                self.mapa[x][y] = 1

    def gerar_cenario_aleatorio(self, num_obstaculos=15):
        self.mapa = [[0 for _ in range(self.width)] for _ in range(self.height)]

        fx = random.randint(1, self.height - 1)
        fy = random.randint(1, self.width - 1)
        self.farol = (fx, fy)

        colocados = 0
        while colocados < num_obstaculos:
            ox = random.randint(0, self.height - 1)
            oy = random.randint(0, self.width - 1)

            if (ox, oy) != self.farol and (ox, oy) != (0, 0) and self.mapa[ox][oy] == 0:
                self.mapa[ox][oy] = 1
                colocados += 1

    def observacaoPara(self, agente):
        ax, ay = self.posicoes[agente]
        fx, fy = self.farol

        obs_data = {
            "agente": (ax, ay),
            "farol": (fx, fy),  #para sensordirecaoalvo
            "mapa": self.mapa   #para sensorproximidadeobstaculo
        }

        obs = Observacao(obs_data)

        for sensor in agente.sensores:
            obs = sensor.filtrar(obs)

        return obs

    def agir(self, acao, agente):
        ax, ay = self.posicoes[agente]

        dx = acao.params.get("dx", 0)
        dy = acao.params.get("dy", 0)

        nx = ax + dx
        ny = ay + dy

        movimento_valido = True

        if not (0 <= nx < self.height and 0 <= ny < self.width):
            movimento_valido = False

        #depois alterar isto porque o fora já deve mostrar como 1
        elif self.mapa[nx][ny] == 1:
            movimento_valido = False

        if movimento_valido:
            self.posicoes[agente] = (nx, ny)
        else:
            nx, ny = ax, ay  # Fica onde estava

        fx, fy = self.farol

        if (nx, ny) == (fx, fy):
            return 100.0, True

        if not movimento_valido:
            return -0.5, False  #parede ou fora dos limites

        return -0.1, False

    def atualizacao(self):
        self.time += 1