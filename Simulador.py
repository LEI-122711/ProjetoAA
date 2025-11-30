import time

from Visualizador import Visualizador

class Simulador:
    def __init__(self, ambiente, agentes):
        self.ambiente = ambiente
        self.agentes = agentes
        self.passo = 0
        self.visualizador = None
        self.resultado = []

    def executar_simulacao(self):
        print("--- Início da Simulação ---")

        simulacao_ativa = True

        # --- CORREÇÃO 1: REMOVI A CRIAÇÃO FORÇADA ---
        # Apaguei as linhas: if self.visualizador is None...

        # Proteção para o loop não ser infinito se os agentes se perderem
        while simulacao_ativa and self.passo < 1000:
            self.passo += 1

            # Atualiza ambiente
            self.ambiente.atualizacao()

            # --- CORREÇÃO 2: SÓ DESENHA SE EXISTIR VISUALIZADOR ---
            if self.visualizador is not None:
                self.visualizador.desenhar()
                time.sleep(0.3) # Podes descomentar se quiseres ver devagar

            todos_terminaram = True

            for agente in self.agentes:
                obs = self.ambiente.observacaoPara(agente)
                agente.observacao(obs)
                acao = agente.age()

                recompensa, terminou = self.ambiente.agir(acao, agente)

                agente.avaliacao_estado_atual(recompensa)

                if not terminou:
                    todos_terminaram = False

            # --- CORREÇÃO 3: VERIFICAÇÃO FINAL ---
            if self.visualizador is not None:
                self.visualizador.desenhar()

            if todos_terminaram:
                self.resultado.append(self.passo)
                # print("Todos os agentes completaram o objetivo!") # Opcional: comentar para não encher a consola
                simulacao_ativa = False