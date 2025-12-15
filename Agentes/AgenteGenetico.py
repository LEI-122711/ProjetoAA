import random
import numpy as np
import json
import math
from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao


class AgenteGenetico(Agente_Interface):
    def __init__(self, population_size=50, mutation_rate=0.15):
        super().__init__()

        self.observacaofinal = None
        self.learning_mode = True

        self.pop_size = population_size
        self.mutation_rate = mutation_rate
        self.geracao = 1
        self.individuo_atual = 0

        # --- MEMÓRIA DE EXPLORAÇÃO ---
        self.celulas_visitadas = set()

        # Inputs: 2 (GPS) + 9 (Visão) + 2 (Memória Ação) = 13
        self.input_size = 13
        self.hidden_size = 20
        self.output_size = 8

        self.genome_size = (self.input_size * self.hidden_size) + self.hidden_size + \
                           (self.hidden_size * self.output_size) + self.output_size

        self.populacao = [np.random.uniform(-1, 1, self.genome_size) for _ in range(self.pop_size)]
        self.fitnesses = []

        self.melhor_cromossoma = self.populacao[0]
        self.file = "genetico_best.json"

        self.ultima_acao_vetor = (0, 0)

        self.acoes_possiveis = [
            (0, -1), (0, 1), (1, 0), (-1, 0),
            (1, -1), (-1, -1), (1, 1), (-1, 1)
        ]

    def observacao(self, observacao):
        self.observacaofinal = observacao

        # Registo de visitas
        if observacao and "agente" in observacao.dados:
            pos = observacao.dados["agente"]
            self.celulas_visitadas.add(tuple(pos))

    def decodificar_pesos(self, genoma):
        start = 0
        end = self.input_size * self.hidden_size
        w1 = genoma[start:end].reshape((self.input_size, self.hidden_size))

        start = end
        end = start + self.hidden_size
        b1 = genoma[start:end]

        start = end
        end = start + (self.hidden_size * self.output_size)
        w2 = genoma[start:end].reshape((self.hidden_size, self.output_size))

        start = end
        b2 = genoma[start:]
        return w1, b1, w2, b2

    def age(self):
        if self.observacaofinal is None:
            return Acao("andar", dx=0, dy=0)

        dados = self.observacaofinal.dados
        dx_gps, dy_gps = dados.get("direcao", (0, 0))
        visao = dados.get("visao")

        # Inputs
        inputs = [np.clip(dx_gps, -1, 1), np.clip(dy_gps, -1, 1)]

        if visao:
            for linha in visao:
                for celula in linha:
                    inputs.append(celula)
        else:
            inputs.extend([0] * 9)

        inputs.append(self.ultima_acao_vetor[0])
        inputs.append(self.ultima_acao_vetor[1])

        inputs_np = np.array(inputs)

        # Seleção Genoma
        if self.learning_mode:
            genoma = self.populacao[self.individuo_atual]
        else:
            genoma = self.melhor_cromossoma

        # Feedforward
        w1, b1, w2, b2 = self.decodificar_pesos(genoma)
        z1 = np.dot(inputs_np, w1) + b1
        a1 = np.tanh(z1)
        z2 = np.dot(a1, w2) + b2

        # Heurística de Segurança (Evitar Paredes)
        indices_ordenados = np.argsort(z2)[::-1]
        melhor_acao_idx = indices_ordenados[0]

        if visao:
            for idx in indices_ordenados:
                dx, dy = self.acoes_possiveis[idx]
                try:
                    if visao[1 + dx][1 + dy] == 0:
                        melhor_acao_idx = idx
                        break
                except:
                    pass

        dx, dy = self.acoes_possiveis[melhor_acao_idx]
        self.ultima_acao_vetor = (dx, dy)

        return Acao("andar", dx=dx, dy=dy)

    def avaliacao_estado_atual(self, recompensa):
        pass

    def fim_episodio(self, pontuacao_total):
        # Reset memória de movimento
        self.ultima_acao_vetor = (0, 0)

        if not self.learning_mode:
            self.celulas_visitadas.clear()
            return

        dados = self.observacaofinal.dados
        dx, dy = dados.get("direcao", (100, 100))
        distancia = abs(dx) + abs(dy)
        chegou = (distancia == 0)

        # --- LÓGICA DE FITNESS CORRIGIDA (Adeus Caminhos Longos) ---

        if chegou:
            # MODO VENCEDOR: Só interessa a Eficiência.
            # Base 10000 garante que ganham sempre aos perdedores.
            # Multiplicamos a pontuação por 10 para que cada passo poupado valha muito.
            # Como pontuacao_total = 100 - (0.1 * passos),
            # Menos passos = Maior Fitness.
            fitness = 10000.0 + (pontuacao_total * 10.0)
        else:
            # MODO PROCURA: Precisa de incentivos.
            # Reduzi o bónus de exploração de 5.0 para 1.0.
            # Assim, explorar é bom, mas não compensa dar voltas enormes.
            bonus_exploracao = len(self.celulas_visitadas) * 1.0
            bonus_proximidade = 500.0 / (distancia + 1.0)

            # Adicionamos pontuacao_total (que é negativa) para penalizar inércia
            fitness = bonus_exploracao + bonus_proximidade + pontuacao_total

            # Clamp a 0 para não estragar a média
            fitness = max(fitness, 0.0)

        self.fitnesses.append(fitness)
        self.celulas_visitadas.clear()
        self.individuo_atual += 1

        if self.individuo_atual >= self.pop_size:
            self.nova_geracao()

    def nova_geracao(self):
        melhor_idx = np.argmax(self.fitnesses)
        self.melhor_cromossoma = self.populacao[melhor_idx].copy()

        print(
            f"Gen {self.geracao} | Max Fit: {self.fitnesses[melhor_idx]:.1f} | Avg Fit: {np.mean(self.fitnesses):.1f}")

        nova_pop = [self.melhor_cromossoma]  # Elitismo

        # Elitismo Top 5 (Para estabilizar)
        indices_top = np.argsort(self.fitnesses)[-5:]
        for i in indices_top:
            if len(nova_pop) < 5:
                nova_pop.append(self.populacao[i].copy())

        while len(nova_pop) < self.pop_size:
            pai1 = self.torneio()
            pai2 = self.torneio()

            mask = np.random.rand(self.genome_size) > 0.5
            filho = np.where(mask, pai1, pai2)

            if random.random() < self.mutation_rate:
                indices_mut = np.random.choice(self.genome_size, int(self.genome_size * 0.15), replace=False)
                filho[indices_mut] += np.random.normal(0, 0.5, size=len(indices_mut))

            nova_pop.append(filho)

        self.populacao = nova_pop
        self.fitnesses = []
        self.individuo_atual = 0
        self.geracao += 1

    def torneio(self):
        indices = random.sample(range(self.pop_size), 5)
        scores = [self.fitnesses[i] for i in indices]
        return self.populacao[indices[np.argmax(scores)]]

    def record_data(self, ficheiro=None):
        if ficheiro is None: ficheiro = self.file
        dados = self.melhor_cromossoma.tolist()
        with open(ficheiro, "w") as f: json.dump(dados, f)
        print(f"Melhor genoma guardado em {ficheiro}")

    def load_data(self, ficheiro=None):
        if ficheiro is None: ficheiro = self.file
        try:
            with open(ficheiro, "r") as f:
                dados = json.load(f)
            self.melhor_cromossoma = np.array(dados)
            self.learning_mode = False
            print("Cérebro Genético carregado!")
        except:
            print("Sem cérebro guardado.")

    def cria(self, ficheiro):
        pass

    def instala(self, sensor):
        super().instala(sensor)