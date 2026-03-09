import csv
import json
from src.IA.busca_estrela import a_estrela


class SimuladorLogica:
    def __init__(self, mapa_csv, input_json, output_json):
        self.mapa = []
        self.pos_inicio = None
        self.pos_fim = None
        self.casas_ordenadas = []

        # Carrega as informações
        self._carregar_mapa(mapa_csv)
        self.ouros, self.bronzes_poder, self.dna = self._carregar_dados(
            input_json, output_json
        )
        self.nomes_ouros = list(self.ouros.keys())
        self.nomes_bronzes = list(self.bronzes_poder.keys())

        # Gera o caminho predefinido (em L)
        pontos_obrigatorios = [self.pos_inicio] + self.casas_ordenadas + [self.pos_fim]
        self.caminho = self._gerar_caminho_simples(pontos_obrigatorios)

        # Variáveis de Estado
        self.tempo_total = 0.0
        self.tempo_caminho = 0.0
        self.tempo_batalhas = 0.0
        self.energias = [5, 5, 5, 5, 5]
        self.log_batalhas = []
        self.passo = 0
        self.casa_atual_idx = 0
        self.simulacao_concluida = False
        self.pos_atual = self.caminho[0] if self.caminho else (0, 0)

        self.custos_terreno = {15: 1, 16: 5, 14: 200}  # Plano, Rochoso, Montanhoso

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
                        if v == 0:
                            self.pos_inicio = (x, y)
                        elif v == 13:
                            self.pos_fim = (x, y)
                        elif 1 <= v <= 12:
                            pos_casas[v] = (x, y)
                self.mapa.append(linha_ints)
        self.casas_ordenadas = [pos_casas[i] for i in range(1, 13) if i in pos_casas]

    def _carregar_dados(self, input_json, output_json):
        with open(input_json, "r", encoding="utf-8") as f:
            entrada = json.load(f)
        with open(output_json, "r", encoding="utf-8") as f:
            saida = json.load(f)
        return entrada["config_ouros"], entrada["config_bronzes"], saida["dna_campeao"]

    def _gerar_caminho_simples(self, waypoints):

        caminho_total = []

        for i in range(len(waypoints) - 1):

            inicio = waypoints[i]
            destino = waypoints[i + 1]

            trecho = a_estrela(self.mapa, inicio, destino)

            if i > 0:
                trecho = trecho[1:]

            caminho_total.extend(trecho)

        return caminho_total

    def avancar_passo(self):
        """Avança 1 bloco. Retorna um dicionário avisando se houve batalha para a interface pausar."""
        if self.simulacao_concluida or self.passo >= len(self.caminho):
            if not self.simulacao_concluida:
                self.log_batalhas.append("--- CHEGOU AO GRANDE MESTRE ---")
                self.salvar_log()
                self.simulacao_concluida = True
            return {"batalha": False}

        self.pos_atual = self.caminho[self.passo]
        teve_batalha = False

        # Custo de Viagem
        val_terreno = self.mapa[self.pos_atual[1]][self.pos_atual[0]]
        custo = self.custos_terreno.get(val_terreno, 1)
        self.tempo_caminho += custo
        self.tempo_total += custo

        # Verifica Batalha
        if self.pos_atual in self.casas_ordenadas:
            idx = self.casas_ordenadas.index(self.pos_atual)
            if idx == self.casa_atual_idx:
                nome_casa = self.nomes_ouros[idx]
                poder_ouro = self.ouros[nome_casa]
                luta_dna = self.dna[idx]
                poder_bronze = 0
                equipe_nomes = []

                for i, lutou in enumerate(luta_dna):
                    if lutou == 1:
                        self.energias[i] -= 1
                        poder_bronze += self.bronzes_poder[self.nomes_bronzes[i]]
                        equipe_nomes.append(self.nomes_bronzes[i])

                tempo_batalha = poder_ouro / poder_bronze if poder_bronze > 0 else 999
                self.tempo_batalhas += tempo_batalha
                self.tempo_total += tempo_batalha
                self.log_batalhas.append(
                    f"Casa {idx+1} ({nome_casa}): {', '.join(equipe_nomes)} (+{tempo_batalha:.1f}m)"
                )

                self.casa_atual_idx += 1
                teve_batalha = True

        self.passo += 1
        return {"batalha": teve_batalha}

    def salvar_log(self):
        with open("data/log_simulacao.txt", "w", encoding="utf-8") as f:
            f.write("=== RELATÓRIO DA TRAVESSIA DAS 12 CASAS ===\n\n")
            f.write("LOG DE BATALHAS:\n")

            for linha in self.log_batalhas:
                f.write(linha + "\n")

            f.write("\n===========================================\n")
            f.write("RESUMO DE DESEMPENHO:\n")
            f.write(
                f"Tempo gasto em batalhas:...... {self.tempo_batalhas:.1f} minutos\n"
            )
            f.write(
                f"Tempo gasto no caminho:....... {self.tempo_caminho:.1f} minutos\n"
            )
            f.write(f"TEMPO TOTAL DA MISSÃO:........ {self.tempo_total:.1f} minutos\n")
            f.write("===========================================\n\n")
            f.write("ESTADO FINAL DOS CAVALEIROS:\n")
            f.write(f"Energias (Seiya, Shiryu, Hyoga, Shun, Ikki): {self.energias}\n")
        print("Arquivo 'log_simulacao.txt' gerado detalhadamente com sucesso!")
