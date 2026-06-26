# TSP — Vizinho mais Próximo + VND

Projeto Final da disciplina **Estrutura de Dados e Complexidade de Algoritmos** (CI/UFPB).
Resolução do Problema do Caixeiro Viajante (TSP) com heurística de construção
gulosa (Vizinho mais Próximo) refinada pela meta-heurística **VND**
(Variable Neighbourhood Descent).

## Estrutura

- `tsp_vnd.py` — implementação (leitura TSPLIB, construção, vizinhanças e VND)
- `berlin52.tsp`, `eil51.tsp`, `st70.tsp`, `eil76.tsp`, `kroA100.tsp` — instâncias da TSPLIB

## Componentes

- **Representação:** vetor de rota (permutação de cidades), ciclo fechado
- **Construção:** Vizinho mais Próximo, O(n²)
- **Vizinhanças:** N1 swap, N2 2-opt, N3 re-insertion (melhor melhora)
- **VND:** troca sistemática entre as 3 vizinhanças

## Execução

```
python tsp_vnd.py <instancia.tsp> [num_execucoes]
```

Exemplo:

```
python tsp_vnd.py berlin52.tsp 10
```

A saída mostra o melhor custo encontrado e o tempo médio por execução.

## Resultados (10 execuções, ótimo da TSPLIB)

| Instância | n   | Melhor | Tempo médio (s) | Gap (%) |
|-----------|-----|--------|-----------------|---------|
| eil51     | 51  | 429    | 0,16            | 0,70    |
| berlin52  | 52  | 7542   | 0,18            | 0,00    |
| st70      | 70  | 685    | 0,54            | 1,48    |
| eil76     | 76  | 545    | 0,75            | 1,30    |
| kroA100   | 100 | 21353  | 2,54            | 0,33    |
