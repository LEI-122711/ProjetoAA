from Sensores.Sensor_Interface import Sensor_Interface
from Observacao import Observacao

class Sensor_LocalFarol(Sensor_Interface):
    def __init__(self):
        super().__init__()

    def filtrar(self,observação):
        ax, ay = observação.dados["agente"]
        fx, fy = observação.dados["farol"]

        dx = 1 if fx > ax else -1 if fx < ax else 0
        dy = 1 if fy > ay else -1 if fy < ay else 0

        return Observacao({
            "direcao": (dx, dy)
        })

