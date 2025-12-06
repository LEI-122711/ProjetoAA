import matplotlib.pyplot as plt
import math
from Ambiente.AmbienteFarol import AmbienteFarol
from Agentes.AgenteFarolQLearning1 import AgenteFarolQLearning
from Sensores.SensorDirecaoAlvo import SensorDirecaoAlvo
from Sensores.SensorLocalFarol import SensorLocalFarol
from Sensores.SensorProximidadeObstáculo import SensorProximidadeObstáculo
from Simulador import Simulador
from Visualizador import Visualizador
import random
import numpy as np


def treinar():
    print("--- INÍCIO DO TREINO Q-LEARNING ---")

    # 1. Configuração Inicial
    agente = AgenteFarolQLearning(
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=1,
    )

    # IMPORTANTE: Instalar os DOIS sensores
    # O agente precisa de saber a Direção E os Obstáculos
    sensor_gps = SensorDirecaoAlvo()
    sensor_obs = SensorProximidadeObstáculo(raio=1)  # Raio 1 vê 3x3

    agente.instala(sensor_gps)
    agente.instala(sensor_obs)

    historico_passos = []
    EPISODIOS = 20000  # Quantas vezes ele vai tentar
    target_epsilon = 0.01
    start_epsilon = 1.0
    #decay_steps = EPISODIOS * 0.95

    #DECAY_RATE = math.pow(target_epsilon / start_epsilon, 1 / decay_steps)

    # 2. Ciclo de Episódios
    for ep in range(EPISODIOS):
        passos = []
        amb = AmbienteFarol()
        amb.add_obstaculo(8, 7)  # Parede simples
        amb.add_obstaculo(7, 7)

        amb.add_agente(agente, x=0, y=0)

        # Decay do Epsilon
        agente.epsilon = start_epsilon - ep * (start_epsilon - target_epsilon) / (EPISODIOS - 1)

        # --- LÓGICA DE "ESPREITAR" ---
        espreitar = (ep == 0) or ((ep + 1) % 5000 == 0) or (ep == EPISODIOS - 1)

        sim = Simulador(amb, [agente])

        if espreitar:
            print(f"👀 A Visualizar Episódio {ep + 1} (Epsilon: {agente.epsilon:.2f})...")
            # Agora já não vai dar erro aqui
            sim.visualizador = Visualizador(amb)
        else:
            sim.visualizador = None

        sim.executar_simulacao()
        historico_passos.append(sim.passo)

        if (ep + 1) % 50 == 0:
            print(f"Episódio {ep + 1}/{EPISODIOS} completado em {sim.passo} passos.")

    print("--- TREINO CONCLUÍDO ---")

    agente.record_data()

    # 3. Mostrar Gráfico (Para o Relatório)
    passos_np = np.array(historico_passos)

    # Calcular Média Móvel (Janela de 100 episódios)
    # Isto suaviza o gráfico e mostra a tendência real
    media_movel = np.convolve(passos_np, np.ones(100) / 100, mode='valid')

    plt.figure(figsize=(10, 5))

    # Plota os dados brutos em cinzento claro (fundo)
    plt.plot(historico_passos, alpha=0.3, color='gray', label='Bruto')

    # Plota a média móvel em azul forte (tendência)
    plt.plot(media_movel, color='blue', label='Média Móvel (100 eps)')

    plt.xlabel('Episódio')
    plt.ylabel('Passos')
    plt.title('Curva de Aprendizagem (Suavizada)')
    plt.legend()
    plt.show()

    # 4. Teste Final (COM VISUALIZADOR)
    print("A executar teste visual com o cérebro treinado...")
    agente.learning_mode = False  # Parar de aprender/explorar

    amb_final = AmbienteFarol()
    amb_final.add_obstaculo(8, 7)
    amb_final.add_obstaculo(7, 7)
    amb_final.add_obstaculo(6, 7)

    amb_final.add_agente(agente, x=0, y=0)

    # Aqui o visualizador vai abrir
    sim_final = Simulador(amb_final, [agente])
    sim_final.executar_simulacao()


if __name__ == "__main__":
    treinar()