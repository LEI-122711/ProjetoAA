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
        dx, dy = dados.get("direcao", (0, 0))
        visao = dados.get("visao")

        # Se já estivermos no alvo ou sem olhos
        if (dx == 0 and dy == 0) or visao is None:
            return Acao("andar", dx=dx, dy=dy)

        # 2. Encontrar o índice inicial na nossa bússola
        start_idx = 0
        if (dx, dy) in self.bussola_8:
            start_idx = self.bussola_8.index((dx, dy))
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
        return Acao("andar", dx=dx, dy=dy)


    def avaliacao_estado_atual(self,recompensa: float):
        pass

