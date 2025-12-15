import json
import re  # Para remover comentários
import matplotlib.pyplot as plt
import numpy as np

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

# Sensores
from Sensores.SensorDirecaoAlvo import SensorDirecaoAlvo
from Sensores.SensorProximidadeObstáculo import SensorProximidadeObstáculo
from Sensores.SensorLocalFarol import SensorLocalFarol


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

        # (Opcional) Se o JSON ainda tiver 'ficheiro_cerebro' explicito, podemos respeitar
        if "ficheiro_cerebro" in config_agente:
            agente.file = config_agente["ficheiro_cerebro"]

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
            sim.visualizador = Visualizador(amb) if espreitar else None

            sim.executar_simulacao()

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

        sim = Simulador(amb, lista_agentes)
        if visualizar:
            sim.visualizador = Visualizador(amb)

        sim.executar_simulacao()
        rec_final = getattr(sim, 'recompensa', getattr(sim, 'recompensa_total', 0))
        print(f">>> Resultado Final: {sim.passo} passos | Recompensa: {rec_final}")


if __name__ == "__main__":
    main()