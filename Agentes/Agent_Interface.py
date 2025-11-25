from abc import ABC, abstractmethod


class Agente_Interface(ABC):

    def __init__(self):
        self.sensores = []

    # ficheiro é uma string com o nome do ficheiro a ler com os parametros
    @abstractmethod
    def cria(self,ficheiro:str):
        pass

    @abstractmethod
    def observacao(self,observacao):
        #recebe observação
        pass

    @abstractmethod
    def age(self)-> 'Acao':  #retornar algo do tipo Ação
        pass

    # a recompensa é um double
    @abstractmethod
    def avaliacao_estado_atual(self,recompensa: float):
        pass


    def instala(self,sensor: 'Sensor'):
        self.sensores.append(sensor)
    
    

    #(mensagem string e Agente de_agente)
    #@abstractmethod
    #def comunica(self,msg: str,de_agente: 'Agente_Interface'):
        #pass
