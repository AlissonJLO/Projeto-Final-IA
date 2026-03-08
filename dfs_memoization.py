import json
import time
from functools import cache

dificuldades = []
poderes = []

@cache
def dfs_batalhas(casa_atual, e0, e1, e2, e3, e4):
    if casa_atual == 12:
        if e0 > 0 or e1 > 0 or e2 > 0 or e3 > 0 or e4 > 0:
            return 0.0, 0
        else:
            return 999999.0, 0

    menor_tempo = float('inf')
    melhor_equipe = 0

    for mask in range(1, 32):
        n0, n1, n2, n3, n4 = e0, e1, e2, e3, e4
        soma_poder = 0.0
        equipe_valida = True

        if mask & 1:
            if n0 == 0: equipe_valida = False
            else: n0 -= 1; soma_poder += poderes[0]
        if mask & 2:
            if n1 == 0: equipe_valida = False
            else: n1 -= 1; soma_poder += poderes[1]
        if mask & 4:
            if n2 == 0: equipe_valida = False
            else: n2 -= 1; soma_poder += poderes[2]
        if mask & 8:
            if n3 == 0: equipe_valida = False
            else: n3 -= 1; soma_poder += poderes[3]
        if mask & 16:
            if n4 == 0: equipe_valida = False
            else: n4 -= 1; soma_poder += poderes[4]

        if not equipe_valida:
            continue

        tempo_nesta_casa = dificuldades[casa_atual] / soma_poder
        tempo_futuro, _ = dfs_batalhas(casa_atual + 1, n0, n1, n2, n3, n4)
        
        tempo_total = tempo_nesta_casa + tempo_futuro

        if tempo_total < menor_tempo:
            menor_tempo = tempo_total
            melhor_equipe = mask

    return menor_tempo, melhor_equipe

def executar_dfs():
    global dificuldades, poderes

    print("Carregando dados do input.json...")
    with open("input.json", "r", encoding="utf-8") as f:
        dados = json.load(f)
    
    ouros = dados["config_ouros"]
    bronzes = dados["config_bronzes"]
    
    dificuldades = list(ouros.values())
    poderes = list(bronzes.values())

    print("Calculando rotas otimizadas com DFS + Memoization...")
    inicio_tempo = time.time()
    
    melhor_tempo, _ = dfs_batalhas(0, 5, 5, 5, 5, 5)
    
    fim_tempo = time.time()
    print(f"Busca concluída em {(fim_tempo - inicio_tempo) * 1000:.2f} ms!")
    print(f"Tempo ótimo encontrado: {melhor_tempo:.2f} minutos.")
    
    dna_campeao = []
    e = [5, 5, 5, 5, 5]
    
    for casa in range(12):
        _, melhor_mask = dfs_batalhas(casa, e[0], e[1], e[2], e[3], e[4])
        
        linha = [0, 0, 0, 0, 0]

        if melhor_mask & 1: linha[0] = 1; e[0] -= 1
        if melhor_mask & 2: linha[1] = 1; e[1] -= 1
        if melhor_mask & 4: linha[2] = 1; e[2] -= 1
        if melhor_mask & 8: linha[3] = 1; e[3] -= 1
        if melhor_mask & 16: linha[4] = 1; e[4] -= 1
        
        dna_campeao.append(linha)

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump({"dna_campeao": dna_campeao}, f)
    
    print("Matriz campeã exportada para output.json com sucesso!")