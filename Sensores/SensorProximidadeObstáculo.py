from Sensores.Sensor_Interface import Sensor_Interface
from Observacao import Observacao

class SensorProximidadeObstáculo(Sensor_Interface):
    def __init__(self,raio=1):
        self.raio = raio

    def filtrar(self, observacao):

        novos_dados = observacao.dados.copy()

        ax, ay = novos_dados["agente"]
        mapa = novos_dados["mapa"]
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

        novos_dados["visao"] = visao

        # O agente recebe APENAS esta matriz 3x3
        return Observacao(novos_dados)

        # Exemplo de saida: [[0, 0, 1], [0, 0, 0], [1, 1, 1]]
        # Significa: Parede à direita e paredes em baixo.

