from Ambiente.Ambient_Interface import Ambient_Interface
from Observacao import Observacao
from Acao import Acao


class AmbienteLabirinto(Ambient_Interface):

    def __init__(self, mapa, inicio, fim):
        self.mapa = mapa    # matriz com 0(livre) e 1(parede)
        self.height = len(mapa)
        self.width = len(mapa[0])
        self.inicio = inicio
        self.fim = fim
        self.posicoes = {}
        self.agentes = []
        self.time = 0

    def add_agente(self, agente):
        self.posicoes[agente] = self.inicio
        self.agentes.append(agente)

    def observacaoPara(self, agente):                            #devolver o que os sensores veem e enviar para o agente
        ax, ay = self.posicoes[agente]  #posição do agente
        fx, fy = self.fim   #posição da saída
        mapa = self.mapa

        obs_data = {
            "agente": (ax, ay),
            "saida": (fx, fy),
        }

        obs = Observacao(obs_data)
        for sensor in agente.sensores:
            obs = sensor.filtrar(obs)

        return obs

    def agir(self, acao, agente):
        ax,ay = self.posicoes[agente]

        novo_x = ax + acao.params.get("dx", 0)
        novo_y = ay + acao.params.get("dy", 0)

        # Verifica limites
        if 0 <= novo_x < self.height and 0 <= novo_y < self.width:
            pass
        else:
            return 0, False

        # Verifica se é parede
        if self.mapa[novo_x][novo_y] == 1:
            return 0, False

        # se a posição é válida, atualiza
        self.posicoes[agente] = (novo_x, novo_y)

        # Verifica se chegou ao fim
        if (novo_x, novo_y) == self.fim:
            return 100, True
        return 0, False

    def atualizacao(self):
        self.time += 1
