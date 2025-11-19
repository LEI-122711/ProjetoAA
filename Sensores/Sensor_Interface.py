from abc import ABC, abstractmethod

class Sensor_Interface(ABC):

    @abstractmethod
    def filtrar(self,observação):
        dados = observação.dados
        pass

