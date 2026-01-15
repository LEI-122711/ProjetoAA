from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao

class AgenteFarol1(Agente_Interface):

    def __init__(self):
        super().__init__()
        self.bussola = [
            (-1, 0), (-1, 1), (0, 1), (1, 1),
            (1, 0), (1, -1), (0, -1), (-1, -1)
        ]
        pass

    def cria(self, ficheiro: str):
        pass


    def observacao(self, observacao):
        self.observacaofinal = observacao
        pass

    def age(self):
        dados = self.observacaofinal.dados

        direcao = dados.get("direcao",(0,0))
        visao = dados.get("visao")

        dx_i, dy_i = direcao

        if (dx_i == 0 and dy_i == 0) or visao is None:
            return Acao("andar", dx=dx_i, dy=dy_i)

        try:
            start_idx = self.bussola.index(direcao)
        except ValueError:
            start_idx = 0

        # se a direção inicial estiver bloqueada (evitar paredes), roda 45 graus, tenta outra direçãoo, repete ate 8 vezes
        for i in range(8):
            idx_atual = (start_idx + i) % 8
            dx, dy = self.bussola[idx_atual]
            try:
                if visao[1 + dx][1 + dy] == 0:
                    return Acao("andar", dx=dx, dy=dy)
            except IndexError:
                pass  # Ignora se sair da matriz 3x3

        return Acao("andar", dx=dx, dy=dy)


    def avaliacao_estado_atual(self,recompensa: float):
        pass

