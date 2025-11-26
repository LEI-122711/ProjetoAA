import random
from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao


class AgenteFarolQLearning(Agente_Interface):

    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0):
        super().__init__()
        self.q_table = {}

        # Parâmetros de Aprendizagem
        self.alpha = learning_rate  # O quão rápido aprende
        self.gamma = discount_factor  # O quanto valoriza o futuro
        self.epsilon = exploration_rate  # Probabilidade de explorar

        # Memória do último passo (para poder aprender)
        self.ultimo_estado = None
        self.ultima_acao = None

        # Modo: True = Aprende, False = Teste (Usa o que sabe)
        self.learning_mode = True


    def observacao(self, observacao):
        # Transforma a observação num formato que possa ser chave de dicionário (tuplo)
        # Ex: O estado passa a ser ((1, 0),) ou algo único
        self.observacaofinal = observacao

    def get_estado_atual(self):
        # Define o que é o "Estado".
        # No teu caso, é a direção que o sensor vê.
        # Retorna um tuplo para ser imutável e servir de chave.
        dados = self.observacaofinal.dados["direcao"]
        return tuple(dados)

    def get_q_value(self, estado, acao_tipo):
        # Retorna o valor da tabela. Se não existir, retorna 0.0
        return self.q_table.get((estado, acao_tipo), 0.0)

    def age(self):
        estado = self.get_estado_atual()
        acoes_possiveis = ["Norte", "Sul", "Este", "Oeste","Noroeste","Nordeste","Sudeste","Sudoeste"]
        dx_dy = {"Norte": (0, -1), "Sul": (0, 1), "Este": (1, 0), "Oeste": (-1, 0),"Nordeste": (1,-1),"Noroeste": (-1,-1),"Sudeste":(1,1),"Sudoeste": (-1,1)}

        # --- ESTRATÉGIA EPSILON-GREEDY ---

        # 1. EXPLORAÇÃO: Se estiver em modo treino e calhar o número aleatório
        if self.learning_mode and random.random() < self.epsilon:
            acao_escolhida = random.choice(acoes_possiveis)

        # 2. APROVEITAMENTO (Exploitation): Escolhe a melhor da tabela
        else:
            valores = [self.get_q_value(estado, a) for a in acoes_possiveis]
            max_valor = max(valores)

            # Se houver empate entre as melhores, escolhe uma delas à sorte
            melhores_acoes = [a for a, v in zip(acoes_possiveis, valores) if v == max_valor]
            acao_escolhida = random.choice(melhores_acoes)

        # Guardar o que fizemos para usar na 'avaliacao' (recompensa)
        self.ultimo_estado = estado
        self.ultima_acao = acao_escolhida

        # Converter para o objeto Acao do teu projeto
        vals = dx_dy[acao_escolhida]
        return Acao("andar", dx=vals[0], dy=vals[1])

    def avaliacao_estado_atual(self, recompensa: float):
        if not self.learning_mode:
            return  # Se estiver em teste, não atualiza a tabela

        # Recuperar o que aconteceu
        estado_anterior = self.ultimo_estado
        acao_anterior = self.ultima_acao
        estado_novo = self.get_estado_atual()

        # 1. Obter o valor antigo da tabela Q(s, a)
        q_antigo = self.get_q_value(estado_anterior, acao_anterior)

        # 2. Calcular o valor máximo do novo estado max Q(s', a')
        acoes_possiveis = ["Norte", "Sul", "Este", "Oeste", "Noroeste", "Nordeste", "Sudeste", "Sudoeste"]
        max_q_novo = max([self.get_q_value(estado_novo, a) for a in acoes_possiveis])

        # 3. FÓRMULA Q-LEARNING
        # Q_novo = Q_velho + alpha * (Recompensa + gamma * max_futuro - Q_velho)
        novo_valor = q_antigo + self.alpha * (recompensa + self.gamma * max_q_novo - q_antigo)

        # 4. Atualizar a tabela
        self.q_table[(estado_anterior, acao_anterior)] = novo_valor

    # Métodos para controlar o treino no main.py
    def set_mode(self, treino: bool):
        self.learning_mode = treino
        if not treino:
            self.epsilon = 0.0  # No teste, nunca explora