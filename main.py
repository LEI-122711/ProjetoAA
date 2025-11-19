# Importamos a classe concreta (não a interface!)
# Nota: "from Pasta.Ficheiro import Classe"
from Ambiente.Ambiente1 import Ambiente1


def testar_ambiente():
    print("--- INÍCIO DO TESTE ---")

    try:
        # 1. Tentar instanciar (Criar o objeto)
        # Se falhar aqui, é porque faltam métodos abstratos na classe Ambiente1
        print("1. A tentar criar o Ambiente1...")
        meu_ambiente = Ambiente1()
        print("   -> SUCESSO: Ambiente criado!")

        # 2. Tentar usar o método
        print("2. A tentar chamar o método 'adeus'...")
        meu_ambiente.adeus()
        print("   -> SUCESSO: Método executado!")

    except TypeError as e:
        print("\n[ERRO FATAL]: Não foi possível criar o ambiente.")
        print(f"Motivo: {e}")
        print("Dica: Verifique se implementou TODOS os métodos da Interface no Ambiente1.")

    except Exception as e:
        print(f"\n[ERRO]: Aconteceu algo inesperado: {e}")

    print("--- FIM DO TESTE ---")


if __name__ == "__main__":
    testar_ambiente()