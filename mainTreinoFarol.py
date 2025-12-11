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
import seaborn as sns


def treinar():
    print("treino farol")

    agente = AgenteFarolQLearning(
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=1,
    )

    sensor_gps = SensorDirecaoAlvo()
    sensor_obs = SensorProximidadeObstáculo(raio=1)

    agente.instala(sensor_gps)
    agente.instala(sensor_obs)

    historico_passos = []
    historico_recompensa = []
    EPISODIOS = 20000
    target_epsilon = 0.01
    start_epsilon = 1.0
    #decay_steps = EPISODIOS * 0.95

    #DECAY_RATE = math.pow(target_epsilon / start_epsilon, 1 / decay_steps)

    # 2. Ciclo de Episódios
    for ep in range(EPISODIOS):
        passos = []
        amb = AmbienteFarol()
        amb.add_obstaculo(8, 7)
        amb.add_obstaculo(9, 7)
        amb.add_obstaculo(7, 7)
        amb.add_obstaculo(3, 3)
        amb.add_obstaculo(2, 3)
        amb.add_obstaculo(1, 3)
        amb.add_obstaculo(4, 3)

        amb.add_agente(agente, x=0, y=0)

        # Decay do Epsilon
        agente.epsilon = start_epsilon - ep * (start_epsilon - target_epsilon) / (EPISODIOS - 1)

        espreitar = (ep == 0) or (ep == EPISODIOS - 1) #or ((ep + 1) % 5000 == 0) alterar para o que

        sim = Simulador(amb, [agente])

        if espreitar:
            print(f"episódio {ep + 1} (Epsilon: {agente.epsilon:.2f})")
            sim.visualizador = Visualizador(amb)
        else:
            sim.visualizador = None

        sim.executar_simulacao()
        historico_passos.append(sim.passo)
        historico_recompensa.append(sim.recompensa)

        if (ep + 1) % 50 == 0:
            print(f"Episódio {ep + 1}/{EPISODIOS} completado em {sim.passo} passos.")

    print("--- TREINO CONCLUÍDO ---")

    agente.record_data()

    # 3. Mostrar Gráfico (Para o Relatório)
    passos_np = np.array(historico_passos)
    recompensas_np = np.array(historico_recompensa)

    # Criar uma figura com 2 linhas (ax1 e ax2)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

    # JANELA DE MÉDIA MÓVEL (100 episódios)
    janela = 100

    #gráfico de passos
    media_passos = np.convolve(passos_np, np.ones(janela) / janela, mode='valid')
    ax1.plot(passos_np, alpha=0.3, color='gray', label='Bruto')
    ax1.plot(media_passos, color='blue', label='Média')
    ax1.set_title('Eficiência (Número de Passos)')
    ax1.set_ylabel('Passos (Menor é melhor)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    #gráfico de recomepensas
    media_recompensas = np.convolve(recompensas_np, np.ones(janela) / janela, mode='valid')
    ax2.plot(recompensas_np, alpha=0.3, color='orange', label='Bruto')
    ax2.plot(media_recompensas, color='red', label='Média')
    ax2.set_title('Eficácia (Recompensa Acumulada)')
    ax2.set_ylabel('Pontos (Maior é melhor)')
    ax2.set_xlabel('Episódio')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
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


def gerar_heatmap_valor(ambiente, agente):
    """
    Gera uma matriz com o valor máximo Q (a utilidade) de cada célula do mapa.
    """
    altura = ambiente.height
    largura = ambiente.width

    # Matriz para guardar os valores (inicia com um valor baixo)
    mapa_valores = np.zeros((altura, largura))

    # Salvar a posição original do agente para não estragar nada
    posicao_original = ambiente.posicoes.get(agente)

    print("A gerar Heatmap de Conhecimento...")

    for x in range(altura):
        for y in range(largura):

            # 1. Se for parede, definimos um valor fixo (ex: 0 ou -1) e saltamos
            if ambiente.mapa[x][y] == 1:
                mapa_valores[x][y] = np.nan  # NaN deixa o quadrado vazio/branco no gráfico
                continue

            # 2. Teletransportar o agente para esta célula
            ambiente.posicoes[agente] = (x, y)

            # 3. Pedir aos sensores para lerem o ambiente nesta nova posição
            obs = ambiente.observacaoPara(agente)

            # 4. Injetar a observação no agente (sem mover)
            # Nota: Usamos o método auxiliar interno se o tiveres, ou simulamos o fluxo
            agente.observacao(obs)

            # 5. Obter o Estado Hash dessa observação
            # (Depende de como o teu método get_estado_hash está definido)
            # Se ele lê de self.observacaofinal, isto funciona.
            # Se ele pede argumento, passamos 'obs'.
            try:
                # Tenta passar o argumento (versão mais recente)
                estado = agente.get_estado_hash(obs)
            except TypeError:
                # Fallback para a versão antiga que lê self.observacaofinal
                estado = agente.get_estado_hash()

            # 6. Ler o valor máximo da Q-Table para este estado
            if estado in agente.q_table:
                # O valor desta célula é a melhor recompensa que ele espera obter daqui
                max_q = max(agente.q_table[estado])
                mapa_valores[x][y] = max_q
            else:
                # Se ele nunca viu este estado, o valor é 0 (ou o valor de inicialização)
                mapa_valores[x][y] = 0.0

    # Restaurar posição original
    if posicao_original:
        ambiente.posicoes[agente] = posicao_original

    return mapa_valores


def plotar_heatmap(mapa_valores, titulo="Mapa de Calor (Max Q-Values)"):
    plt.figure(figsize=(8, 6))

    # Usar seaborn se tiveres, senão usa plt.imshow
    try:
        # cmap="viridis" ou "magma" ou "coolwarm" são boas cores
        # annot=True escreve os números (bom para mapas pequenos)
        sns.heatmap(mapa_valores, cmap="viridis", annot=False, fmt=".1f", cbar_kws={'label': 'Valor Esperado (Q)'})
    except NameError:
        # Fallback para matplotlib puro
        plt.imshow(mapa_valores, cmap='viridis', interpolation='nearest')
        plt.colorbar(label='Valor Esperado (Q)')

    plt.title(titulo)
    plt.xlabel("Y (Colunas)")
    plt.ylabel("X (Linhas)")

    # Inverter o eixo Y para o (0,0) ficar no topo esquerdo como nas matrizes
    # (Opcional, depende de como o imshow se comporta)

    plt.show()


if __name__ == "__main__":
    treinar()