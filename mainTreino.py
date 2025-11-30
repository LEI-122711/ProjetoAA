import matplotlib.pyplot as plt
import math
from Ambiente.AmbienteFarol import AmbienteFarol
from Agentes.AgenteFarolQLearning1 import AgenteQLearning
from Sensores.SensorLocalFarol import SensorLocalFarol
from Sensores.SensorProximidadeObstáculo import SensorProximidadeObstáculo
from Simulador import Simulador
from Visualizador import Visualizador


def treinar():
    print("--- INÍCIO DO TREINO Q-LEARNING ---")

    # 1. Configuração Inicial
    agente = AgenteQLearning(
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=1,
    )

    # IMPORTANTE: Instalar os DOIS sensores
    # O agente precisa de saber a Direção E os Obstáculos
    sensor_gps = SensorLocalFarol()
    sensor_obs = SensorProximidadeObstáculo(raio=1)  # Raio 1 vê 3x3

    agente.instala(sensor_gps)
    agente.instala(sensor_obs)

    historico_passos = []
    EPISODIOS = 5000  # Quantas vezes ele vai tentar
    target_epsilon = 0.01
    start_epsilon = 1.0
    decay_steps = EPISODIOS * 0.90

    DECAY_RATE = math.pow(target_epsilon / start_epsilon, 1 / decay_steps)

    # 2. Ciclo de Episódios
    for ep in range(EPISODIOS):
        passos = []
        amb = AmbienteFarol()
        amb.add_obstaculo(8, 7)
        amb.add_obstaculo(7, 7)
        amb.add_obstaculo(6, 7)
        amb.add_obstaculo(3, 3)
        amb.add_obstaculo(2, 2)

        amb.add_agente(agente, x=0, y=0)

        # Decay do Epsilon
        agente.epsilon = max(0.01, agente.epsilon * DECAY_RATE)

        # --- LÓGICA DE "ESPREITAR" ---
        espreitar = (ep == 0) or ((ep + 1) % 1000 == 0) or (ep == EPISODIOS - 1)

        sim = Simulador(amb, [agente])

        if espreitar:
            print(f"👀 A Visualizar Episódio {ep + 1} (Epsilon: {agente.epsilon:.2f})...")
            # Agora já não vai dar erro aqui
            sim.visualizador = Visualizador(amb)
        else:
            sim.visualizador = None

        sim.executar_simulacao()
        historico_passos.append(sim.passo)

        if (ep + 1) % 10 == 0:
            print(f"Episódio {ep + 1}/{EPISODIOS} completado em {sim.passo} passos.")

    print("--- TREINO CONCLUÍDO ---")

    # 3. Mostrar Gráfico (Para o Relatório)
    plt.plot(historico_passos)
    plt.xlabel('Episódio')
    plt.ylabel('Passos para chegar')
    plt.title('Curva de Aprendizagem')
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