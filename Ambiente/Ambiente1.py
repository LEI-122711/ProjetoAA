from Ambiente.Ambient_Interface import Ambient_Interface
from Observacao import Observacao

class Ambiente1(Ambient_Interface):

    def __init__(self, linhas=10, colunas=10):
        print("Ambiente 1 criado!")

        self.linhas = linhas
        self.colunas = colunas

        # Grelha vazia para exemplo
        self.matriz = [[0 for _ in range(colunas)] for _ in range(linhas)]
        self.agentes_pos = {}

    def cria(self, ficheiro: str):
        print(f"A carregar parâmetros do ambiente...")

    def addAgente_centro(self, agente):
        cx = self.linhas // 2
        cy = self. colunas // 2

        self.agentes_pos[agente] = (cx, cy)

        agente.cx = cx
        agente.cy = cy
        agente.ambiente = self

        print(f"Agente colocado no centro: ({cx}, {cy})")

    def observacaoPara(self, agente):
        pos = self.agentes_pos.get(agente, None)
        return Observacao({
            "posicao": pos,
            "info": "ok"
        })

    def agir(self, acao, agente):
        print("Ação recebida:", acao.tipo, acao.params)

        if acao.tipo == "mover":
            dx, dy = acao.params.get("dx"), acao.params.get("dy")
            x, y = self.agentes_pos[agente]
            nx, ny = x + dx, y + dy

            # Verificar limites
            if 0 <= nx < self.linhas and 0 <= ny < self.colunas:
                self.agentes_pos[agente] = (nx, ny)
                print(f"Agente moveu-se para {nx, ny}")
            else:
                print("Movimento inválido!")

    def atualizacao(self):
        print("Atualização do ambiente concluída.")
