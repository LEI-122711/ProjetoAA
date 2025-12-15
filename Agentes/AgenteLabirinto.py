from Agentes.Agent_Interface import Agente_Interface
from Acao import Acao


class AgenteLabirinto(Agente_Interface):

    def __init__(self):
        super().__init__()
        self.observacaofinal = None

        # Bússola 8 direções (Sentido Horário)
        # 0:Norte, 1:NE, 2:Este, 3:SE, 4:Sul, 5:SO, 6:Oeste, 7:NO
        self.bussola = [
            (-1, 0), (-1, 1), (0, 1), (1, 1),
            (1, 0), (1, -1), (0, -1), (-1, -1)
        ]

        # Estado Interno
        self.encontrou_parede = False
        self.heading_idx = 0  # Para onde estou virado (Índice da bússola)

    def cria(self, ficheiro: str):
        pass

    def observacao(self, observacao):
        self.observacaofinal = observacao

    def _obter_indice_bussola(self, vetor):
        """Converte vetor (dx,dy) em índice da bússola (0-7)"""
        if vetor in self.bussola:
            return self.bussola.index(vetor)
        return 0  # Default

    def age(self):
        if self.observacaofinal is None:
            return Acao("andar", dx=0, dy=0)

        dados = self.observacaofinal.dados
        dx_meta, dy_meta = dados.get("direcao", (0, 0))
        visao = dados.get("visao")  # Matriz 3x3

        if visao is None:
            return Acao("andar", dx=0, dy=0)

        # Se chegou ao objetivo, para
        if dx_meta == 0 and dy_meta == 0:
            return Acao("andar", dx=0, dy=0)

        # --- FASE 1: MODO LIVRE (Ir direto ao GPS) ---
        if not self.encontrou_parede:
            # Verifica se o movimento do GPS é válido (Livre = 0)
            # O agente está em visao[1][1]. Alvo é visao[1+dx][1+dy]

            # Se o GPS for (0,0) ou inválido, ignora
            if (dx_meta, dy_meta) == (0, 0):
                return Acao("andar", dx=0, dy=0)

            try:
                if visao[1 + dx_meta][1 + dy_meta] == 0:
                    # Caminho livre! Atualiza a nossa "frente" e anda.
                    self.heading_idx = self._obter_indice_bussola((dx_meta, dy_meta))
                    return Acao("andar", dx=dx_meta, dy=dy_meta)
                else:
                    # BATEU! Ativar Modo "Seguir Parede"
                    self.encontrou_parede = True
                    # A nossa "frente" passa a ser a direção onde batemos
                    self.heading_idx = self._obter_indice_bussola((dx_meta, dy_meta))
            except IndexError:
                pass

        # --- FASE 2: MODO SEGUIR PAREDE (Right-Hand Rule) ---
        if self.encontrou_parede:
            # A lógica é varrer as direções começando pela nossa DIREITA.
            # Num relógio, a Direita (90º) é o índice atual + 2.
            # Vamos testar: Direita -> Frente-Direita -> Frente -> Frente-Esquerda -> Esquerda...

            start_scan = (self.heading_idx + 2) % 8

            for i in range(8):
                # Varrer no sentido anti-horário (para a esquerda) a partir da direita
                idx_teste = (start_scan - i) % 8

                dx, dy = self.bussola[idx_teste]

                try:
                    if visao[1 + dx][1 + dy] == 0:
                        # Encontrou passagem!
                        # Atualiza a orientação para a nova direção e move-se
                        self.heading_idx = idx_teste
                        return Acao("andar", dx=dx, dy=dy)
                except IndexError:
                    pass

        # Se tudo falhar (encurralado), tenta ficar parado
        return Acao("andar", dx=0, dy=0)

    def avaliacao_estado_atual(self, recompensa: float):
        pass