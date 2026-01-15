import random
from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao


class AgenteLabirinto(Agente_Interface):

    def __init__(self):
        super().__init__()
        self.observacaofinal = None

        # Estado: Qual a parede que estou a "tocar" atualmente?
        # Pode ser: None, (0, -1)[Esq], (0, 1)[Dir], (-1, 0)[Cima], (1, 0)[Baixo]
        self.parede_focada = None

        # Definição das 8 direções para movimento aleatório
        self.direcoes_possiveis = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, 1), (-1, -1), (1, 1), (1, -1)
        ]

    def cria(self, ficheiro: str):
        pass

    def observacao(self, observacao):
        self.observacaofinal = observacao

    def _tem_parede_em(self, visao, dx, dy):
        """Verifica se há parede (1) na posição relativa dx, dy"""
        try:
            return visao[1 + dx][1 + dy] == 1
        except IndexError:
            return True

    def age(self):
        if self.observacaofinal is None:
            return Acao("andar", dx=0, dy=0)

        dados = self.observacaofinal.dados
        dx_meta, dy_meta = dados.get("direcao", (0, 0))
        visao = dados.get("visao")

        if visao is None: return Acao("andar", dx=0, dy=0)

        if dx_meta == 0 and dy_meta == 0:
            return Acao("andar", dx=0, dy=0)

        if self.parede_focada is None:
            paredes_vizinhas = []
            if self._tem_parede_em(visao, -1, 0): paredes_vizinhas.append((-1, 0))
            if self._tem_parede_em(visao, 1, 0):  paredes_vizinhas.append((1, 0))
            if self._tem_parede_em(visao, 0, -1): paredes_vizinhas.append((0, -1))
            if self._tem_parede_em(visao, 0, 1):  paredes_vizinhas.append((0, 1))

            if not paredes_vizinhas:
                dx, dy = random.choice(self.direcoes_possiveis)
                if visao[1 + dx][1 + dy] == 0:
                    return Acao("andar", dx=dx, dy=dy)
                else:
                    return Acao("andar", dx=0, dy=0)
            else:
                self.parede_focada = random.choice(paredes_vizinhas)
                return Acao("andar", dx=0, dy=0)


        else:
            px, py = self.parede_focada

            dx_move, dy_move = 0, 0
            novo_foco_canto = None  # Qual será a parede depois de dobrar a esquina?

            if self.parede_focada == (0, -1):  # Parede Esquerda -> Move Baixo
                dx_move, dy_move = 1, 0
                novo_foco_canto = (-1, 0)  # Nova parede: Cima
            elif self.parede_focada == (0, 1):  # Parede Direita -> Move Cima
                dx_move, dy_move = -1, 0
                novo_foco_canto = (1, 0)  # Nova parede: Baixo
            elif self.parede_focada == (1, 0):  # Parede Baixo -> Move Direita
                dx_move, dy_move = 0, 1
                novo_foco_canto = (0, -1)  # Nova parede: Esquerda
            elif self.parede_focada == (-1, 0):  # Parede Cima -> Move Esquerda
                dx_move, dy_move = 0, -1
                novo_foco_canto = (0, 1)  # Nova parede: Direita

            # verificar canto extero
            check_x = px + dx_move
            check_y = py + dy_move

            if not self._tem_parede_em(visao, check_x, check_y):
                self.parede_focada = novo_foco_canto

                return Acao("andar", dx=check_x, dy=check_y)

            # canto interno
            if self._tem_parede_em(visao, dx_move, dy_move):
                self.parede_focada = (dx_move, dy_move)
                return Acao("andar", dx=0, dy=0)

            #caminho livre
            return Acao("andar", dx=dx_move, dy=dy_move)

    def avaliacao_estado_atual(self, recompensa: float):
        pass