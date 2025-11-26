from Ambiente.Ambient_Interface import Ambient_Interface
from Observacao import Observacao
from Acao import Acao


class AmbienteFarol(Ambient_Interface):

    def __init__(self, height=10, width=10):
        self.height = height
        self.width = width
        self.farol = (8, 8)  # O nosso "fim" ou objetivo

        # --- NOVIDADE: A Grelha de Obstáculos ---
        # Cria uma matriz vazia (0 = Livre)
        # self.mapa[x][y]
        self.mapa = [[0 for _ in range(width)] for _ in range(height)]

        self.posicoes = {}
        self.agentes = []
        self.time = 0

    def add_agente(self, agente, x=None, y=None):
        # Se não definir posição, começa no canto (0,0)
        if x is None or y is None:
            x, y = 0, 0

        # Garante que não nasce em cima de uma parede
        if self.mapa[x][y] == 1:
            print(f"AVISO: Agente tentou nascer na parede em ({x},{y})!")

        self.posicoes[agente] = (x, y)
        self.agentes.append(agente)

    # Método extra para colocar paredes no Farol
    def add_obstaculo(self, x, y):
        if 0 <= x < self.height and 0 <= y < self.width:
            # Não colocar parede em cima do Farol!
            if (x, y) != self.farol:
                self.mapa[x][y] = 1

    def observacaoPara(self, agente):
        ax, ay = self.posicoes[agente]
        fx, fy = self.farol

        obs_data = {
            "agente": (ax, ay),
            "farol": (fx, fy),  # Para o SensorLocalFarol (vetor)
            "mapa": self.mapa  # Para o SensorProximidade (obstáculos)
        }

        obs = Observacao(obs_data)

        for sensor in agente.sensores:
            obs = sensor.filtrar(obs)

        return obs

    def agir(self, acao, agente):
        ax, ay = self.posicoes[agente]

        # 1. Calcular intenção de movimento
        dx = acao.params.get("dx", 0)
        dy = acao.params.get("dy", 0)

        nx = ax + dx
        ny = ay + dy

        # 2. Validar Movimento
        movimento_valido = True

        # 2.1 Verificar Limites (Saiu do mundo?)
        if not (0 <= nx < self.height and 0 <= ny < self.width):
            movimento_valido = False

        # 2.2 Verificar Obstáculos (Bateu numa parede adicionada?)
        # Só verificamos se estiver dentro dos limites para não dar erro de índice
        elif self.mapa[nx][ny] == 1:
            movimento_valido = False

        # 3. Atualizar Posição
        if movimento_valido:
            self.posicoes[agente] = (nx, ny)
        else:
            nx, ny = ax, ay  # Fica onde estava

        # 4. Verificar Objetivo
        fx, fy = self.farol

        if (nx, ny) == (fx, fy):
            return 100.0, True

        # 5. Penalizações
        if not movimento_valido:
            return -0.5, False  # Bateu na parede ou limite

        return -0.1, False  # Custo normal

    def atualizacao(self):
        self.time += 1