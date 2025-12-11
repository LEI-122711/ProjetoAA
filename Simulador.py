import time

from Visualizador import Visualizador

class Simulador:
    def __init__(self, ambiente, agentes):
        self.ambiente = ambiente
        self.agentes = agentes
        self.passo = 0
        self.recompensa = 0
        self.visualizador = None
        self.resultado = []

    def executar_simulacao(self):
        print("a simular i guess")

        simulacao_ativa = True


        while simulacao_ativa and self.passo < 200:
            self.passo += 1

            self.ambiente.atualizacao()

            if self.visualizador is not None:
                self.visualizador.desenhar()
                #time.sleep(0.2) #alterar tempo para ver as coisas

            todos_terminaram = True

            for agente in self.agentes:
                obs = self.ambiente.observacaoPara(agente)
                agente.observacao(obs)
                acao = agente.age()

                recompensa, terminou = self.ambiente.agir(acao, agente)

                self.recompensa += recompensa

                #agente.avaliacao_estado_atual(recompensa)
                obs_nova = self.ambiente.observacaoPara(agente)
                agente.observacao(obs_nova)

                if not terminou:
                    todos_terminaram = False

                agente.avaliacao_estado_atual(recompensa)

            if self.visualizador is not None:
                self.visualizador.desenhar()

            if todos_terminaram:
                self.resultado.append(self.passo)
                simulacao_ativa = False