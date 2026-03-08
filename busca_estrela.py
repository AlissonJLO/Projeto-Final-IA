import heapq #crio uma fila de prioridade para pegar o nó com menor custo


def heuristica(a, b): #Distância de Manhattan para calcular a distância entre dois pontos em um plano 2D sem diagonais
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def obter_vizinhos(pos): #recebe uma posição do mapa (x,y)
    x, y = pos #desempacota a posição do mapa
    return [ #retorna as posições ao redor da posição atual
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]


def custo_terreno(valor): #recebe a posição no mapa (x, y)e retorna o custo desse terreno
    if valor == 14:   #montanhoso
        return 200
    elif valor == 16: #rochoso
        return 5
    elif valor == 15: #plano
        return 1
    else:
        return 1


def a_estrela(mapa, inicio, objetivo): #recebe a matriz do terreno, pos inicial e finao (x,y)

    linhas = len(mapa) #descobre quantidade de linhas do mapa
    colunas = len(mapa[0]) #descobre quantidade de colunas do mapa para não fugir dele

    open_set = [] #cria uma lista vazia que guardará os nós a serem explorados ordenados pelo custo total
    heapq.heappush(open_set, (0, inicio))

    veio_de = {} #guarda de onde cada posição veio para reconstruir o caminho depois de chegar ao objetivo

    g_score = {inicio: 0} #guarda o custo real do caminho do inicio até cada posição

    while open_set:

        _, atual = heapq.heappop(open_set) #remove a prioridade e reorganiza a fila
        if atual == objetivo:

            caminho = [atual]

            while atual in veio_de:
                atual = veio_de[atual]
                caminho.append(atual)

            caminho.reverse()
            return caminho

        for vizinho in obter_vizinhos(atual):

            x, y = vizinho

            if x < 0 or y < 0 or x >= colunas or y >= linhas:
                continue

            terreno = mapa[y][x]
            custo = custo_terreno(terreno)

            novo_g = g_score[atual] + custo

            if vizinho not in g_score or novo_g < g_score[vizinho]:

                g_score[vizinho] = novo_g

                f = novo_g + heuristica(vizinho, objetivo)

                heapq.heappush(open_set, (f, vizinho))

                veio_de[vizinho] = atual

    return []