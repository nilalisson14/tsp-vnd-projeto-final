import sys
import math
import time
import random


def ler_instancia(caminho):
    """Le uma instancia TSPLIB (EUC_2D) e retorna a lista de coordenadas."""
    coords = []
    lendo = False
    with open(caminho) as arq:
        for linha in arq:
            linha = linha.strip()
            if linha.startswith("NODE_COORD_SECTION"):
                lendo = True
                continue
            if linha.startswith("EOF") or linha == "":
                if lendo:
                    break
                continue
            if lendo:
                partes = linha.split()
                x = float(partes[1])
                y = float(partes[2])
                coords.append((x, y))
    return coords


def matriz_distancias(coords):
    """Calcula a matriz de distancias euclidianas (arredondamento TSPLIB)."""
    n = len(coords)
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dx = coords[i][0] - coords[j][0]
            dy = coords[i][1] - coords[j][1]
            D[i][j] = round(math.sqrt(dx * dx + dy * dy))
    return D


def custo(rota, D):
    """Custo total do ciclo: soma das arestas + retorno a cidade inicial."""
    total = 0
    n = len(rota)
    for i in range(n):
        total += D[rota[i]][rota[(i + 1) % n]]
    return total


# ---------------------------------------------------------------------------
# Heuristica de construcao
# ---------------------------------------------------------------------------

def vizinho_mais_proximo(D, inicio=0):
    """Heuristica gulosa: a cada passo vai para a cidade mais proxima. O(n^2)."""
    n = len(D)
    visitado = [False] * n
    rota = [inicio]
    visitado[inicio] = True
    atual = inicio
    for _ in range(n - 1):
        melhor = -1
        melhor_dist = float("inf")
        for j in range(n):
            if not visitado[j] and D[atual][j] < melhor_dist:
                melhor_dist = D[atual][j]
                melhor = j
        rota.append(melhor)
        visitado[melhor] = True
        atual = melhor
    return rota


# ---------------------------------------------------------------------------
# Movimentos de vizinhanca (melhor melhora)
# ---------------------------------------------------------------------------

def melhor_swap(rota, D):
    """N1 - troca duas cidades de posicao. Retorna o melhor vizinho."""
    n = len(rota)
    melhor = rota
    melhor_custo = custo(rota, D)
    for i in range(n - 1):
        for j in range(i + 1, n):
            nova = rota[:]
            nova[i], nova[j] = nova[j], nova[i]
            c = custo(nova, D)
            if c < melhor_custo:
                melhor_custo = c
                melhor = nova
    return melhor, melhor_custo


def melhor_2opt(rota, D):
    """N2 - remove 2 arcos e religa invertendo o trecho. Retorna o melhor vizinho."""
    n = len(rota)
    melhor = rota
    melhor_custo = custo(rota, D)
    for i in range(n - 1):
        for j in range(i + 1, n):
            nova = rota[:i] + rota[i:j + 1][::-1] + rota[j + 1:]
            c = custo(nova, D)
            if c < melhor_custo:
                melhor_custo = c
                melhor = nova
    return melhor, melhor_custo


def melhor_reinsertion(rota, D):
    """N3 - remove uma cidade e reinsere na melhor posicao. Retorna o melhor vizinho."""
    n = len(rota)
    melhor = rota
    melhor_custo = custo(rota, D)
    for i in range(n):
        sem = rota[:i] + rota[i + 1:]
        cidade = rota[i]
        for k in range(len(sem) + 1):
            nova = sem[:k] + [cidade] + sem[k:]
            c = custo(nova, D)
            if c < melhor_custo:
                melhor_custo = c
                melhor = nova
    return melhor, melhor_custo


# ---------------------------------------------------------------------------
# VND - Variable Neighbourhood Descent
# ---------------------------------------------------------------------------

def vnd(rota, D, vizinhancas):
    """Descida em vizinhanca variavel (pseudocodigo dos slides)."""
    s = rota
    fs = custo(s, D)
    r = len(vizinhancas)
    k = 1
    while k <= r:
        viz = vizinhancas[k - 1]
        s_linha, f_linha = viz(s, D)
        if f_linha < fs:
            s = s_linha
            fs = f_linha
            k = 1
        else:
            k = k + 1
    return s, fs


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("uso: python tsp_vnd.py <instancia.tsp> [num_execucoes]")
        return

    caminho = sys.argv[1]
    execucoes = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    coords = ler_instancia(caminho)
    D = matriz_distancias(coords)
    vizinhancas = [melhor_swap, melhor_2opt, melhor_reinsertion]

    print(f"Instancia: {caminho}")
    print(f"Cidades: {len(coords)}")
    print(f"Execucoes: {execucoes}")
    print("-" * 40)

    melhor_global = float("inf")
    tempos = []

    for e in range(execucoes):
        inicio = random.randrange(len(coords))
        t0 = time.perf_counter()
        rota = vizinho_mais_proximo(D, inicio)
        rota, frota = vnd(rota, D, vizinhancas)
        t1 = time.perf_counter()
        tempos.append(t1 - t0)
        if frota < melhor_global:
            melhor_global = frota

    print(f"Melhor resultado : {melhor_global}")
    print(f"Tempo medio      : {sum(tempos) / len(tempos):.4f} s")


if __name__ == "__main__":
    main()
