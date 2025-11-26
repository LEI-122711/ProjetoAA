import time

from Visualizador import Visualizador


class Simulador:
    def __init__(self, ambiente, agentes):
        self.ambiente = ambiente
        self.agentes = agentes  # Lista de agentes
        self.passo = 0
        self.visualizador = None
        self.resultado = []

    def executar_simulacao(self):
        print("--- Início da Simulação ---")

        simulacao_ativa = True

        self.visualizador = Visualizador(self.ambiente)

        while simulacao_ativa :
            self.passo += 1
            print(f"\nPasso {self.passo}")

            #atualizar se for eu quiser fazer o farol desligado
            self.ambiente.atualizacao()

            self.visualizador.desenhar()
            time.sleep(0.3)

            todos_terminaram = True

            for agente in self.agentes:

                obs = self.ambiente.observacaoPara(agente)
                agente.observacao(obs)

                acao = agente.age()

                recompensa, terminou = self.ambiente.agir(acao, agente)

                agente.avaliacao_estado_atual(recompensa)

                print(f"Agente agiu: {acao.params} -> Recompensa: {recompensa}")

                if not terminou:
                    todos_terminaram = False

            self.visualizador.desenhar()
            #time.sleep(0.3)

            # Se todos os agentes chegaram ao objetivo, paramos
            if todos_terminaram:
                self.resultado.append(self.passo)
                print("Todos os agentes completaram o objetivo!")
                simulacao_ativa = False

            # Opcional: Pausa para visualizar
            # time.sleep(0.5)