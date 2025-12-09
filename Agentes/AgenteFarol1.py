from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao


'''
O agente apenas ve a direção em que o farol está, e o seu objetivo e lá chegar
A observacaofinal contem a direação do farol como um par de coordenadas
Cria e retorna uma ação do tipo Acao com o nome "andar" e os parâmetros iguais as coordenadas

RESUMO: Onde quer que o farol esteja, move-te nessa direção.
'''

class AgenteFarol1(Agente_Interface):

    def __init__(self):
        super().__init__()

        self.N = (-1,0)
        self.NE = (-1,1)
        self.E  = (0, 1)
        self.SE = (1, 1)
        self.S  = (1, 0)
        self.SW = (1, -1)
        self.W  = (0, -1)
        self.NW = (-1, -1)

        #centro d visao
        self.cx = 1
        self.cy = 1


        self.bussola_8 = [
            self.N, self.NE, self.E, self.SE,
            self.S, self.SW, self.W, self.NW
        ]
        pass


    def cria(self, ficheiro: str):
        pass


    def observacao(self, observacao):
        self.observacaofinal = observacao

    def age(self):
        dados = self.observacaofinal.dados

        #O que o agente ve: direção -> para onde deve ir; visão -> matriz
        #Le a info enviada pelo ambiente

        direcao = dados.get("direcao", (0, 0))
        visao = dados.get("visao")

        dx_i, dy_i = direcao

        #Chegamos ao destino ou não temos visão
        if (dx_i == 0 and dy_i == 0) or visao is None:
            return Acao("andar", dx=dx_i, dy=dy_i)

        '''
        se direçao = (0,0) ja chegamos ao farol
        se visão nao existe nao é possivel evitar paredes entao segue a direção
        '''

        start_idx = 0
        if (direcao) in self.bussola_8:
            start_idx = self.bussola_8.index(direcao)
        else:
            start_idx = 0

        # se a direção inicial estiver bloqueada (evitar paredes)
        # roda 45 graus, tenta outra d, repete ate 8 vezes



        for i in range(8):
            idx_atual = (start_idx + i) % 8
            dx, dy = self.bussola_8[idx_atual]


            try:
                if visao[cx + dx][cy + dy] == 0:
                    return Acao("andar", dx=dx, dy=dy)
            except IndexError:
                pass  # Ignora se sair da matriz 3x3


        return Acao("andar", dx=dx_i, dy=dy_i)


    def avaliacao_estado_atual(self,recompensa: float):
        pass

