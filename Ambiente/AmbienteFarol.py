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

    # Coloca um novo agente no ambiente numa posição I e usa os dicionários posicoes e agentes
    def add_agente(self,agente,x:int,y:int):
       self.posicoes[agente] = (x,y)
       self.agentes[agente] = agente

    '''
    Gera a observação que o ambiente devolve ao agente -> calcula e devolve
    a posição do agente e a posição do farol dentro de um objeto.
    O agente é que terá de calcular a direção a partir destes dados
    '''
    def observacaoPara(self,Agente):
        ax,ay = self.posicoes[Agente]
        fx,fy = self.farol

        obs=  Observacao({
            "agente": (ax,ay),
            "farol": (fx,fy)
        })

<<<<<<< HEAD
    '''
    Recebe a ação escolhida pelo agente e executa no ambiente -> extrai as coordenadas do deslocamento
    da ação, calcula a nova posição, impede que o agente saia dos limites do ambiente e atualiza a posição do agente
    emk self.posicoes
    '''
=======
        for sensor in Agente.sensores:
            obs = sensor.filtrar(obs)

        #Agente.observacao(obs)

        return obs

>>>>>>> b16f01c6118bdbf643deebf165be016a00e09f27
    def agir(self,Acao,Agente):

        ax,ay = self.posicoes[Agente]

        x = ax + Acao.params.get("dx",0)
        y = ay + Acao.params.get("dy",0)

        x = max(0, min(self.height - 1, x))
        y = max(0, min(self.width - 1, y))

        self.posicoes[Agente] = (x,y)

<<<<<<< HEAD
    # Incremnete ao contador self.time
=======
        fx,fy = self.farol

        if(x,y) == (fx,fy):
            return 100,True

        return 0,False




>>>>>>> b16f01c6118bdbf643deebf165be016a00e09f27
    def atualizacao(self):
        self.time += 1
<<<<<<< HEAD
        if self.time > 10:
            self.time = 0
        pass

    '''
    Calcula a recompensa para o agente após a execução da sua ação
    Se o agente chegou a posição destino (farol) recebe +1.0
    senao -0.01 (custo por passo)

    '''

    def treat(self, agente):
        if self.posicoes[agente] == self.farol:
            return 1.0
        return -0.01   
   
=======
>>>>>>> b16f01c6118bdbf643deebf165be016a00e09f27
