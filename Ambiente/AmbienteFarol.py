from Ambiente.Ambient_Interface import Ambient_Interface
from Observacao import Observacao
from Acao import Acao


class AmbienteFarol(Ambient_Interface):

    def __init__(self, height = 10, width = 10):
        self.height = height
        self.width = width
        self.farol = (8,8)
        self.posicoes = {}
        self.agentes = []
        self.time = 0
        pass

    def add_agente(self, agente, x:int, y:int):
       self.posicoes[agente] = (x,y)
       self.agentes.append(agente)


    def observacaoPara(self, agente):
        ax,ay = self.posicoes[agente]
        fx,fy = self.farol

        obs = Observacao({
            "agente": (ax,ay),
            "farol": (fx,fy)
        })

        for sensor in agente.sensores:
            obs = sensor.filtrar(obs)

        #Agente.observacao(obs)

        return obs

    def agir(self, acao, agente):
        ax,ay = self.posicoes[agente]

        x = ax + acao.params.get("dx",0)
        y = ay + acao.params.get("dy",0)

        x = max(0, min(self.height - 1, x))
        y = max(0, min(self.width - 1, y))

        self.posicoes[agente] = (x,y)

        fx,fy = self.farol

        if(x,y) == (fx,fy):
            return 100,True

        return 0,False


    def atualizacao(self):
        self.time += 1
