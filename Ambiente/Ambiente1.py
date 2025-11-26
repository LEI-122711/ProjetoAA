from Ambiente.Ambient_Interface import Ambient_Interface
from Observacao import Observacao

class Ambiente1(Ambient_Interface):

    def __init__(self):
        print("Ambiente 1 criado!")

    '''
    Ciclo de Simulação:  Devolve a perceção específica do estado local para o agente.
    Implementação: Devolve uma observação simples (apenas confirma a comunicação)
    '''
    def observacaoPara(self, agente):
        return Observacao({"teste": "ok"})

    '''
    Ciclo de Simulação: Executa a ação do agente no ambiente -> Mover, Recolher, Depositar
    Implementação: Imprime os parametros da ação mas nao altera
    '''
    def agir(self, acao, agente):
        print("Ação recebida:", acao.tipo, acao.params)

    '''
    Ciclo de Simulação: Atualiza os elementos dinâmicos do ambiente recursos a crescer, farol a mover-se
    '''
    def atualizacao(self):
        print("Atualização concluída.")
        
    def adeus(self):
        print("Adeus!")