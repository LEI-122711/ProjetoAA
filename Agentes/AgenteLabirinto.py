from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao


class AgenteLabirinto(Agente_Interface):

    def __init__(self):
        super().__init__()
        self.bussola_8 = [
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

        # 1. Obter dados
        dx_ideal, dy_ideal = dados.get("direcao", (0, 0))
        visao = dados.get("visao")

        # Se já estivermos no alvo ou sem olhos
        if (dx_ideal == 0 and dy_ideal == 0) or visao is None:
            return Acao("andar", dx=dx_ideal, dy=dy_ideal)

        # 2. Encontrar o índice inicial na nossa bússola
        start_idx = 0
        if (dx_ideal, dy_ideal) in self.bussola_8:
            start_idx = self.bussola_8.index((dx_ideal, dy_ideal))
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
        return Acao("andar", dx=dx_ideal, dy=dy_ideal)

    def avaliacao_estado_atual(self, recompensa: float):
        pass