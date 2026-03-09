# 🌌 A Travessia das 12 Casas - Inteligência Artificial

Este repositório contém a solução do Trabalho Prático da disciplina de Inteligência Artificial. O objetivo do sistema é guiar os Cavaleiros de Bronze pelo mapa do Santuário, gerenciando a navegação física pelos terrenos através do **Algoritmo A\*** e comparando duas abordagens distintas para encontrar a melhor combinação de lutas contra os Cavaleiros de Ouro: um **Algoritmo Genético** e uma **Busca em Profundidade (DFS) com Memoization**. O objetivo final é salvar Atena dentro do limite de 720 minutos e sobreviver ao rígido gasto de energia.

---

## 🏗️ Estrutura do Projeto

O código foi refatorado utilizando uma arquitetura profissional modular, separando completamente o "cérebro" (IA), o "motor de regras" (Engine), os dados (Data) e a "visualização" (GUI).

```text
Trabalho_Final_IA/
│
├── main.py                     # Ponto de entrada do sistema
├── README.md                   # Documentação
│
├── data/                       # Arquivos de Dados e Configurações
│   ├── coordernadasmapaco.csv  # Matriz 42x42 com terrenos e casas
│   ├── input.json              # Configurações dinâmicas de atributos e IA
│   ├── output.json             # DNA gerado autonomamente pela IA
│   └── log_simulacao.txt       # Relatório de desempenho gerado ao final
│
└── src/                        # Código Fonte Principal
    ├── ai/                     # Módulos de Inteligência Artificial
    │   ├── algoritmo_genetico.py
    │   ├── dfs_memoization.py
    │   └── busca_estrela.py
    │
    ├── engine/                 # Motor de Regras de Negócio e Estados
    │   └── logica.py
    │
    └── gui/                    # Interface Visual Pygame
        └── interface_hud.py
```


### ⚙️ Códigos Fonte (`src/`)

- **`src/ai/busca_estrela.py`**: Implementa o algoritmo A\* (A-Estrela) para navegação espacial, calculando a rota física mais rápida, desviando de montanhas.
- **`src/ai/dfs_memoization.py`**: Motor de Busca Exata. Utiliza DFS otimizada com Programação Dinâmica (Cache) e operações binárias para avaliar subproblemas sobrepostos e garantir a solução ótima absoluta.
- **`src/ai/algoritmo_genetico.py`**: Motor de Busca Heurística. Gera populações de estratégias de luta, aplica _crossover_ e mutação, aproximando-se do tempo ótimo de forma evolutiva.
- **`src/engine/logica.py`**: O Motor de Simulação. Aplica os custos de terreno (Plano, Rochoso, Montanhoso), gerencia os passos no mapa e calcula as penalidades de dano e energia.
- **`src/gui/interface_hud.py`**: A Interface Gráfica. Utiliza Pygame para desenhar um Painel Tático (HUD) dinâmico com ícones coloridos, reproduzindo a simulação para avaliação visual em tempo real.

---

## 🛠️ Configurações Parametrizáveis (`data/input.json`)

O sistema foi construído para ser dinâmico. Você pode alterar as variáveis do ambiente diretamente no arquivo `data/input.json` **sem precisar mexer no código-fonte**.

- **Forças Cósmicas:** Altere os valores em `config_ouros` e `config_bronzes` para mudar a dificuldade do jogo.
- **Parâmetros do Genético:** As chaves `"tamanho_pop"` e `"num_geracoes"` definem o esforço computacional do Algoritmo Genético. Modifique-as para testar a diferença entre execuções mais rápidas ou convergências mais precisas (ex: 1000 de população e 100 gerações).

---

## 🚀 Como Instalar e Executar

### Pré-requisitos

Certifique-se de ter o **Python 3** instalado em sua máquina e a biblioteca `pygame` para a renderização da interface.

1. Abra o terminal na pasta raiz do projeto (`Trabalho_Final_IA`).
2. Instale as dependências executando:

```bash
pip install pygame

```

### Iniciando a Simulação

Para rodar o projeto completo, execute o orquestrador na raiz da pasta:

```bash
python main.py

```

**O que vai acontecer:**

1. O terminal exibirá um **menu interativo** perguntando qual motor tático utilizar para as batalhas: **DFS** ou **Genético**.
2. O algoritmo calculará a melhor combinação de lutas e a rota física será traçada pelo algoritmo **A\***.
3. A interface Pygame abrirá automaticamente, exibindo o mapa limpo à esquerda e o Painel de Controle (HUD) à direita.
4. O agente percorrerá a rota. Ao entrar em uma Casa, ocorrerá uma "pausa dramática" na simulação para o cálculo do embate, e a energia da equipe cairá no painel visualmente.
5. Ao alcançar o Grande Mestre (objetivo verde), o relatório detalhado será salvo em `data/log_simulacao.txt` e o teste será concluído.

---

## 👥 Membros do Grupo

- **Alisson Joaquim Lara Oliveira** – Interface Gráfica (GUI) e Integração Front-end
- **Enzo Magalhães Campos** – Otimização Heurística (Algoritmo Genético)
- **Marco Antonio Jobim Filho** – Busca Exata e Programação Dinâmica (DFS com Memoization)
- **Gabriel Bernardelli Esteves** – Navegação Espacial (Algoritmo A\*)