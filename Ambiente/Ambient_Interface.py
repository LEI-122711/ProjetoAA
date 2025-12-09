from abc import ABC ,abstractmethod


class Ambient_Interface(ABC):

    @abstractmethod
    def cria(self, ficheiro: str):
        pass

    @abstractmethod
    def observacaoPara(self, agente):
        pass

    @abstractmethod
    def atualizacao(self):
        pass

    @abstractmethod
    def agir(self, acao, agente):
        pass



    @property
    @abstractmethod
    def largura(self): pass

    @property
    @abstractmethod
    def altura(self): pass



