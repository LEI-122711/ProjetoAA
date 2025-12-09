import random
import numpy as np
from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao
import json


class AgenteLabirintoQLearning(Agente_Interface):

    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, dificuldade = 1):
        super().__init__()
        # Tabela Q simples

        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate

        self.learning_mode = True

        self.dificuldade_labirinto = dificuldade
        self.file = f"labirintoQLearning.{self.dificuldade_labirinto}.json"

        self.q_table = {}
        self.ultimo_estado = None
        self.ultima_acao_idx = None

    def observacao(self, observacao):
        self.observacaofinal = observacao

    def cria(self, ficheiro: str):
        pass

    def get_estado_hash(self):
        # Cria uma assinatura única do que o agente está a ver
        dados = self.observacaofinal.dados

        direcao = dados.get("direcao", (0, 0))
        visao = dados.get("visao", None)


        '''
        Features simples -> nao aprende caminhos espeificos, ou seja, o agente aprende a 
        evitar paredes e a mover-se nas direções que dao mais recompensa, mas nao aprende 
        o labirinto em si; Nao memoriza caminhos e pode falhar em labirintos com becos, porque 
        nao ve ao longe
        
        Tuplos -> bom para um labirinto especifico e pode encontrar um caminho muito bom com o tempo
        mas, se mudar o labirinto ele nao reconhece nada e tem que aprender tudo de novo e a tabela
        Q explode em tamanho
        --> Melhor estratégia se ha uma 1 Q-table por cada mapa.
        
        '''
        if visao is None:
           visao_t = None
        else:
            visao_t = tuple(tuple(l) for l in visao)


        return (direcao,visao_t)

    def get_q_valores(self, estado):
        if estado not in self.q_table:
            self.q_table[estado] = [0.0] * len(self.bussola)
        return self.q_table[estado]

    def age(self):
        estado = self.get_estado_hash()
        q_valores = self.get_q_valores(estado)

        num_acoes = len(self.bussola)

        #Aleatorio
        if self.learning_mode and random.random() < self.epsilon:
            acao_idx = random.randint(0, num_acoes - 1)

        # Avaliar aproveitamento
        else:
            max_val = max(q_valores)

            # Desempate aleatório entre as melhores ações
            best = [i for i, v in enumerate(q_valores) if v == max_val]
            acao_idx = random.choice(best)

        self.ultimo_estado = estado
        self.ultima_acao_idx = acao_idx

        dx, dy = self.bussola[acao_idx]
        return Acao("andar", dx=dx, dy=dy)

    def avaliacao_estado_atual(self, recompensa: float):
        if not self.learning_mode or self.ultimo_estado is None:
            return

        estado_antigo = self.ultimo_estado
        acao_idx = self.ultima_acao_idx
        new_estado = self.get_estado_hash()

        q_antigo = self.get_q_valores(estado_antigo)[acao_idx]
        max_q_novo = max(self.get_q_valores(new_estado))

        #Formula
        new_value = q_antigo + self.alpha * (recompensa + self.gamma * max_q_novo - q_antigo)
        self.q_table[estado_antigo][acao_idx] = new_value

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

            # Configura logo para modo de teste
            self.learning_mode = False
            self.epsilon = 0.0
            print("Cérebro carregado com sucesso! Modo Perito ativado.")
        except FileNotFoundError:
            print("Erro: Ficheiro de cérebro não encontrado.")