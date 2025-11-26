from Ambiente.AmbienteFarol import AmbienteFarol
from Agentes.AgenteFarol1 import AgenteFarol1
from Sensores.SensorLocalFarol import SensorLocalFarol
from Simulador import Simulador


def testar_ambiente():
    print("--- INÍCIO DO TESTE ---")

    # 1. Setup
    amb = AmbienteFarol()
    agente = AgenteFarol1()
    sensor = SensorLocalFarol()
    amb.add_obstaculo(8,7)

    # 2. Instalação
    agente.instala(sensor)
    amb.add_agente(agente, x=0, y=0)  # Posição inicial

    # 3. Simulação
    sim = Simulador(amb, [agente])
    sim.executar_simulacao()


if __name__ == "__main__":
    testar_ambiente()