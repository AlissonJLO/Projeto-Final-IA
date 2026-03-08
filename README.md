# 🌌 A Travessia das 12 Casas - Inteligência Artificial

Este repositório contém a solução do Trabalho Prático da disciplina de Inteligência Artificial. O objetivo do sistema é guiar os Cavaleiros de Bronze pelo mapa do Santuário, gerenciando a navegação pelos terrenos e utilizando um **Algoritmo Genético** para encontrar a melhor combinação de lutas contra os Cavaleiros de Ouro, salvando Atena dentro do limite de 720 minutos e sobrevivendo ao gasto de energia.

---

## 🏗️ Estrutura do Projeto

O código foi construído utilizando um padrão inspirado no **MVC (Model-View-Controller)**, separando completamente o "cérebro" (Algoritmo Genético), o "motor de regras" (Backend) e a "visualização" (Frontend).

### ⚙️ Códigos Fonte (Python)

- **`main.py`**: O Orquestrador. É o arquivo principal que o usuário deve rodar. Ele executa o Algoritmo Genético primeiro e, em seguida, inicia a visualização gráfica automaticamente.
- **`dfs_memoization.py`**: A Busca Exata. Motor de IA que utiliza Busca em Profundidade (DFS) otimizada com Programação Dinâmica (Cache) e operações binárias. Avalia subproblemas sobrepostos para garantir matematicamente o menor tempo de batalha absoluto na casa dos milissegundos.
- **`algoritmo_genetico.py`**: A Inteligência Artificial. Lê os dados de entrada, gera as populações de estratégias de luta, aplica _crossover_ e mutação, e salva o DNA da equipe com o menor custo de tempo no arquivo de saída.
- **`logica.py`**: O Motor de Simulação (Backend). Responsável por ler o mapa, traçar as rotas, aplicar os custos de terreno (Plano, Rochoso, Montanhoso) e calcular os danos/energia com base nas decisões da IA.
- **`interface_hud.py`**: A Interface Gráfica (Frontend). Utiliza a biblioteca Pygame para desenhar um Painel Tático (HUD) limpo e dinâmico, reproduzindo a simulação passo a passo na tela para avaliação.

### 🗂️ Arquivos de Dados

- **`coordernadasmapaco.csv`**: Matriz 42x42 representando o mapa do santuário, os tipos de terreno e as localizações exatas das 12 Casas e do Grande Mestre.
- **`input.json`**: Arquivo de configuração base. Contém os parâmetros de dificuldade (Poder Cósmico) das Casas de Ouro e a força individual de cada Cavaleiro de Bronze.
- **`output.json`**: Arquivo gerado de forma autônoma pelo `algoritmo_genetico.py`. Guarda a matriz vencedora (DNA) de quem lutará em cada casa.
- **`log_simulacao.txt`**: Relatório textual detalhado gerado automaticamente ao final da simulação visual, contendo o histórico de combates, tempo de caminhada, tempo de batalhas e energias finais.

---

## 🚀 Como Instalar e Executar

### Pré-requisitos

Certifique-se de ter o **Python 3** instalado em sua máquina e a biblioteca `pygame` para a renderização gráfica.

1. Abra o terminal na pasta raiz do projeto.
2. Instale as dependências executando:

```bash
   pip install pygame

```

### Iniciando a Simulação

Para rodar a simulação completa (Cálculo Genético + Visualização no Mapa), basta executar o orquestrador:

```bash
python main.py

```

**O que vai acontecer:**

1. O terminal exibirá um menu perguntando qual motor de IA utilizar para as batalhas (DFS ou Genético).
2. O motor selecionado calculará a melhor estratégia de combates e exportará a matriz vencedora (o DNA da equipe) para o arquivo output.json.
3. A interface em Pygame abrirá automaticamente, exibindo o mapa (esquerda) e o Painel Tático (direita).
4. O agente percorrerá o mapa em velocidade controlada. Ao atingir uma Casa do Zodíaco, a interface fará uma pausa dramática para a batalha, atualizando a energia gasta no painel.
5. Ao alcançar a Casa do Grande Mestre (quadrado verde), um log de desempenho será gerado localmente (`log_simulacao.txt`) e a simulação será concluída.

---

## 👥 Membros do Grupo

- Alisson Joaquim Lara Oliveira (Responsável pela Interface Gráfica)
- Enzo (Responsável pelo Algoritmo Genético)
- Marco Antonio Jobim Filho (Responsável pelo Algoritmo DFS com Memoization)
- Gabriel
