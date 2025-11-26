from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao


class AgenteLabirinto(Agente_Interface):

    def __init__(self):
        super().__init__()
        pass

    def cria(self, ficheiro: str):
        pass

    def observacao(self, observacao):
        self.observacaofinal = observacao
        pass

    def age(self):
        dx,dy = self.observacaofinal.dados["direcao"]
        return Acao("andar", dx=dx, dy=dy)

    def avaliacao_estado_atual(self, recompensa: float):
        pass