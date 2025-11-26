from abc import ABC, abstractmethod

class Sensor_Interface(ABC):

    @abstractmethod
    def filtrar(self, observacao):
        dados = (observacao.dados)
        pass

