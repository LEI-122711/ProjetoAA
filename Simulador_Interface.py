from abc import ABC, abstractmethod

class Simulador_Interface(ABC):

    @abstractmethod
    def cria(self, ficheiro: str): #MotorDeSimulacao
        pass

    @abstractmethod
    def listaAgentes(self): #Agente[]
        pass

    @abstractmethod
    def executa(self):
        pass