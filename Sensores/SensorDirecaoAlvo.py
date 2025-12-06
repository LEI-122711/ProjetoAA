from Sensores.Sensor_Interface import Sensor_Interface
from Observacao import Observacao

class SensorDirecaoAlvo(Sensor_Interface):
    def __init__(self):
        super().__init__()

    def filtrar(self, observacao):

        novos_dados = observacao.dados.copy()

        ax, ay = novos_dados["agente"]

        if "farol" in novos_dados:
            fx, fy = novos_dados["farol"]
        elif "saida" in novos_dados:
            fx, fy = novos_dados["saida"]
        else:
            raise KeyError("Observação não contem nem 'farol' nem 'saida'.")

        dx = 1 if fx > ax else -1 if fx < ax else 0
        dy = 1 if fy > ay else -1 if fy < ay else 0

        novos_dados["direcao"]=(dx, dy)

        return Observacao(novos_dados)