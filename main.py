from Ambiente.AmbienteFarol import AmbienteFarol
from Agentes.AgenteFarol1 import AgenteFarol1
from Sensores.SensorDirecaoAlvo import SensorDirecaoAlvo
from Sensores.SensorLocalFarol import SensorLocalFarol
from Sensores.SensorProximidadeObstáculo import SensorProximidadeObstáculo
from Simulador import Simulador
from Visualizador import Visualizador
from Agentes.AgenteFarolQLearning1 import AgenteFarolQLearning
from Ambiente.AmbienteLabirinto import AmbienteLabirinto
from Agentes.AgenteLabirinto import AgenteLabirinto
from Agentes.AgenteLabirintoQLearning import AgenteLabirintoQLearning
from mainTreinoFarol import gerar_heatmap_valor, plotar_heatmap


def testar_ambiente():
    print("teste")

    #esta é a dificuldade 1
    mapa = [
        [0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [1, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0]
    ]
    amb = AmbienteFarol()
    #amb= AmbienteLabirinto(mapa,(0,0),(6,4))
    #agente = AgenteFarol1()
    agente = AgenteFarolQLearning()
    #agente = AgenteLabirintoQLearning()
    #agente = AgenteLabirinto()
    sensor = SensorDirecaoAlvo()
    sensor2 = SensorProximidadeObstáculo()
    agente.load_data()
    #agente.load_data("labirintoQLearning1.json")

    amb.add_obstaculo(8, 7)
    #amb.add_obstaculo(9, 7)
    amb.add_obstaculo(7, 7)
    amb.add_obstaculo(3, 3)
    amb.add_obstaculo(2, 3)
    amb.add_obstaculo(1, 3)
    amb.add_obstaculo(4, 3)

    agente.instala(sensor)
    agente.instala(sensor2)
    amb.add_agente(agente, x=0, y=0)  # Posição inicial

    heatmap= gerar_heatmap_valor(amb,agente)
    plotar_heatmap(heatmap,"heatmap no farol")

    sim = Simulador(amb, [agente])
    sim.visualizador = Visualizador(amb)
    sim.executar_simulacao()



if __name__ == "__main__":
    testar_ambiente()