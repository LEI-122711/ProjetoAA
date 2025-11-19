class Observacao:

    def __init__(self,dados: dict):
        self._dados = dados
        pass

    @property
    def dados(self):
        return self._dados

