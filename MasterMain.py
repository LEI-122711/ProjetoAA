import json
import re  # Para remover comentários
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sympy import false

# --- IMPORTS DO PROJETO ---
from Simulador import Simulador
from Visualizador import Visualizador

# Ambientes
from Ambiente.AmbienteFarol import AmbienteFarol
from Ambiente.AmbienteLabirinto import AmbienteLabirinto

# Agentes
from Agentes.AgenteLabirintoQLearning import AgenteLabirintoQLearning
from Agentes.AgenteFarolQLearning1 import AgenteFarolQLearning
from Agentes.AgenteLabirinto import AgenteLabirinto
from Agentes.AgenteFarol1 import AgenteFarol1
from Agentes.AgenteGenetico import AgenteGenetico

# Sensores
from Sensores.SensorDirecaoAlvo import SensorDirecaoAlvo
from Sensores.SensorProximidadeObstáculo import SensorProximidadeObstáculo


# --- FUNÇÕES AUXILIARES DE MAPA (Do Labirinto) ---
def get_mapa_labirinto(dificuldade):
    if dificuldade == 1:
        return [
            [0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ], (0, 0), (6, 4)
    elif dificuldade == 2:
        return [
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
        ], (0, 0), (10, 10)
    elif dificuldade == 3:
        return [
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
        ], (0, 0), (9, 10)
    elif dificuldade == 4:
        return [
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
            [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
        ], (0, 0), (19, 19)
    elif dificuldade == 5: #modificação do 4 com mais buracos para ver se o qlearning melhora
        return [
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
            [0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
        ], (0, 0), (11, 9)
    return None

# --- LEITURA DE JSON COM COMENTÁRIOS ---
def carregar_configuracao(ficheiro="config.json"):
    with open(ficheiro, 'r', encoding='utf-8') as f:
        conteudo = f.read()
        # Regex mágica para remover linhas que começam por //
        conteudo_limpo = re.sub(r'^\s*//.*$', '', conteudo, flags=re.MULTILINE)
        return json.loads(conteudo_limpo)

# --- FÁBRICA DE AMBIENTES ---
def criar_ambiente(config_amb):
    tipo = config_amb["tipo"].lower()

    if tipo == "farol":
        amb = AmbienteFarol()
        # Adicionar obstáculos extra definidos no JSON
        obstaculos = config_amb.get("obstaculos_extra", [])
        for obs in obstaculos:
            amb.add_obstaculo(obs[0], obs[1])
        return amb

    elif tipo == "labirinto":
        dif = config_amb.get("dificuldade", 1)
        mapa, inicio, fim = get_mapa_labirinto(dif)
        amb = AmbienteLabirinto(mapa, inicio, fim)
        return amb

    else:
        raise ValueError(f"Ambiente desconhecido: {tipo}")


# --- FÁBRICA DE AGENTES ---
# ALTERAÇÃO: Recebe agora 'config_ambiente' completo, não apenas o tipo
def criar_agente(config_agente, config_ambiente):
    classe = config_agente["classe"]
    ambiente_tipo = config_ambiente["tipo"].lower()

    agente = None
    if classe == "AgenteQLearning":
        lr = config_agente.get("learning_rate", 0.1)
        df = config_agente.get("discount_factor", 0.9)

        if ambiente_tipo == "farol":
            agente = AgenteFarolQLearning(learning_rate=lr, discount_factor=df)
            # Nome automático para Farol
            agente.file = "farolQLearning_data.json"
        else:
            # Labirinto
            dif = config_ambiente.get("dificuldade", 1)
            # Passamos a dificuldade para o construtor do agente
            agente = AgenteLabirintoQLearning(learning_rate=lr, discount_factor=df, dificuldade=dif)
            # Nome automático para Labirinto
            agente.file = f"labirintoQLearning{dif}.json"


    elif classe == "AgenteGenetico":
        agente = AgenteGenetico()
        if ambiente_tipo == "farol":
            agente.file = "farolGenetico_Best.json"
        else:
            dif = config_ambiente.get("dificuldade", 1)
            agente.file = f"labirintoGenetico_Best{dif}.json"

    elif classe == "AgenteLabirinto":
        agente = AgenteLabirinto()
    elif classe == "AgenteFarol1":
        agente = AgenteFarol1()
    else:
        raise ValueError(f"Agente desconhecido: {classe}")

    # 2. Instalar Sensores (Kit Padrão)
    # Todos levam GPS e Obstáculos para garantir compatibilidade
    agente.instala(SensorDirecaoAlvo())
    agente.instala(SensorProximidadeObstáculo(raio=1))

    return agente


# --- LOOP PRINCIPAL ---
def main():
    print(">>> A Ler Configuração...")
    config = carregar_configuracao("config.json")

    modo = config["modo"]
    visualizar = config["visualizar"]

    # 1. SETUP INICIAL
    amb = criar_ambiente(config["ambiente"])

    lista_agentes = []
    for conf_ag in config["agentes"]:
        # CORREÇÃO AQUI: Passamos config["ambiente"] inteiro, não apenas ["tipo"]
        ag = criar_agente(conf_ag, config["ambiente"])
        lista_agentes.append(ag)
        amb.add_agente(ag)

    print(f">>> Modo: {modo.upper()} | Ambiente: {config['ambiente']['tipo']}")

    # --- MODO TREINO ---
    if modo == "treino":
        conf_treino = config["treino"]
        episodios = conf_treino["episodios"]
        agente_principal = lista_agentes[0]

        historico_passos = []
        historico_recompensa = []

        start_epsilon = 1.0
        target_epsilon = 0.01

        fator_decaimento = conf_treino.get("fator_decaimento_epsilon", 0.9)

        print(f">>> A Iniciar Treino de {episodios} episódios...")

        for ep in range(episodios):
            amb = criar_ambiente(config["ambiente"])
            amb.add_agente(agente_principal)

            divisor = (episodios - 1) * fator_decaimento
            if divisor > 0:
                novo_eps = start_epsilon - ep * (start_epsilon - target_epsilon) / divisor
                agente_principal.epsilon = max(target_epsilon, novo_eps)

            espreitar = visualizar and ((ep == 0) or (ep == episodios - 1))

            sim = Simulador(amb, [agente_principal])
            sim.visualizador = Visualizador(amb, gravar_gif=False) if espreitar else None

            sim.executar_simulacao()

            rec_total = getattr(sim, 'recompensa', getattr(sim, 'recompensa_total', 0))

            if hasattr(agente_principal, 'fim_episodio'):
                agente_principal.fim_episodio(rec_total)

            historico_passos.append(sim.passo)
            # Compatibilidade com diferentes versões do simulador
            rec = getattr(sim, 'recompensa', getattr(sim, 'recompensa_total', 0))
            historico_recompensa.append(rec)

            if (ep + 1) % (episodios // 10) == 0:
                print(f"Ep {ep + 1}: {sim.passo} passos (Eps: {agente_principal.epsilon:.2f})")


        if hasattr(agente_principal, 'record_data'):
            # Agora ele usa o self.file definido automaticamente na criação
            agente_principal.record_data()

        # Gráficos
        print(">>> A Gerar Gráficos...")
        passos_np = np.array(historico_passos)
        recompensas_np = np.array(historico_recompensa)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        janela = 100 if episodios > 100 else 10

        # Passos
        if len(passos_np) >= janela:
            media_passos = np.convolve(passos_np, np.ones(janela) / janela, mode='valid')
            ax1.plot(passos_np, alpha=0.3, color='gray', label='Bruto')
            ax1.plot(media_passos, color='blue', label='Média')
        else:
            ax1.plot(passos_np, color='blue', label='Bruto')

        ax1.set_title(f"Eficiência (Passos) - {config['ambiente']['tipo']}")
        ax1.set_ylabel('Passos (Menor é melhor)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Recompensas
        if len(recompensas_np) >= janela:
            media_recompensas = np.convolve(recompensas_np, np.ones(janela) / janela, mode='valid')
            ax2.plot(recompensas_np, alpha=0.3, color='orange', label='Bruto')
            ax2.plot(media_recompensas, color='red', label='Média')
        else:
            ax2.plot(recompensas_np, color='red', label='Bruto')

        ax2.set_title('Eficácia (Recompensa Acumulada)')
        ax2.set_ylabel('Pontos (Maior é melhor)')
        ax2.set_xlabel('Episódio')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    # --- MODO TESTE ---
    elif modo == "teste":
        print(">>> A Executar Teste...")

        for ag in lista_agentes:
            if hasattr(ag, 'load_data'):
                try:
                    # O agente já tem o self.file configurado desde a criação.
                    ag.load_data()
                except:
                    print(f"Aviso: Sem memória encontrada para {ag.file}.")

            if hasattr(ag, 'learning_mode'):
                ag.learning_mode = False
                ag.epsilon = 0.0

        if len(lista_agentes) == 1:
            agente_teste = lista_agentes[0]
            # Verifica se tem q_table (é QLearning)
            if hasattr(agente_teste, 'q_table'):
                amb.add_agente(agente_teste)  # Temporário para scan
                mapa_calor = gerar_heatmap_valor(amb, agente_teste)
                plotar_heatmap(mapa_calor, titulo=f"Heatmap - {config['ambiente']['tipo']}")
                # Remove para reiniciar limpo
                amb.posicoes = {}
                amb.agentes = []
                amb.add_agente(agente_teste)

        sim = Simulador(amb, lista_agentes)

        if visualizar:
            sim.visualizador = Visualizador(amb, gravar_gif=True)

        sim.executar_simulacao()
        rec_final = getattr(sim, 'recompensa', getattr(sim, 'recompensa_total', 0))
        print(f">>> Resultado Final: {sim.passo} passos | Recompensa: {rec_final}")

        if sim.visualizador and hasattr(sim.visualizador, 'gravar_gif') and sim.visualizador.gravar_gif:
            tipo_amb = config["ambiente"]["tipo"]
            dif = config["ambiente"].get("dificuldade", "")
            str_dif = f"_dif{dif}" if dif else ""
            nome_agente = lista_agentes[0].__class__.__name__

            nome_ficheiro = f"teste_{tipo_amb}{str_dif}_{nome_agente}.gif"
            sim.visualizador.salvar_gif(nome_ficheiro)


def gerar_heatmap_valor(ambiente, agente):
    """
    Gera uma matriz com o valor máximo Q (a utilidade) de cada célula do mapa.
    """
    altura = ambiente.height
    largura = ambiente.width

    mapa_valores = np.zeros((altura, largura))
    posicao_original = ambiente.posicoes.get(agente)

    print(">>> A gerar Heatmap de Conhecimento...")

    for x in range(altura):
        for y in range(largura):
            # Se for parede, valor nulo
            if ambiente.mapa[x][y] == 1:
                mapa_valores[x][y] = np.nan
                continue

            # Teletransportar agente e ver o que ele acha
            ambiente.posicoes[agente] = (x, y)
            obs = ambiente.observacaoPara(agente)
            agente.observacao(obs)

            try:
                # Tenta obter estado (compatível com várias versões do agente)
                try:
                    estado = agente.get_estado_hash(obs)
                except TypeError:
                    estado = agente.get_estado_hash()

                # Ler valor máximo Q
                if hasattr(agente, 'q_table') and estado in agente.q_table:
                    max_q = max(agente.q_table[estado])
                    mapa_valores[x][y] = max_q
                else:
                    mapa_valores[x][y] = 0.0
            except Exception:
                mapa_valores[x][y] = 0.0

    # Restaurar posição original
    if posicao_original:
        ambiente.posicoes[agente] = posicao_original

    return mapa_valores


def plotar_heatmap(mapa_valores, titulo="Mapa de Calor (Max Q-Values)"):
    plt.figure(figsize=(8, 6))
    try:
        sns.heatmap(mapa_valores, cmap="viridis", annot=False, fmt=".1f", cbar_kws={'label': 'Valor Esperado (Q)'})
    except NameError:
        plt.imshow(mapa_valores, cmap='viridis', interpolation='nearest')
        plt.colorbar(label='Valor Esperado (Q)')

    plt.title(titulo)
    plt.xlabel("Y (Colunas)")
    plt.ylabel("X (Linhas)")
    plt.show()


if __name__ == "__main__":
    main()