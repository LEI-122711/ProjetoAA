from abc import ABC ,abstractmethod


class Ambient_Interface(ABC):

    @abstractmethod
    def observacaoPara(self, agente):
        pass

    @abstractmethod
    def atualizacao(self):
        pass

    @abstractmethod
    def agir(self, acao, agente):
        pass