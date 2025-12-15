import matplotlib.pyplot as plt
import math
import numpy as np
from Ambiente.AmbienteLabirinto import AmbienteLabirinto
from Agentes.AgenteLabirintoQLearning import AgenteLabirintoQLearning
from Sensores.SensorDirecaoAlvo import SensorDirecaoAlvo
from Sensores.SensorProximidadeObstáculo import SensorProximidadeObstáculo
from Simulador import Simulador
from Visualizador import Visualizador


# --- DEFINIÇÃO DOS MAPAS (3 DIFICULDADES) ---

def get_mapa(dificuldade):
    if dificuldade == 1: #7x7
        mapa = [
            [0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ]
        return mapa, (0, 0), (6, 4)

    elif dificuldade == 2: #10x10 , substituir pelo 3
        mapa = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
            [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        ]
        return mapa, (0, 0), (9, 10)

    elif dificuldade == 3: #substituir pelo 2
        mapa = [
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        return mapa, (0, 0), (10, 10)

    return None


def treinar_nivel(dificuldade, episodios):
    print(f"dificuldade {dificuldade}")

    matriz, inicio, fim = get_mapa(dificuldade)

    agente = AgenteLabirintoQLearning(
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=1.0
    )
    agente.dificuldade_labirinto = dificuldade
    agente.file = f"labirintoQLearning{dificuldade}.json"

    sensor_gps = SensorDirecaoAlvo()
    sensor_obs = SensorProximidadeObstáculo(raio=1)

    agente.instala(sensor_gps)
    agente.instala(sensor_obs)

    historico_passos = []

    # LINEAR, NÃO SEI MAIS O QUE ALTERAR, FICA ASSIM POR ENQUANTO
    start_epsilon = 1.0
    target_epsilon = 0.01

    for ep in range(episodios):
        amb = AmbienteLabirinto(matriz, inicio, fim)
        amb.add_agente(agente)

        agente.epsilon = start_epsilon - ep * (start_epsilon - target_epsilon) / (episodios - 1)
        agente.epsilon = max(target_epsilon, agente.epsilon)

        espreitar = (ep == 0) or (ep == episodios - 1) #or ((ep + 1) % (episodios/3) == 0) adicionar isto se quiser ver partes do treino

        sim = Simulador(amb, [agente])

        if espreitar:
            sim.visualizador = Visualizador(amb)
        else:
            sim.visualizador = None

        sim.executar_simulacao()
        historico_passos.append(sim.passo)

        #if (ep + 1) % 500 == 0:
        #    print(f"Dif {dificuldade} | Ep {ep + 1}/{episodios} | Passos: {sim.passo}")

    agente.record_data()

    return historico_passos


def executar_treino_completo():
    eps_facil = 5000
    eps_medio = 20000
    eps_dificil = 20000

    #hist1 = treinar_nivel(1, eps_facil)
    #hist2 = treinar_nivel(2, eps_medio)
    hist3 = treinar_nivel(3, eps_dificil)

    print("treino feito")

    #gráficos
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 12))

    def plot_suave(ax, dados, titulo):
        dados_np = np.array(dados)
        media = np.convolve(dados_np, np.ones(50) / 50, mode='valid')
        ax.plot(dados, color='gray', alpha=0.3)
        ax.plot(media, color='blue')
        ax.set_title(titulo)
        ax.set_ylabel("Passos")

    #cada gráfico para cada treino

    #plot_suave(ax1, hist1, "Nível 1 (Fácil)")
    #plot_suave(ax2, hist2, "Nível 2 (Médio)")
    plot_suave(ax3, hist3, "Nível 3 (Difícil)")

    plt.tight_layout()
    plt.show()

    print("teste final visual, apenas para ver o teste")

    mapa3, ini3, fim3 = get_mapa(2)
    amb_final = AmbienteLabirinto(mapa3, ini3, fim3)

    agente = AgenteLabirintoQLearning()
    agente.instala(SensorDirecaoAlvo())
    agente.instala(SensorProximidadeObstáculo(raio=1))

    agente.dificuldade_labirinto = 2
    agente.file = "labirintoQLearning2.json"
    agente.load_data()

    amb_final.add_agente(agente)

    sim = Simulador(amb_final, [agente])
    sim.visualizador = Visualizador(amb_final)
    sim.executar_simulacao()


if __name__ == "__main__":
    executar_treino_completo()