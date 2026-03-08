import sys
from algoritmo_genetico import executar_genetico
from interface_hud import iniciar_interface
from dfs_memoization import executar_dfs

if __name__ == "__main__":
    print("=== INICIANDO O SISTEMA DA TRAVESSIA DAS 12 CASAS ===")

    print("\nSelecione o motor de Inteligência Artificial para as batalhas:")
    print("[1] Algoritmo Genético (Heurística)")
    print("[2] DFS + Memoization (Busca Exaustiva Ótima)")

    escolha = input("\nDigite a sua escolha: ").strip()

    if escolha == "1":
        print("\n>>> INICIANDO MOTOR: ALGORITMO GENÉTICO <<<")
        executar_genetico()
    elif escolha == "2":
        print("\n>>> INICIANDO MOTOR: DFS + MEMOIZATION <<<")
        executar_dfs()
    else:
        print("\nEscolha inválida. O sistema será encerrado.")
        sys.exit(1)

    # 2. Roda a interface gráfica para exibir a simulação com base nos resultados
    print("\nIniciando a Interface Gráfica Pygame...")
    iniciar_interface()

    print("=== SIMULAÇÃO CONCLUÍDA ===")
