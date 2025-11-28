import random
import numpy as np
from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao


class AgenteQLearning(Agente_Interface):

    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0):
        super().__init__()
        # A Tabela Q: Chave=(Estado), Valor=[Lista de Q-Values para cada ação]
        self.q_table = {}

        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate

        self.observacaoatual = None

        # --- ATUALIZAÇÃO: 8 DIREÇÕES ---
        # Definimos as 8 possibilidades de movimento (dx, dy)
        self.acoes_possiveis = [
            (0, -1), (0, 1), (1, 0), (-1, 0),  # Norte, Sul, Este, Oeste
            (1, -1), (-1, -1), (1, 1), (-1, 1)  # NE, NO, SE, SO
        ]
        self.nomes_acoes = [
            "Norte", "Sul", "Este", "Oeste",
            "Nordeste", "Noroeste", "Sudeste", "Sudoeste"
        ]

        self.ultimo_estado = None
        self.ultima_acao_idx = None
        self.learning_mode = True

    def observacao(self, observacao):
        self.observacaoanterior = self.observacaoatual if self.observacaoatual is not None else observacao
        self.observacaoatual = observacao

    def get_estado_hash(self, observacao):
        """
        Traduz os dados complexos dos sensores numa 'Assinatura' única (Tuplo)
        para usar como chave na Tabela Q.
        """
        dados = observacao.dados

        # 1. Parte da Direção (Vem do SensorLocalFarol/GPS)
        direcao = dados.get("direcao", (0, 0))

        # 2. Parte da Visão (Vem do SensorProximidade)
        visao_tuple = ()
        if "visao" in dados:
            # Converte lista de listas em tuplo de tuplos (imutável)
            visao_tuple = tuple(tuple(linha) for linha in dados["visao"])

        return (direcao, visao_tuple)

    def get_q_valores(self, estado):
        # DINÂMICO: Cria uma lista de zeros com o tamanho exato das ações possíveis
        if estado not in self.q_table:
            self.q_table[estado] = [random.random() for _ in range(len(self.acoes_possiveis))] # [0.0] * len(self.acoes_possiveis)
        return self.q_table[estado]

    def age(self):
        estado = self.get_estado_hash(self.observacaoanterior)
        q_valores = self.get_q_valores(estado)
        num_acoes = len(self.acoes_possiveis)

        # --- ESTRATÉGIA EPSILON-GREEDY ---

        # 1. EXPLORAÇÃO (Aleatório)
        if self.learning_mode and random.random() < self.epsilon:
            acao_idx = random.randint(0, num_acoes - 1)

        # 2. APROVEITAMENTO (Melhor Q-Value)
        else:
            max_val = max(q_valores)
            # Lista de índices que têm o valor máximo (para desempatar aleatoriamente)
            melhores_indices = [i for i, v in enumerate(q_valores) if v == max_val]
            acao_idx = random.choice(melhores_indices)

        # Guardar para a fase de aprendizagem
        self.ultimo_estado = estado
        self.ultima_acao_idx = acao_idx

        # Criar objeto Ação
        dx, dy = self.acoes_possiveis[acao_idx]
        return Acao("andar", dx=dx, dy=dy)

    def avaliacao_estado_atual(self, recompensa: float):
        if not self.learning_mode or self.ultimo_estado is None:
            return

        # Recuperar dados
        estado_antigo = self.ultimo_estado
        acao_idx = self.ultima_acao_idx
        estado_novo = self.get_estado_hash(self.observacaoatual)

        # Valores Q
        q_valores_antigos = self.get_q_valores(estado_antigo)
        q_valor_antigo = q_valores_antigos[acao_idx]

        # Max Q do futuro
        q_valores_novos = self.get_q_valores(estado_novo)
        max_q_novo = max(q_valores_novos)

        # --- FÓRMULA Q-LEARNING ---
        novo_valor = q_valor_antigo + self.alpha * (recompensa + self.gamma * max_q_novo - q_valor_antigo)

        # Atualizar Tabela
        self.q_table[estado_antigo][acao_idx] = novo_valor

    def cria(self, ficheiro):
        pass