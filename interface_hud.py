import pygame
import csv
import sys
import json
import os

# --- CONSTANTES VISUAIS E DE MAPA ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
TERRENOS_INFO = {
    15: {"cor": (202, 202, 202), "custo": 1},  # Plano
    16: {"cor": (178, 156, 156), "custo": 5},  # Rochoso
    14: {"cor": (105, 105, 105), "custo": 200},  # Montanhoso
}
COR_CASAS = (218, 165, 32)  # Dourado
COR_INICIO = (255, 50, 50)  # Vermelho
COR_FIM = (50, 255, 50)  # Verde
TAMANHO_BLOCO = 15


# --- LEITURA DOS ARQUIVOS DO ENZO ---
def carregar_dados():
    try:
        with open("input.json", "r", encoding="utf-8") as f:
            entrada = json.load(f)
        with open("output.json", "r", encoding="utf-8") as f:
            saida = json.load(f)
        return entrada["config_ouros"], entrada["config_bronzes"], saida["dna_campeao"]
    except Exception as e:
        print(f"Erro ao carregar os JSONs: {e}")
        sys.exit(1)


# --- GERAÇÃO DE CAMINHO PREDEFINIDO (SEM BUSCA) ---
def gerar_caminho_simples(waypoints):
    """
    Gera um caminho predefinido conectando os pontos em formato de 'L'
    (horizontal primeiro, depois vertical), ignorando regras de terreno.
    """
    caminho = []
    for i in range(len(waypoints) - 1):
        atual = waypoints[i]
        destino = waypoints[i + 1]
        x, y = atual
        cx, cy = destino

        # Move no eixo X
        step_x = 1 if cx > x else -1
        for nx in range(x, cx, step_x):
            caminho.append((nx, y))
        x = cx

        # Move no eixo Y
        step_y = 1 if cy > y else -1
        for ny in range(y, cy, step_y):
            caminho.append((x, ny))

    caminho.append(waypoints[-1])  # Adiciona o destino final
    return caminho


# --- FUNÇÃO PARA SALVAR LOG ---
def salvar_log_em_arquivo(log_batalhas, tempo_total, energias):
    try:
        with open("log_simulacao.txt", "w", encoding="utf-8") as f:
            f.write("=== RELATÓRIO DA TRAVESSIA DAS 12 CASAS ===\n\n")
            f.write("LOG DE BATALHAS:\n")
            for linha in log_batalhas:
                f.write(linha + "\n")
            f.write(f"\nTEMPO TOTAL FINAL: {tempo_total:.1f} minutos\n")
            f.write(f"ENERGIAS FINAIS (Seiya, Shiryu, Hyoga, Shun, Ikki): {energias}\n")
        print("Arquivo 'log_simulacao.txt' gerado com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar o log: {e}")


# --- CLASSE PRINCIPAL DA INTERFACE ---
class InterfaceTatitca:
    def __init__(self, mapa_csv):
        pygame.init()
        self.mapa = []
        self.pos_inicio = None
        self.pos_fim = None
        self._carregar_mapa(mapa_csv)

        self.largura_mapa = len(self.mapa[0]) * TAMANHO_BLOCO
        self.altura_mapa = len(self.mapa) * TAMANHO_BLOCO
        self.largura_painel = 380

        self.tela = pygame.display.set_mode(
            (self.largura_mapa + self.largura_painel, max(self.altura_mapa, 600))
        )
        pygame.display.set_caption("A Travessia das 12 Casas - IA Genética")

        self.font_titulo = pygame.font.SysFont("arial", 22, bold=True)
        self.font_texto = pygame.font.SysFont("arial", 16, bold=True)
        self.font_log = pygame.font.SysFont("arial", 14)
        self.clock = pygame.time.Clock()

    def _carregar_mapa(self, csv_file):
        pos_casas = {}
        with open(csv_file, "r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            for y, linha in enumerate(leitor):
                linha_ints = []
                for x, val in enumerate(linha):
                    val = val.strip()
                    if not val:
                        linha_ints.append(None)
                    else:
                        v = int(val)
                        linha_ints.append(v)
                        # CORREÇÃO DA LEITURA DO MAPA
                        if v == 0:
                            self.pos_inicio = (x, y)
                        elif v == 13:
                            self.pos_fim = (x, y)  # Objetivo (Verde)
                        elif 1 <= v <= 12:
                            pos_casas[v] = (x, y)  # Casas 1 a 12
                self.mapa.append(linha_ints)

        # Garante que as casas estão ordenadas da 1 à 12
        self.casas_ordenadas = [pos_casas[i] for i in range(1, 13) if i in pos_casas]

    def desenhar(self, pos_atual, tempo_total, energias, log_batalhas):
        self.tela.fill((10, 15, 25))

        # 1. Desenha o Mapa
        for y, linha in enumerate(self.mapa):
            for x, val in enumerate(linha):
                cor = BRANCO
                if val == 0:
                    cor = COR_INICIO
                elif val == 13:
                    cor = COR_FIM
                elif val is not None and 1 <= val <= 12:
                    cor = COR_CASAS
                elif val in TERRENOS_INFO:
                    cor = TERRENOS_INFO[val]["cor"]
                else:
                    cor = PRETO

                pygame.draw.rect(
                    self.tela,
                    cor,
                    (
                        x * TAMANHO_BLOCO,
                        y * TAMANHO_BLOCO,
                        TAMANHO_BLOCO,
                        TAMANHO_BLOCO,
                    ),
                )
                pygame.draw.rect(
                    self.tela,
                    PRETO,
                    (
                        x * TAMANHO_BLOCO,
                        y * TAMANHO_BLOCO,
                        TAMANHO_BLOCO,
                        TAMANHO_BLOCO,
                    ),
                    1,
                )

        # Desenha Agente (Bolinha Branca representando a equipe)
        cx, cy = pos_atual
        pygame.draw.circle(
            self.tela,
            (255, 255, 255),
            (cx * TAMANHO_BLOCO + 7, cy * TAMANHO_BLOCO + 7),
            6,
        )

        # 2. Desenha Painel HUD
        x_base = self.largura_mapa + 20
        pygame.draw.line(
            self.tela,
            (218, 165, 32),
            (self.largura_mapa, 0),
            (self.largura_mapa, 800),
            4,
        )

        y_offset = 20
        titulo = self.font_titulo.render(
            "STATUS: EXECUÇÃO GENÉTICA", True, (218, 165, 32)
        )
        self.tela.blit(titulo, (x_base, y_offset))

        y_offset += 40
        pct = min(tempo_total / 720.0, 1.0)
        cor_tempo = (
            (0, 255, 0) if pct < 0.7 else ((255, 165, 0) if pct < 0.9 else (255, 0, 0))
        )

        txt_tempo = self.font_texto.render(
            f"TEMPO: {tempo_total:.1f} / 720 min", True, BRANCO
        )
        self.tela.blit(txt_tempo, (x_base, y_offset))
        pygame.draw.rect(self.tela, (50, 50, 50), (x_base, y_offset + 25, 300, 15))
        pygame.draw.rect(
            self.tela, cor_tempo, (x_base, y_offset + 25, int(300 * pct), 15)
        )
        pygame.draw.rect(self.tela, BRANCO, (x_base, y_offset + 25, 300, 15), 1)

        y_offset += 60
        txt_energia = self.font_titulo.render(
            "COSMO DOS CAVALEIROS", True, (218, 165, 32)
        )
        self.tela.blit(txt_energia, (x_base, y_offset))

        y_offset += 35
        nomes = ["Seiya", "Shiryu", "Hyoga", "Shun", "Ikki"]
        for i, nome in enumerate(nomes):
            energia = energias[i]
            cor_txt = BRANCO if energia > 0 else (100, 100, 100)
            self.tela.blit(
                self.font_texto.render(f"{nome.upper()}", True, cor_txt),
                (x_base, y_offset),
            )
            for j in range(5):
                cor_bloco = (0, 191, 255) if j < energia else (40, 40, 40)
                pygame.draw.rect(
                    self.tela, cor_bloco, (x_base + 80 + (j * 30), y_offset + 2, 20, 12)
                )
            y_offset += 25

        y_offset += 20
        txt_log = self.font_titulo.render("LOG TÁTICO", True, (218, 165, 32))
        self.tela.blit(txt_log, (x_base, y_offset))
        y_offset += 30

        for log in log_batalhas[-8:]:
            self.tela.blit(self.font_log.render(log, True, BRANCO), (x_base, y_offset))
            y_offset += 20

        pygame.display.flip()


def main():
    # 1. Carrega dados do Enzo
    ouros, bronzes_poder, dna = carregar_dados()
    nomes_ouros = list(ouros.keys())
    nomes_bronzes = list(bronzes_poder.keys())

    # 2. Inicia Interface e Mapa
    interface = InterfaceTatitca("coordernadasmapaco.csv")

    # Monta a lista de pontos obrigatórios e gera o caminho predefinido (linhas retas)
    pontos_obrigatorios = (
        [interface.pos_inicio] + interface.casas_ordenadas + [interface.pos_fim]
    )
    caminho = gerar_caminho_simples(pontos_obrigatorios)

    # 3. Variáveis de Simulação
    tempo_total = 0.0
    energias = [5, 5, 5, 5, 5]
    log_batalhas = []

    casa_atual_idx = 0
    rodando = True
    passo = 0
    simulacao_concluida = False

    print("Iniciando reprodução tática no mapa com caminho predefinido...")

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        if passo < len(caminho):
            pos_atual = caminho[passo]

            # Custo de Viagem
            val_terreno = interface.mapa[pos_atual[1]][pos_atual[0]]
            custo = TERRENOS_INFO.get(val_terreno, {"custo": 1})["custo"]
            tempo_total += custo

            # Verifica Batalha
            if pos_atual in interface.casas_ordenadas:
                idx = interface.casas_ordenadas.index(pos_atual)
                if idx == casa_atual_idx:
                    nome_casa = nomes_ouros[idx]
                    poder_ouro = ouros[nome_casa]

                    # Lê a decisão genética do JSON
                    luta_dna = dna[idx]
                    poder_bronze = 0
                    equipe_nomes = []

                    for i, lutou in enumerate(luta_dna):
                        if lutou == 1:
                            energias[i] -= 1
                            poder_bronze += bronzes_poder[nomes_bronzes[i]]
                            equipe_nomes.append(nomes_bronzes[i])

                    tempo_batalha = (
                        poder_ouro / poder_bronze if poder_bronze > 0 else 999
                    )
                    tempo_total += tempo_batalha

                    log_batalhas.append(
                        f"Casa {idx+1} ({nome_casa}): {', '.join(equipe_nomes)} (+{tempo_batalha:.1f}m)"
                    )
                    casa_atual_idx += 1

                    # Pausa dramática na batalha
                    interface.desenhar(pos_atual, tempo_total, energias, log_batalhas)
                    pygame.time.wait(1500)

            interface.desenhar(pos_atual, tempo_total, energias, log_batalhas)
            interface.clock.tick(30)
            passo += 1

        elif not simulacao_concluida:
            # Acontece apenas uma vez quando chega ao final
            log_batalhas.append("--- CHEGOU AO GRANDE MESTRE ---")
            interface.desenhar(pos_atual, tempo_total, energias, log_batalhas)
            salvar_log_em_arquivo(log_batalhas, tempo_total, energias)
            simulacao_concluida = True

    pygame.quit()


if __name__ == "__main__":
    main()
