from algoritmo_genetico import executar_genetico
from interface_hud import iniciar_interface

if __name__ == "__main__":
    print("=== INICIANDO O SISTEMA DA TRAVESSIA DAS 12 CASAS ===")

    # 1. Roda o Algoritmo Genético para decidir as melhores lutas (Gera o output.json)
    executar_genetico()

    # 2. Roda a interface gráfica para exibir a simulação com base nos resultados
    print("\nIniciando a Interface Gráfica Pygame...")
    iniciar_interface()

    print("=== SIMULAÇÃO CONCLUÍDA ===")
