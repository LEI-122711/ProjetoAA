from Ambiente.AmbienteFarol import AmbienteFarol
from Agentes.AgenteFarol1 import AgenteFarol1
from Sensores.SensorDirecaoAlvo import SensorDirecaoAlvo
from Sensores.SensorLocalFarol import SensorLocalFarol
from Sensores.SensorProximidadeObstáculo import SensorProximidadeObstáculo
from Simulador import Simulador
from Visualizador import Visualizador
from Agentes.AgenteFarolQLearning1 import AgenteQLearning


def testar_ambiente():
    print("--- INÍCIO DO TESTE ---")

    # 1. Setup
    amb = AmbienteFarol()
    #agente = AgenteFarol1()
    agente = AgenteQLearning()
    sensor = SensorDirecaoAlvo()
    sensor2 = SensorProximidadeObstáculo()
    agente.load_data()

    amb.add_obstaculo(8, 7)
    amb.add_obstaculo(7, 7)

    # 2. Instalação
    agente.instala(sensor)
    agente.instala(sensor2)
    amb.add_agente(agente, x=0, y=0)  # Posição inicial

    # 3. Simulação
    sim = Simulador(amb, [agente])
    sim.visualizador = Visualizador(amb)
    sim.executar_simulacao()



if __name__ == "__main__":
    testar_ambiente()