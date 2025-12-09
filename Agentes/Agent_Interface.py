from abc import ABC, abstractmethod


class Agente_Interface(ABC):

    def __init__(self):
        self.sensores = []

        self.N = (-1, 0)
        self.NE = (-1, 1)
        self.E = (0, 1)
        self.SE = (1, 1)
        self.S = (1, 0)
        self.SW = (1, -1)
        self.W = (0, -1)
        self.NW = (-1, -1)

        self.bussola = [
            self.N, self.NE, self.E, self.SE,
            self.S, self.SW, self.W, self.NW
        ]
        pass

        self.cx = None
        self.cy = None

        self.ambiente = None

    # ficheiro é uma string com o nome do ficheiro a ler com os parametros
    @abstractmethod
    def cria(self, ficheiro: str):
        pass

    @abstractmethod
    def observacao(self, observacao):
        # recebe observação
        pass

    @abstractmethod
    def age(self) -> 'Acao':  # retornar algo do tipo Ação
        pass

    # a recompensa é um double
    @abstractmethod
    def avaliacao_estado_atual(self, recompensa: float):
        pass

    def instala(self, sensor: 'Sensor'):  # 'Sensor_Interface'
        self.sensores.append(sensor)

    # (mensagem string e Agente de_agente)
    # @abstractmethod
    # def comunica(self, msg: str, de_agente: 'Agente_Interface'):
    # pass
