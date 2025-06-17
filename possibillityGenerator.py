from math import factorial
from itertools import combinations

# def combinacao(n, k):
#     return factorial(n) // (factorial(k) * factorial(n - k)) 
# print(f'Número de combinações possíveis: {combinacao(25, 15), combinacao(25, 14), combinacao(25, 13), combinacao(25, 12), combinacao(25, 11)}')

numeros = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
with open("Combinacoes-15.txt", "w") as file:
# Exemplo de combinações usando itertools
    combinacoes = combinations(numeros, 15)
    file.write("Combinacoes de 15 numeros:\n")
    for comb in combinacoes:
        file.write(f"{comb}\n")

with open("Combinacoes-14.txt", "w") as file:
# Exemplo de combinações usando itertools
    combinacoes = combinations(numeros, 14)
    file.write("Combinacoes de 14 numeros:\n")
    for comb in combinacoes:
        file.write(f"{comb}\n")

with open("Combinacoes-13.txt", "w") as file:
# Exemplo de combinações usando itertools
    combinacoes = combinations(numeros, 13)
    file.write("Combinacoes de 13 numeros:\n")
    for comb in combinacoes:
        file.write(f"{comb}\n")

with open("Combinacoes-12.txt", "w") as file:
# Exemplo de combinações usando itertools
    combinacoes = combinations(numeros, 12)
    file.write("Combinacoes de 12 numeros:\n")
    for comb in combinacoes:
        file.write(f"{comb}\n")


with open("Combinacoes-11.txt", "w") as file:
# Exemplo de combinações usando itertools
    combinacoes = combinations(numeros, 11)
    file.write("Combinacoes de 11 numeros:\n")
    for comb in combinacoes:
        file.write(f"{comb}\n")