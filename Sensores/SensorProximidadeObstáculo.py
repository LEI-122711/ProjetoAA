from Sensores.Sensor_Interface import Sensor_Interface
from Observacao import Observacao

class SensorLocalFarol(Sensor_Interface):
    def __init__(self,raio=2):
        self.raio = raio

    def filtrar(self, observacao):
        ax, ay = observacao.dados["agente"]
        mapa = observacao.dados["mapa"]
        height = len(mapa)
        width = len(mapa[0])


        visao = []

        # Percorre as células à volta do agente (ex: de x-1 a x+1)
        for i in range(ax - self.raio, ax + self.raio + 1):
            linha = []
            for j in range(ay - self.raio, ay + self.raio + 1):
                # Se estiver fora do mapa, considera parede (1)
                if i < 0 or i >= height or j < 0 or j >= width:
                    linha.append(1)
                else:
                    linha.append(mapa[i][j])  # Copia o valor real (0 ou 1)
            visao.append(linha)

        # O agente recebe APENAS esta matriz 3x3
        return Observacao({
            "visao": visao,
            # Exemplo de saida: [[0, 0, 1], [0, 0, 0], [1, 1, 1]]
            # Significa: Parede à direita e paredes em baixo.
            "posicao_agente": (ax, ay)  # Opcional
        })

