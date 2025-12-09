from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao


class AgenteLabirinto(Agente_Interface):

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


        self.bussola_8 = [
            self.N, self.NE, self.E, self.SE,
            self.S, self.SW, self.W, self.NW
        ]
        pass

    def cria(self, ficheiro: str):
        pass

    def observacao(self, observacao):
        self.observacaofinal = observacao

    def nextPlaceEmpty(selfself, visao, dx, dy):
        x = self.cx +dx
        y = self.cy + dy
        if y < 0 or y >= len(visao):
            return False
        if x < 0 or x >= len(visao[0]):
            return False

        return visao[y][x] == 0

    def age(self):
        if self.observacaofinal is None:
            return Acao("andar", dx=0, dy=0)

        dados = self.observacaofinal.dados
        visao = dados.get("visao")

        dx_i, dy_i = dados.get("direcao", (0, 0))

        # Se já estivermos no alvo ou sem olhos
        if (dx_i == 0 and dy_i == 0) or visao is None:
            return Acao("andar", dx=dx_i, dy=dy_i)

        start_idx = 0
        if (dx_i, dy_i) in self.bussola_8:
            start_idx = self.bussola_8.index((dx_i, dy_i))
        else:
            # Fallback se a direção for (0,0) ou estranha
            start_idx = 0

        # 3. Ciclo de Tentativas (Rodar 45º de cada vez)
        # Agora tentamos 8 vezes para cobrir o círculo completo
        for i in range(8):
            idx_atual = (start_idx + i) % 8
            dx, dy = self.bussola_8[idx_atual]

            # Verificar na matriz de visão se esta direção está livre
            # O agente está em [1][1].
            try:
                # Proteção de limites e verificação de parede (0 = livre)
                if visao[1 + dx][1 + dy] == 0:
                    return Acao("andar", dx=dx, dy=dy)
            except IndexError:
                pass  # Ignora se sair da matriz 3x3

        # Se estiver tudo bloqueado (encurralado), tenta a ideal
        return Acao("andar", dx=dx_i, dy=dy_i)

    def avaliacao_estado_atual(self, recompensa: float):
        pass