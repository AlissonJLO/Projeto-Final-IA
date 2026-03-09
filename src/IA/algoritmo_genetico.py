import random
import copy
import json

ouros = {
    "Áries" : 50,
    "Touro" : 55,
    "Gêmeos" : 60,
    "Câncer" : 70,
    "Leão" : 75,
    "Virgem" : 80,
    "Libra" : 85,
    "Escorpião" : 90,
    "Sagitário" : 95,
    "Capricórnio" : 100,
    "Aquário" : 110,
    "Peixes" : 120
}

bronzes = {
    "Seiya": 1.5,
    "Shiryu": 1.4,
    "Hyoga": 1.3,
    "Shun": 1.2,
    "Ikki": 1.1
}

tamanho_pop = 1000
num_geracoes = 100

def sincronizar_com_gui():
    global ouros, bronzes, tamanho_pop, num_geracoes  # Avisamos o Python que vamos atualizar as globais
    try:
        with open("data/input.json", "r", encoding="utf-8") as f:
            dados_gui = json.load(f)

            # O segredo está aqui: o método .update() substitui os valores
            # sem mudar o tipo da variável ou o nome.
            ouros.update(dados_gui["config_ouros"])
            bronzes.update(dados_gui["config_bronzes"])

            tamanho_pop = dados_gui.get("tamanho_pop", tamanho_pop)
            num_geracoes = dados_gui.get("num_geracoes", num_geracoes)

        print("Dados da GUI sincronizados com sucesso.")
    except Exception as e:
        # Se o arquivo não existir ou o JSON estiver errado, ele usa o fixo
        print(f"Aviso: Usando dicionários fixos (Erro: {e})")

# 1 = Lutando, 0 = Descansando
# [Seiya, Shiryu, Hyoga, Shun, Ikki]
individuo = [
    [1, 1, 0, 0, 0], # Áries
    [0, 1, 1, 0, 0], # Touro
    [0, 0, 1, 1, 0], # Gêmeos
    [0, 0, 0, 1, 1],  # Câncer
    [0, 0, 0, 0, 1],  # Leão
    [1, 1, 0, 0, 0],  # Virgem
    [0, 1, 0, 0, 0],  # Libra
    [0, 0, 1, 1, 0],  # Escorpião
    [0, 0, 0, 0, 1],  # Sagitário
    [0, 0, 0, 0, 1],  # Capricórnio
    [0, 0, 0, 1, 0],  # Aquário
    [0, 0, 1, 0, 0],  # Peixes
]

nomes_bronzes = list(bronzes.keys())
nomes_ouros = list(ouros.keys())


def Fitness (individuo):
    tempo_total = 0
    energia = [5,5,5,5,5]

    for  casas, lutas in enumerate(individuo):  # Itera sobre cada Luta
        poder_ouro = ouros[nomes_ouros[casas]]
        poder_bronze = 0

        for indice, cavaleiro in enumerate(lutas):  # Calculadora de bronzes
            if cavaleiro == 1:
                poder_bronze += bronzes[nomes_bronzes[indice]]
                energia[indice] -= 1
        if poder_bronze > 0: # Evitar divisão por zero para preservar o programa em caso de have indivíduos com zero lutadores
            tempo_total += poder_ouro/poder_bronze
        else:
            tempo_total += 1000

    # --- Verificação de validade final ---
    # Contamos quantos erros de energia aconteceram
    erros_energia = 0
    for i in energia:
        if i < 0:
            erros_energia += abs(i)

    # Verificamos se alguém sobrou (conforme sua lógica original)
    # Obs: Se todos lutarem exatamente 5 vezes, i será 0.
    # Se você quer permitir que todos usem toda a energia, mude para i >= 0
    alguem_sobrou = any(i >= 1 for i in energia)

    # --- Retorno Inteligente ---

    # Caso 1: Perfeito (Válido)
    if erros_energia == 0 and alguem_sobrou:
        return tempo_total

    # Caso 2: Erro de "Todos morreram" (Penalidade Nível 1)
    if erros_energia == 0 and not alguem_sobrou:
        return 1000 + tempo_total

    # Caso 3: Estourou Energia (Erro Grave - Penalidade Nível 2)
    # Quanto mais estourou, pior a nota
    return 2000 + (erros_energia * 100) + tempo_total


def gerar_individuo(): # Essa função e a de baixo são para implementar a população incial
    # Cria uma matriz 12x5 com 0 ou 1 aleatórios
    return [[(1 if random.random() < 0.3 else 0) for _ in range(5)] for _ in range(12)]


def pop_inicial(tamanho_populacao):
    populacao_avaliada = []

    for _ in range(tamanho_populacao):
        # 1. Gera o DNA (A matriz 12x5)
        novo_individuo = gerar_individuo()

        # 2. Calcula o Fitness imediatamente
        nota = Fitness(novo_individuo)

        # 3. Já guarda o par [DNA, Nota] na tabela
        populacao_avaliada.append([novo_individuo, nota])

    return populacao_avaliada
def crossover(pai1, pai2):
    # Sorteia dois pontos aleatórios para fatiar o DNA
    p1 = random.randint(1, 5)
    p2 = random.randint(7, 11)

    import copy
    # O filho herda: [Pai1(Início), Pai2(Meio), Pai1(Fim)]
    filho = copy.deepcopy(pai1[:p1]) + \
            copy.deepcopy(pai2[p1:p2]) + \
            copy.deepcopy(pai1[p2:])

    return filho

def mutacao(dna, taxa_mutacao=0.05):
    # 'dna' é a matriz 12x5
    # Para cada casa e cada cavaleiro, existe uma pequena chance de mudar

    for i in range(len(dna)):  # Percorre as 12 casas
        for j in range(len(dna[i])):  # Percorre os 5 cavaleiros

            if random.random() < taxa_mutacao:
                # Inverte o bit: se era 0 vira 1, se era 1 vira 0
                dna[i][j] = 1 if dna[i][j] == 0 else 0

    return dna

def reparar_individuo(dna):
    energia_maxima = 5
    for cavaleiro_idx in range(5):
        # Conta em quantas casas esse cavaleiro está lutando
        lutas = [casa_idx for casa_idx in range(12) if dna[casa_idx][cavaleiro_idx] == 1]

        # Se ele lutou mais que 5, "desligamos" casas aleatórias até chegar em 5
        while len(lutas) > energia_maxima:
            casa_para_remover = random.choice(lutas)
            dna[casa_para_remover][cavaleiro_idx] = 0
            lutas.remove(casa_para_remover)
    return dna

def gerar_proxima_geracao(populacao_atual, tamanho_pop=1000):
    populacao_atual.sort(key=lambda x: x[1])
    nova_geracao = []

    # 1. ELITISMO
    for i in range(5):
        nova_geracao.append(copy.deepcopy(populacao_atual[i]))

    # 2. FILTRO DE PAIS
    # Pegamos os 200 melhores da lista
    pais_disponiveis = populacao_atual[:200]

    # 3. REPRODUÇÃO
    while len(nova_geracao) < tamanho_pop:
        pai1 = random.choice(pais_disponiveis)[0]
        pai2 = random.choice(pais_disponiveis)[0]

        dna_filho = crossover(pai1, pai2)
        dna_filho = mutacao(dna_filho)
        dna_filho = reparar_individuo(dna_filho)

        nota_filho = Fitness(dna_filho)
        nova_geracao.append([dna_filho, nota_filho])

    return nova_geracao


# --- INICIANDO A MÁQUINA ---

if __name__ == "__main__":
    sincronizar_com_gui() # Atualiza as forças antes de criar a pop_inicial

    # Gera a população de teste
    populacao_atual = pop_inicial(tamanho_pop)

    print(f"Iniciando evolução... População Inicial: {len(populacao_atual)} indivíduos.")

    for g in range(num_geracoes):
        # Gera a nova população a partir da atual
        populacao_atual = gerar_proxima_geracao(populacao_atual, tamanho_pop=tamanho_pop)

        # Como a função já ordena, o melhor está sempre no índice 0
        melhor_tempo = populacao_atual[0][1]

        # Printa o progresso a cada geração
        print(f"Geração {g:03d} | Melhor Tempo: {melhor_tempo:.2f}")

    # --- RESULTADO FINAL ---

    print("\n" + "=" * 30)
    print("EVOLUÇÃO CONCLUÍDA")
    print(f"Melhor tempo alcançado: {populacao_atual[0][1]:.2f} min")
    print("Estratégia (Matriz 12x5):")
    for linha in populacao_atual[0][0]:
        print(linha)
    print("=" * 30)

    # --- EXPORTAR PARA ARQUIVO DE SAÍDA ---
    with open("output.json", "w") as f:
        # Salvamos apenas a matriz do campeão
        json.dump({"dna_campeao": populacao_atual[0][0]}, f)


