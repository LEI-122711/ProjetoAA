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
    """
    Retorna (mapa, inicio, fim) baseado na dificuldade.
    0 = Livre, 1 = Parede
    """
    if dificuldade == 1:
        # FÁCIL: Corredor com poucos obstáculos
        # Mapa 7x7
        mapa = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]
        return mapa, (0, 0), (6, 6)

    elif dificuldade == 2:
        # MÉDIO: Mais obstáculos e becos
        # Mapa 10x10
        mapa = [
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # Caminho meio aberto
            [1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        return mapa, (0, 0), (9, 9)

    elif dificuldade == 3:
        # DIFÍCIL: Labirinto clássico (Ziguezague obrigatório)
        # Mapa 10x10 denso
        mapa = [
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],  # Parede grande
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        return mapa, (0, 0), (9, 9)

    return None


def treinar_nivel(dificuldade, episodios):
    print(f"\n=== A INICIAR TREINO: DIFICULDADE {dificuldade} ===")

    # 1. Obter mapa
    matriz, inicio, fim = get_mapa(dificuldade)

    # 2. Configurar Agente (Cria ficheiro novo para cada dificuldade)
    agente = AgenteLabirintoQLearning(
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=1.0  # Começa sempre a explorar no novo mapa
    )
    # Define manualmente a dificuldade para ele gravar no ficheiro certo
    agente.dificuldade_labirinto = dificuldade
    agente.file = f"labirintoQLearning{dificuldade}.json"

    sensor_gps = SensorDirecaoAlvo()
    sensor_obs = SensorProximidadeObstáculo(raio=1)

    agente.instala(sensor_gps)
    agente.instala(sensor_obs)

    historico_passos = []

    # Decaimento Linear do Epsilon
    start_epsilon = 1.0
    target_epsilon = 0.01

    for ep in range(episodios):
        # Cria ambiente novo (limpo) a cada episódio
        amb = AmbienteLabirinto(matriz, inicio, fim)
        amb.add_agente(agente)  # Usa inicio padrão definido no ambiente

        # Decay do Epsilon
        agente.epsilon = start_epsilon - ep * (start_epsilon - target_epsilon) / (episodios - 1)
        agente.epsilon = max(target_epsilon, agente.epsilon)

        # Visualizar apenas o primeiro e o último
        espreitar = (ep == 0) or (ep == episodios - 1) or ((ep + 1) % (episodios/3) == 0)

        sim = Simulador(amb, [agente])

        if espreitar:
            # print(f"👀 Dificuldade {dificuldade} | Ep {ep+1} | Eps: {agente.epsilon:.2f}")
            sim.visualizador = Visualizador(amb)
        else:
            sim.visualizador = None

        sim.executar_simulacao()
        historico_passos.append(sim.passo)

        if (ep + 1) % 500 == 0:
            print(f"Dif {dificuldade} | Ep {ep + 1}/{episodios} | Passos: {sim.passo}")

    # Guardar o cérebro deste nível
    agente.record_data()

    return historico_passos


def executar_treino_completo():
    # Podes ajustar o número de episódios por dificuldade
    # O Difícil precisa de mais tempo!
    eps_facil = 3000
    eps_medio = 5000
    eps_dificil = 10000

    hist1 = treinar_nivel(1, eps_facil)
    hist2 = treinar_nivel(2, eps_medio)
    hist3 = treinar_nivel(3, eps_dificil)

    print("\n--- TREINOS CONCLUÍDOS ---")

    # Mostrar Gráficos (Um por dificuldade)
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 12))

    def plot_suave(ax, dados, titulo):
        dados_np = np.array(dados)
        media = np.convolve(dados_np, np.ones(50) / 50, mode='valid')
        ax.plot(dados, color='gray', alpha=0.3)
        ax.plot(media, color='blue')
        ax.set_title(titulo)
        ax.set_ylabel("Passos")

    plot_suave(ax1, hist1, "Nível 1 (Fácil)")
    plot_suave(ax2, hist2, "Nível 2 (Médio)")
    plot_suave(ax3, hist3, "Nível 3 (Difícil)")

    plt.tight_layout()
    plt.show()

    # --- TESTE FINAL (MODO PERITO - NÍVEL 3) ---
    print("\n--- TESTE FINAL VISUAL (DIFICULDADE 3) ---")

    # 1. Setup Ambiente Difícil
    mapa3, ini3, fim3 = get_mapa(3)
    amb_final = AmbienteLabirinto(mapa3, ini3, fim3)

    # 2. Setup Agente Perito
    agente = AgenteLabirintoQLearning()
    agente.instala(SensorDirecaoAlvo())
    agente.instala(SensorProximidadeObstáculo(raio=1))

    # Carregar o cérebro difícil
    agente.dificuldade_labirinto = 3
    agente.file = "labirintoQLearning3.json"
    agente.load_data()  # Isto já mete epsilon=0

    amb_final.add_agente(agente)

    sim = Simulador(amb_final, [agente])
    sim.visualizador = Visualizador(amb_final)
    sim.executar_simulacao()


if __name__ == "__main__":
    executar_treino_completo()