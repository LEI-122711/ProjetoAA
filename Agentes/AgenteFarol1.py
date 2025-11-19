from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao

class AgenteFarol1(Agente_Interface):

    def __init__(self):
        super().__init__()
        pass


    def observacao(self,observacao):
        for sensor in self.sensores:
            observacao = sensor.filtrar(observacao)
        self.observacaofinal = observacao
        pass

    def cria(self,ficheiro:str):
        pass

    def age(self):
        dx,dy = self.observacaofinal("direção")
        return Acao("andar",{"dx": dx,"dy": dy})

    def avaliacao_estado_atual(self,recompensa: float):

        pass