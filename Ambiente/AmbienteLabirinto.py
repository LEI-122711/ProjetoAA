from Ambiente.Ambient_Interface import Ambient_Interface
from Observacao import Observacao
from Acao import Acao


class AmbienteLabirinto(Ambient_Interface):

    def __init__(self, mapa, inicio, fim):
        """
        :param mapa: Matriz 2D onde 0 = Livre e 1 = Parede
        :param inicio: Tuplo (x, y) onde os agentes nascem por defeito
        :param fim: Tuplo (x, y) do objetivo (Saída)
        """
        self.mapa = mapa
        self.height = len(mapa)
        self.width = len(mapa[0])
        self.inicio = inicio
        self.fim = fim

        self.posicoes = {}
        self.agentes = []
        self.time = 0

    def add_agente(self, agente, x=None, y=None):
        # UNIFICAÇÃO: Se não passar coordenadas, usa o ponto de partida padrão
        if x is None or y is None:
            x, y = self.inicio

        # Proteção extra: Verificar se não está a nascer numa parede
        if self.mapa[x][y] == 1:
            print(f"AVISO CRÍTICO: Agente inserido na parede em ({x}, {y})!")

        self.posicoes[agente] = (x, y)
        self.agentes.append(agente)

    def observacaoPara(self, agente):
        ax, ay = self.posicoes[agente]
        fx, fy = self.fim

        obs_data = {
            "agente": (ax, ay),
            "saida": (fx, fy),  # Equivalente ao 'farol' no outro ambiente
            "mapa": self.mapa  # A matriz completa (Sensores vão filtrar isto)
        }

        obs = Observacao(obs_data)

        # Filtro pelos sensores instalados no agente
        for sensor in agente.sensores:
            obs = sensor.filtrar(obs)

        return obs

    def agir(self, acao, agente):
        ax, ay = self.posicoes[agente]

        # 1. Calcular a intenção de movimento
        dx = acao.params.get("dx", 0)
        dy = acao.params.get("dy", 0)

        nx = ax + dx
        ny = ay + dy

        # 2. Validar Movimento
        movimento_valido = True

        # 2.1 Verificar Limites (Saiu do Labirinto?)
        if not (0 <= nx < self.height and 0 <= ny < self.width):
            movimento_valido = False

        # 2.2 Verificar Obstáculos (Bateu na parede?)
        elif self.mapa[nx][ny] == 1:
            movimento_valido = False

        # 3. Atualizar Posição
        # Se válido move, senão fica onde estava (ax, ay)
        if movimento_valido:
            self.posicoes[agente] = (nx, ny)
        else:
            nx, ny = ax, ay

            # 4. Verificar Objetivo
        if (nx, ny) == self.fim:
            return 100.0, True  # Terminou com sucesso

        # 5. Penalizações (Reward Shaping)
        if not movimento_valido:
            return -0.5, False  # Bateu na parede (Penalização média)

        return -0.1, False  # Custo de passo (Penalização pequena)

    def atualizacao(self):
        self.time += 1