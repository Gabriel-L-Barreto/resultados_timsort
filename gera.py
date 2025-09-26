import random

def gerar_entrada(nome_arquivo, dados):
    with open(nome_arquivo, "w") as f:
        f.write(" ".join(map(str, dados)))


def gerar_entradas():
    tamanhos = {
        "pequena": 10000,
        "media": 500000,
        "grande": 1000000
    }

    for nome, n in tamanhos.items():
        # --- Desordenada (shuffle total) ---
        desordenada = list(range(1, n + 1))
        random.shuffle(desordenada)
        gerar_entrada(f"entrada_{nome}_desordenada.txt", desordenada)

        # --- Pré-ordenada (agora totalmente inversa) ---
        pre_ordenada = list(range(n, 0, -1))
        gerar_entrada(f"entrada_{nome}_reversa.txt", pre_ordenada)

        # --- Ordenada (melhor caso) ---
        ordenada = list(range(1, n + 1))
        gerar_entrada(f"entrada_{nome}_ordenada.txt", ordenada)

        print(f"Arquivos de entrada para {nome} ({n} elementos) gerados.")


if __name__ == "__main__":
    gerar_entradas()
