from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao


class AgenteLabirinto(Agente_Interface):

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

    def nextPlaceEmpty(self, visao, dx, dy):
        h = len(visao)
        w = len (visao[0])
        cx, cy = w//2, h//2

        nx = cx + dx
        ny = cy + dy

        if not (0 <= nx < w and 0 <= ny < h):
            return False

        celula = visao[ny][nx]

        return celula == 0


    def age(self):
        if self.observacaofinal is None:
            return Acao("andar", dx = 0, dy = 0)

        dados = self.observacaofinal.dados

        direcao = dados.get("direcao", (0,0))
        dx_i, dy_i = direcao
        visao = dados.get("visao")

        if visao is None:
            return Acao("andar", dx=0, dy=0)

        start_idx = self.bussola.index((dx_i, dy_i))

        for i in range(8):
            idx_atual = (start_idx + i) % 8
            dx, dy = self.bussola[idx_atual]
            if self.nextPlaceEmpty(visao, dx, dy):
                return Acao("andar", dx=dx, dy=dy)

        return Acao("andar", dx=0, dy=0)

    def avaliacao_estado_atual(self, recompensa: float):
        pass
