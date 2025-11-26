from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao


'''
O agente apenas observa a direção em que o farol está, e o seu objetivo e lá chegar
A observacaofinal contem a direação do farol como um par de coordenadas
Cria e retorna uma ação do tipo Acao com o nome "andar" e os parâmetros iguais as coordenadas

RESUMO: Onde quer que o farol esteja, move-te nessa direção.
'''

class AgenteFarol1(Agente_Interface):

    def __init__(self):
        super().__init__()
        pass


    def cria(self, ficheiro: str):
        pass


    def observacao(self, observacao):
        self.observacaofinal = observacao
        pass

    def age(self):
        dx,dy = self.observacaofinal.dados("direção")
        return Acao("andar",{"dx": dx,"dy": dy})
        dx,dy = self.observacaofinal.dados["direcao"]
        return Acao("andar",dx=dx,dy=dy)


    def avaliacao_estado_atual(self,recompensa: float):
        pass

    def comunica(self, msg, de_agente):
        pass

