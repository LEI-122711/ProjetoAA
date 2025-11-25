from Ambiente.Ambient_Interface import Ambient_Interface
from Observacao import Observacao
from Acao import Acao


class AmbienteFarol(Ambient_Interface):

    def __init__(self,height = 10,width = 10):
        self.height = height
        self.width = width
        self.farol = (8,8)
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

        obs=  Observacao({
            "agente": (ax,ay),
            "farol": (fx,fy)
        })

        for sensor in Agente.sensores:
            obs = sensor.filtrar(obs)

        #Agente.observacao(obs)

        return obs

    def agir(self,Acao,Agente):

        ax,ay = self.posicoes[Agente]

        x = ax + Acao.params.get("dx",0)
        y = ay + Acao.params.get("dy",0)

        x = max(0, min(self.height - 1, x))
        y = max(0, min(self.width - 1, y))

        self.posicoes[Agente] = (x,y)

        fx,fy = self.farol

        if(x,y) == (fx,fy):
            return 100,True

        return 0,False




    def atualizacao(self):



        self.time += 1
