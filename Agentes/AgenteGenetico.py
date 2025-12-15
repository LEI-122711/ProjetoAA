import random
import numpy as np
import json
from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao


class AgenteGenetico(Agente_Interface):
    def __init__(self, population_size=50, mutation_rate=0.1):
        super().__init__()

        self.observacaofinal = None
        self.learning_mode = True  # Se True, evolui. Se False, usa o melhor.

        # --- CONFIGURAÇÃO GENÉTICA ---
        self.pop_size = population_size
        self.mutation_rate = mutation_rate
        self.geracao = 1
        self.individuo_atual = 0

        # Estrutura do Cérebro (Rede Simples)
        # Inputs: 2 (GPS) + 9 (Visão 3x3) = 11
        # Outputs: 8 (Direções possíveis)
        self.input_size = 11
        self.output_size = 8

        # A população é uma lista de matrizes de pesos (Cromossomas)
        # Cada indivíduo é uma matriz 11x8
        self.populacao = [np.random.uniform(-1, 1, (self.input_size, self.output_size)) for _ in range(self.pop_size)]
        self.fitnesses = []  # Guarda a pontuação de cada um

        # O Melhor de todos (para guardar/carregar)
        self.melhor_cromossoma = self.populacao[0]

        # 8 Direções
        self.acoes_possiveis = [
            (0, -1), (0, 1), (1, 0), (-1, 0),  # N, S, E, O
            (1, -1), (-1, -1), (1, 1), (-1, 1)  # NE, NO, SE, SO
        ]

    def observacao(self, observacao):
        self.observacaofinal = observacao

    def age(self):
        # 1. Preparar Inputs (Achatar os sensores num array)
        if self.observacaofinal is None:
            return Acao("andar", dx=0, dy=0)

        dados = self.observacaofinal.dados
        dx_gps, dy_gps = dados.get("direcao", (0, 0))
        visao = dados.get("visao")

        # Vetor de entrada (Input Layer)
        inputs = [dx_gps, dy_gps]

        if visao:
            # Achata a matriz 3x3 para uma lista de 9 números
            for linha in visao:
                for celula in linha:
                    inputs.append(celula)
        else:
            # Se não houver visão, enche com zeros
            inputs.extend([0] * 9)

        inputs_np = np.array(inputs)  # Shape (11,)

        # 2. Escolher o cérebro a usar
        if self.learning_mode:
            cromossoma = self.populacao[self.individuo_atual]
        else:
            cromossoma = self.melhor_cromossoma

        # 3. Calcular Saída (Feedforward)
        # Produto escalar: (1, 11) dot (11, 8) = (1, 8)
        outputs = np.dot(inputs_np, cromossoma)

        # 4. Escolher a ação com maior ativação
        acao_idx = np.argmax(outputs)

        dx, dy = self.acoes_possiveis[acao_idx]
        return Acao("andar", dx=dx, dy=dy)

    def avaliacao_estado_atual(self, recompensa):
        # O Agente Genético NÃO aprende passo a passo.
        # Ele só aprende no fim do episódio.
        pass

    # --- MÉTODO NOVO: OBRIGATÓRIO CHAMAR NO FINAL DO EPISÓDIO ---
    def fim_episodio(self, pontuacao_total):
        if not self.learning_mode:
            return

        # 1. Registar performance do indivíduo atual
        self.fitnesses.append(pontuacao_total)
        self.individuo_atual += 1

        # 2. Se já testámos todos, criar nova geração
        if self.individuo_atual >= self.pop_size:
            self.nova_geracao()

    def nova_geracao(self):
        # Encontrar o melhor desta geração
        melhor_idx = np.argmax(self.fitnesses)
        self.melhor_cromossoma = self.populacao[melhor_idx].copy()

        print(f"Geração {self.geracao} terminada. Melhor Fitness: {self.fitnesses[melhor_idx]:.2f}")

        nova_pop = []

        # ELITISMO: O melhor passa sempre sem alterações
        nova_pop.append(self.melhor_cromossoma)

        # SELEÇÃO E CRUZAMENTO
        while len(nova_pop) < self.pop_size:
            # Torneio: Escolher 2 pais aleatórios e ficar com o melhor
            pai1 = self.torneio()
            pai2 = self.torneio()

            # Crossover (Ponto único ou média)
            filho = (pai1 + pai2) / 2.0

            # Mutações (Adicionar ruído aleatório)
            if random.random() < self.mutation_rate:
                ruido = np.random.normal(0, 0.5, size=filho.shape)
                filho += ruido

            nova_pop.append(filho)

        self.populacao = nova_pop
        self.fitnesses = []
        self.individuo_atual = 0
        self.geracao += 1

    def torneio(self):
        # Escolhe 3 aleatórios e retorna o melhor (para ser pai)
        indices = random.sample(range(self.pop_size), 3)
        scores = [self.fitnesses[i] for i in indices]
        vencedor = indices[np.argmax(scores)]
        return self.populacao[vencedor]

    # --- PERSISTÊNCIA ---
    def record_data(self, ficheiro="genetico_best.json"):
        # Guardar apenas o melhor cromossoma
        dados = self.melhor_cromossoma.tolist()  # Converter numpy para lista
        with open(ficheiro, "w") as f:
            json.dump(dados, f)
        print(f"Melhor genoma guardado em {ficheiro}")

    def load_data(self, ficheiro="genetico_best.json"):
        try:
            with open(ficheiro, "r") as f:
                dados = json.load(f)
            self.melhor_cromossoma = np.array(dados)
            self.learning_mode = False  # Assume modo teste
            print("Cérebro Genético carregado!")
        except:
            print("Erro ao carregar ficheiro genético.")

    def cria(self, ficheiro):
        pass

    def instala(self, sensor):
        super().instala(sensor)