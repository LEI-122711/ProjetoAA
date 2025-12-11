import random
import numpy as np
from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao
import json


class AgenteLabirintoQLearning(Agente_Interface):

    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, dificuldade = 1):
        super().__init__()
        self.q_table = {}

        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate

        self.dificuldade_labirinto = dificuldade
        self.file = "labirintoQLearning" + str(self.dificuldade_labirinto) + ".json"

        self.acoes_possiveis = [
            (0, -1), (0, 1), (1, 0), (-1, 0),  # N, S, E, O
            (1, -1), (-1, -1), (1, 1), (-1, 1)  # NE, NO, SE, SO
        ]

        self.ultimo_estado = None
        self.ultima_acao_idx = None
        self.learning_mode = True

    def observacao(self, observacao):
        self.observacaofinal = observacao

    def get_estado_hash(self):
        #cria uma chave
        dados = self.observacaofinal.dados
        direcao = dados.get("direcao", (0, 0))

        visao_tuple = ()
        if "visao" in dados:
            #converter a matriz de visão num tuplo imutável
            visao_tuple = tuple(tuple(linha) for linha in dados["visao"])

        return (direcao, visao_tuple)

    def get_q_valores(self, estado):
        if estado not in self.q_table:
            self.q_table[estado] = [0.0] * len(self.acoes_possiveis)
        return self.q_table[estado]

    def age(self):
        estado = self.get_estado_hash()
        q_valores = self.get_q_valores(estado)
        num_acoes = len(self.acoes_possiveis)

        # aleatório
        if self.learning_mode and random.random() < self.epsilon:
            acao_idx = random.randint(0, num_acoes - 1)

        # melhor q-value
        else:
            max_val = max(q_valores)
            # desempate aleatório se dois tiverem o mesmo valor
            melhores_indices = [i for i, v in enumerate(q_valores) if v == max_val]
            acao_idx = random.choice(melhores_indices)

        self.ultimo_estado = estado
        self.ultima_acao_idx = acao_idx

        dx, dy = self.acoes_possiveis[acao_idx]
        return Acao("andar", dx=dx, dy=dy)

    def avaliacao_estado_atual(self, recompensa: float):
        if not self.learning_mode or self.ultimo_estado is None:
            return

        estado_antigo = self.ultimo_estado
        acao_idx = self.ultima_acao_idx
        estado_novo = self.get_estado_hash()

        # Atualização Q-Learning Padrão
        q_antigo = self.get_q_valores(estado_antigo)[acao_idx]
        max_q_novo = max(self.get_q_valores(estado_novo))

        novo_valor = q_antigo + self.alpha * (recompensa + self.gamma * max_q_novo - q_antigo)
        self.q_table[estado_antigo][acao_idx] = novo_valor

    def cria(self, ficheiro):
        pass

    def record_data(self, ficheiro= None):
        if ficheiro is None:
            ficheiro = self.file
        # Temos de converter as chaves (tuplos) para strings para o JSON aceitar
        dados_str = {str(k): v for k, v in self.q_table.items()}
        with open(ficheiro, "w") as f:
            json.dump(dados_str, f)
        print(f"informação em {ficheiro}")

    def load_data(self, ficheiro = None):
        if ficheiro is None:
            ficheiro = self.file
        try:
            with open(ficheiro, "r") as f:
                dados_str = json.load(f)
            # Converter strings de volta para tuplos
            # eval() é um truque rápido para converter "(1,0)" em tuplo (1,0)
            self.q_table = {eval(k): v for k, v in dados_str.items()}
            self.learning_mode = False
            self.epsilon = 0.0
            print("ficheiro encontrad")
        except FileNotFoundError:
            print("ficheiro do qlearning não encontrado")