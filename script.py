import time
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

# === Funções auxiliares para manipulação bitwise ===
def tupla_para_bitmap(tupla):
    bitmap = 0
    for num in tupla:
        bitmap |= 1 << (num - 1)
    return bitmap

def bitmap_para_tupla(bitmap):
    return tuple(i + 1 for i in range(25) if (bitmap >> i) & 1)

# === Leitura dos arquivos com conversão para bitmap ===
def ler_combinacoes_arquivo_bitmap(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        linhas = f.readlines()
    combinacoes = [tupla_para_bitmap(eval(linha.strip())) for linha in linhas]
    return combinacoes

# === Filtragem estatística para eliminar sequências muito prováveis irrelevantes ===
def filtro_estatistico(combinacoes):
    filtradas = []
    for c in combinacoes:
        nums = bitmap_para_tupla(c)
        sequencial = all(nums[i] + 1 == nums[i + 1] for i in range(len(nums) - 1))
        if not sequencial:
            filtradas.append(c)
    return filtradas

# === Paralelização da construção do mapa de cobertura ===
def processar_bloco_mapa_cobertura(args):
    sub15_sublista, sub14_bitmaps = args
    mapa_parcial = dict()
    for s15 in sub15_sublista:
        cobertos = set()
        for s14 in sub14_bitmaps:
            if (s15 & s14) == s14:
                cobertos.add(s14)
        if cobertos:
            mapa_parcial[s15] = cobertos
    return mapa_parcial

def construir_mapa_cobertura_bitwise_paralelo(sub14_bitmaps, sub15_bitmaps, n_processos=None):
    if n_processos is None:
        n_processos = max(1, cpu_count() - 1)

    chunk_size = (len(sub15_bitmaps) + n_processos - 1) // n_processos
    blocos = [sub15_bitmaps[i*chunk_size:(i+1)*chunk_size] for i in range(n_processos)]

    args = [(bloco, sub14_bitmaps) for bloco in blocos]

    mapa_cobertura = dict()
    contagem_sub14 = {s14: 0 for s14 in sub14_bitmaps}

    print(f"Construindo mapa de cobertura com {n_processos} processos...")

    with Pool(processes=n_processos) as pool:
        resultados = list(tqdm(pool.imap(processar_bloco_mapa_cobertura, args), total=len(args)))

    for mapa_parcial in resultados:
        for s15, cobertos in mapa_parcial.items():
            mapa_cobertura[s15] = cobertos
            for s14 in cobertos:
                contagem_sub14[s14] += 1

    return mapa_cobertura, contagem_sub14

# === Algoritmo guloso modificado para cobertura parcial ===
def algoritmo_guloso_parcial(mapa_cobertura, contagem_sub14, sub14_bitmaps, cobertura_minima=0.95):
    total_sub14 = len(sub14_bitmaps)
    cobertos = set()
    solucao = []

    # Enquanto cobertura < mínima desejada
    while len(cobertos) / total_sub14 < cobertura_minima:
        melhor_cobertura = 0
        melhor_sub15 = None

        # Seleciona o conjunto de 15 que cobre mais subconjuntos ainda não cobertos
        for s15, cobertos_s15 in mapa_cobertura.items():
            novos_cobertos = cobertos_s15 - cobertos
            if len(novos_cobertos) > melhor_cobertura:
                melhor_cobertura = len(novos_cobertos)
                melhor_sub15 = s15

        if melhor_sub15 is None:
            print("Nenhum novo conjunto pode aumentar a cobertura.")
            break

        solucao.append(melhor_sub15)
        cobertos.update(mapa_cobertura[melhor_sub15])

        print(f"Cobertura atual: {len(cobertos)}/{total_sub14} ({len(cobertos)/total_sub14:.2%})")

        # Remove o conjunto selecionado para não reutilizar
        del mapa_cobertura[melhor_sub15]

    return solucao, cobertos

# === MAIN ===
if _name_ == "_main_":
    inicio_total = time.time()

    print("Carregando combinações...")
    sub14_bitmaps = ler_combinacoes_arquivo_bitmap("Combinacoes-14.txt")
    sub15_bitmaps = ler_combinacoes_arquivo_bitmap("Combinacoes-15.txt")

    print(f"Total combinações 14: {len(sub14_bitmaps)}")
    print(f"Total combinações 15: {len(sub15_bitmaps)}")

    print("Aplicando filtro estatístico para eliminar sequências...")
    sub14_bitmaps = filtro_estatistico(sub14_bitmaps)
    sub15_bitmaps = filtro_estatistico(sub15_bitmaps)
    print(f"Após filtro - combinações 14: {len(sub14_bitmaps)}")
    print(f"Após filtro - combinações 15: {len(sub15_bitmaps)}")

    mapa_cobertura, contagem_sub14 = construir_mapa_cobertura_bitwise_paralelo(sub14_bitmaps, sub15_bitmaps)

    print("Executando algoritmo guloso para obter cobertura parcial...")
    solucao, cobertos = algoritmo_guloso_parcial(mapa_cobertura, contagem_sub14, sub14_bitmaps, cobertura_minima=0.95)

    print("\n========== RESULTADO FINAL ==========")
    print(f"Conjuntos de 15 usados: {len(solucao)}")
    print(f"Subconjuntos de 14 cobertos: {len(cobertos)} de {len(sub14_bitmaps)} ({len(cobertos)/len(sub14_bitmaps):.2%})")

    fim_total = time.time()
    print(f"Tempo total de execução: {(fim_total - inicio_total)/60:.2f} minutos")