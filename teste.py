import itertools
import time
from math import comb # Função para calcular combinações C(n, k)

def encontrar_cobertura(numeros_totais, tamanho_aposta, tamanho_premio):
    """
    Encontra um conjunto de cobertura usando uma heurística gulosa otimizada.

    Args:
        numeros_totais (int): O total de números para escolher (ex: 25).
        tamanho_aposta (int): O número de itens em cada aposta (ex: 15).
        tamanho_premio (int): O número de itens a serem cobertos (ex: 14, 13, ...).

    Returns:
        list: Uma lista de tuplas, representando o conjunto de cobertura encontrado.
    """

    universo = set(range(1, numeros_totais + 1))

    # 1. Gerar todas as combinações de prêmio a serem cobertas.
    # Usamos um 'set' para remoções eficientes.
    print(f"Gerando {comb(numeros_totais, tamanho_premio):,} combinações de {tamanho_premio} números...")
    combinacoes_a_cobrir = set(itertools.combinations(universo, tamanho_premio))

    conjunto_solucao = []

    start_time = time.time()

    # 2. Loop principal: continue até que todas as combinações de prêmio tenham sido cobertas.
    while combinacoes_a_cobrir:

        # 3. Escolha uma combinação de prêmio ainda não coberta para ser nosso "alvo".
        # O método .pop() remove e retorna um elemento arbitrário do set.
        # Essa arbitrariedade adiciona um elemento randômico útil à heurística.
        alvo = next(iter(combinacoes_a_cobrir))

        # 4. Gere um conjunto de "candidatas".
        # Estas são as apostas de 15 números que garantidamente cobrem o nosso "alvo".
        # O número de candidatas é (numeros_totais - tamanho_premio). Ex: 25 - 14 = 11.
        melhor_candidata = None
        max_cobertas = 0

        numeros_restantes = universo.difference(set(alvo))
        candidatas = [tuple(sorted(alvo + (n,))) for n in numeros_restantes]

        # 5. Avalie qual das candidatas é a "melhor".
        # A melhor é aquela que cobre o maior número de combinações ainda não cobertas.
        for candidata in candidatas:
            # Encontre todas as combinações de prêmio que esta candidata cobre.
            # C(15, 14) = 15. Então cada candidata cobre 15 combinações de 14 números.
            cobertas_pela_candidata = set(itertools.combinations(candidata, tamanho_premio))

            # Verifique a interseção com as que ainda precisamos cobrir.
            novas_cobertas = combinacoes_a_cobrir.intersection(cobertas_pela_candidata)

            if len(novas_cobertas) > max_cobertas:
                max_cobertas = len(novas_cobertas)
                melhor_candidata = candidata

        # 6. Adicione a melhor candidata à solução e remova as combinações que ela cobre.
        if melhor_candidata:
            conjunto_solucao.append(melhor_candidata)

            cobertas_pela_melhor = set(itertools.combinations(melhor_candidata, tamanho_premio))
            combinacoes_a_cobrir.difference_update(cobertas_pela_melhor)

        # Log de progresso
        num_restantes = len(combinacoes_a_cobrir)
        print(f"Apostas na solução: {len(conjunto_solucao)}. Combinações restantes a cobrir: {num_restantes:,}")

    end_time = time.time()
    print(f"\nCobertura encontrada em {end_time - start_time:.2f} segundos.")
    return conjunto_solucao

# --- Execução para o PROGRAMA 2 (SB15_14) ---
N_TOTAL = 25
K_APOSTA = 15
T_PREMIO = 14


# Altere este valor para 13, 12 ou 11 para os outros programas.

# Executa a função
sb15_14 = encontrar_cobertura(N_TOTAL, K_APOSTA, T_PREMIO)

# Imprime o resultado final
print(f"\n--- Resultado para t={T_PREMIO} ---")
print(f"Tamanho do subconjunto encontrado: {len(sb15_14)}")
# print("Subconjunto:")
# for aposta in sb15_14:
#     print(aposta)

# Calcula o custo financeiro
custo_por_aposta = 3.00
custo_total = len(sb15_14) * custo_por_aposta
print(f"Custo financeiro: {len(sb15_14)} apostas x R$ {custo_por_aposta:.2f} = R$ {custo_total:.2f}")