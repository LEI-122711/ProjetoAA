from abc import ABC ,abstractmethod


class Ambient_Interface(ABC):



    @abstractmethod
    def observacaoPara(self,Agente):
        pass

    @abstractmethod
    def atualizacao(self):
        pass

    @abstractmethod
    def agir(self,Acao,Agente):
        pass