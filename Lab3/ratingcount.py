# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Classificador a priori de avaliação."""


def map(lines):
    u"""Contabiliza avaliações."""
    map = {}
    # Map
    for line in lines:
        (_, movie, rank, _) = line.split("::")
        if not (movie in map):
            map[movie] = [0, 0, 0, 0, 0, 0]
        map[movie][int(rank)] += 1

    # Reduce
    for movie in map:
        total = sum(map[movie])
        for i in range(1, 6):
            map[movie][0] += i * map[movie][i]
        map[movie][0] = map[movie][0] / total

    return map


def analyse():
    u"""Analisa o classificador."""
    # # Teste das minhas avaliações
    # my_rates = {"1": 5, "73": 2, "260": 4, "1210": 5, "1274": 3,
    #             "1566": 5, "1721": 2, "1907": 4, "2571": 5, "3054": 3}
    my_rates = {"2134": 3, "1265": 4, "1196": 5, "590": 4, "736": 1,
                "592": 5, "593": 4, "2088": 3, "3040": 5, "2243": 3}

    # Parâmetros de comparação
    taxa_acerto = erro_quadratico = kappa = 0
    matriz_confusao = [[0 for x in range(5)]
                       for y in range(5)]

    for movie, my_rate in my_rates.iteritems():
        avaliation = advice[movie][0]
        # Taxa de acerto
        taxa_acerto += 1 if (avaliation == my_rate) else 0
        # Matriz confusão
        matriz_confusao[my_rate - 1][avaliation - 1] += 1
        # Erro quadrático médio
        erro_quadratico += (my_rate - avaliation)**2

    taxa_acerto = 1.0 * taxa_acerto / len(my_rates)
    esperado = 0.25
    erro_quadratico = 1.0 * erro_quadratico / len(my_rates)
    kappa = (taxa_acerto - esperado) / (1 - esperado)

    # Imprimindo resultados
    print("Taxa de acerto   : %.2f" % taxa_acerto)
    print("Matriz confusão  : " + str(matriz_confusao))
    print("Erro quadrático  : %.2f" % erro_quadratico)
    print("Índice Kappa     : %.2f" % kappa)

advice = map(open("ml-1m/ratings.dat", "r").readlines())
movie = "2"
print advice[movie]
analyse()
