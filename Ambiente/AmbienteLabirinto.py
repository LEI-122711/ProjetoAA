from Ambiente.Ambient_Interface import Ambient_Interface
from Observacao import Observacao
from Acao import Acao


class AmbienteLabirinto(Ambient_Interface):

    def __init__(self, mapa, inicio, fim):

        self.mapa = mapa
        self.height = len(mapa)
        self.width = len(mapa[0])
        self.inicio = inicio
        self.fim = fim

        self.posicoes = {}
        self.agentes = []
        self.time = 0

    def add_agente(self, agente, x=None, y=None):
        if x is None or y is None:      #p
            x, y = self.inicio

        # Proteção extra: Verificar se não está a nascer numa parede
        if self.mapa[x][y] == 1:
            print(f"não começar aqui, isto é parede({x},{y})")

        self.posicoes[agente] = (x, y)
        self.agentes.append(agente)

    def observacaoPara(self, agente):
        ax, ay = self.posicoes[agente]
        fx, fy = self.fim

        obs_data = {
            "agente": (ax, ay),
            "saida": (fx, fy),  #para o sensordirecao
            "mapa": self.mapa  # para o sensorproximidadeobstaculo
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

        # alterar como no ambiente farol
        elif self.mapa[nx][ny] == 1:
            movimento_valido = False

        if movimento_valido:
            self.posicoes[agente] = (nx, ny)
        else:
            nx, ny = ax, ay

        if (nx, ny) == self.fim:
            return 100.0, True

        if not movimento_valido:
            return -0.5, False  #parede ou fora do mapa

        return -0.1, False

    def atualizacao(self):
        self.time += 1