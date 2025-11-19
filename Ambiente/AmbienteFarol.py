from Ambiente.Ambient_Interface import Ambient_Interface
from Observacao import Observacao
from Acao import Acao


class AmbienteFarol(Ambient_Interface):

    def __init__(self,height = 5,weight = 5):
        self.height = height
        self.weight = weight
        self.farol = (3,3)
        self.posicoes = {}
        self.agentes = {}
        self.time = 0
        pass

    def add_agente(self,agente,x:int,y:int):
       self.posicoes[agente] = (x,y)
       self.agentes[agente] = agente


    def observacaoPara(self,Agente):
        ax,ay = self.posicoes[Agente]
        fx,fy = self.farol

        return Observacao({
            "agente": (ax,ay),
            "farol": (fx,fy)
        })

    def agir(self,Acao,Agente):
        ax,ay = self.posicoes[Agente]

        x = ax + Acao.params.get("dx",0)
        y = ay + Acao.params.get("dy",0)

        x = max(0, min(self.height - 1, x))
        y = max(0, min(self.weight - 1, y))

        self.posicoes[Agente] = (x,y)


    def atualizacao(self):



        self.time += 1
        if self.time > 10:
            self.time = 0
        pass