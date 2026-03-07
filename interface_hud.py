import pygame
import sys
from logica import SimuladorLogica  # Importa o Backend

# --- CONSTANTES VISUAIS (Frontend) ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CORES_TERRENO = {
    15: (202, 202, 202),  # Plano
    16: (178, 156, 156),  # Rochoso
    14: (105, 105, 105),  # Montanhoso
}
COR_CASAS = (218, 165, 32)
COR_INICIO = (255, 50, 50)
COR_FIM = (50, 255, 50)
TAMANHO_BLOCO = 15


class InterfaceTatica:
    def __init__(self, motor_logico):
        pygame.init()
        self.motor = motor_logico  # Referência ao simulador

        self.largura_mapa = len(self.motor.mapa[0]) * TAMANHO_BLOCO
        self.altura_mapa = len(self.motor.mapa) * TAMANHO_BLOCO
        self.largura_painel = 380

        self.tela = pygame.display.set_mode(
            (self.largura_mapa + self.largura_painel, max(self.altura_mapa, 600))
        )
        pygame.display.set_caption("A Travessia das 12 Casas - Visualizador")

        self.font_titulo = pygame.font.SysFont("arial", 22, bold=True)
        self.font_texto = pygame.font.SysFont("arial", 16, bold=True)
        self.font_log = pygame.font.SysFont("arial", 14)
        self.clock = pygame.time.Clock()

    def desenhar(self):
        self.tela.fill((10, 15, 25))

        # 1. Desenha o Mapa lendo as posições do motor lógico
        for y, linha in enumerate(self.motor.mapa):
            for x, val in enumerate(linha):
                cor = BRANCO
                if val == 0:
                    cor = COR_INICIO
                elif val == 13:
                    cor = COR_FIM
                elif val is not None and 1 <= val <= 12:
                    cor = COR_CASAS
                elif val in CORES_TERRENO:
                    cor = CORES_TERRENO[val]
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

        # Desenha Agente
        cx, cy = self.motor.pos_atual
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
        self.tela.blit(
            self.font_titulo.render("STATUS: EXECUÇÃO GENÉTICA", True, (218, 165, 32)),
            (x_base, y_offset),
        )

        y_offset += 40
        pct = min(self.motor.tempo_total / 720.0, 1.0)
        cor_tempo = (
            (0, 255, 0) if pct < 0.7 else ((255, 165, 0) if pct < 0.9 else (255, 0, 0))
        )

        txt_tempo = self.font_texto.render(
            f"TEMPO: {self.motor.tempo_total:.1f} / 720 min", True, BRANCO
        )
        self.tela.blit(txt_tempo, (x_base, y_offset))
        pygame.draw.rect(self.tela, (50, 50, 50), (x_base, y_offset + 25, 300, 15))
        pygame.draw.rect(
            self.tela, cor_tempo, (x_base, y_offset + 25, int(300 * pct), 15)
        )
        pygame.draw.rect(self.tela, BRANCO, (x_base, y_offset + 25, 300, 15), 1)

        y_offset += 60
        self.tela.blit(
            self.font_titulo.render("COSMO DOS CAVALEIROS", True, (218, 165, 32)),
            (x_base, y_offset),
        )

        y_offset += 35
        nomes = ["Seiya", "Shiryu", "Hyoga", "Shun", "Ikki"]
        for i, nome in enumerate(nomes):
            energia = self.motor.energias[i]
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
        self.tela.blit(
            self.font_titulo.render("LOG TÁTICO", True, (218, 165, 32)),
            (x_base, y_offset),
        )
        y_offset += 30

        for log in self.motor.log_batalhas[-8:]:
            self.tela.blit(self.font_log.render(log, True, BRANCO), (x_base, y_offset))
            y_offset += 20

        pygame.display.flip()


def iniciar_interface():
    # 1. Instancia a lógica (Backend)
    motor = SimuladorLogica("coordernadasmapaco.csv", "input.json", "output.json")

    # 2. Instancia a Interface visual passando a lógica (Frontend)
    interface = InterfaceTatica(motor)

    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        if not motor.simulacao_concluida:
            # O motor avança e devolve um alerta se rolou batalha
            status = motor.avancar_passo()

            if status["batalha"]:
                interface.desenhar()  # Atualiza os status caindo
                pygame.time.wait(1500)  # Pausa dramática da interface

        interface.desenhar()
        interface.clock.tick(30)

    pygame.quit()
