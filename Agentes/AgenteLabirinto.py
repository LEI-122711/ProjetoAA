from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao


class AgenteLabirinto(Agente_Interface):

    def __init__(self):
        super().__init__()

    def cria(self, ficheiro: str):
        pass

    def observacao(self, observacao):
        self.observacaofinal = observacao

    def nextPlaceEmpty(self, visao, dx, dy):
        cx, cy = self.cx, self.cy

        nx = cx + dx
        ny = cy + dy

        # limites
        if ny < 0 or ny >= len(visao):
            return False
        if nx < 0 or nx >= len(visao[0]):
            return False

        return visao[ny][nx] == 0

    def age(self):
        if self.observacaofinal is None:
            return Acao("andar", dx=0, dy=0)

        dados = self.observacaofinal.dados
        visao = dados.get("visao")
        dx_i, dy_i = dados.get("direcao", (0, 0))

        # Se já estivermos no alvo ou sem visao
        if (dx_i == 0 and dy_i == 0) or visao is None:
            return Acao("andar", dx=dx_i, dy=dy_i)

        if (dx_i, dy_i) in self.bussola:
            start_idx = self.bussola.index((dx_i, dy_i))
        else:
            # Fallback se a direção for (0,0) ou estranha
            start_idx = 0

        # 3. Ciclo de Tentativas (Rodar 45º de cada vez)
        # Agora tentamos 8 vezes para cobrir o círculo completo
        for i in range(8):
            idx_atual = (start_idx + i) % 8
            dx, dy = self.bussola[idx_atual]

            # Verificar se a célula ao redor está livre
            try:
                # Proteção de limites e verificação de parede (0 = livre)
                if self.nextPlaceEmpty(visao, dx, dy):
                    return Acao("andar", dx=dx, dy=dy)
            except:
                pass  # Ignora se sair da matriz 3x3

        # Se estiver tudo bloqueado (encurralado), tenta a ideal
        return Acao("andar", dx=dx_i, dy=dy_i)

    def avaliacao_estado_atual(self, recompensa: float):
        pass
