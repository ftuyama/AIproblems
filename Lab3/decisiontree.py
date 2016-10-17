# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Árvore de decisão para avaliação."""


class Node(object):
    u"""Nó de decisão da árvore."""

    def __init__(self, attribute):
        u"""Inicializa Nó."""
        self.attribute = attribute
        self.children = []

'''
    Auxiliares para leitura dos dados
'''


def map_ratings(lines):
    u"""Contabiliza avaliações."""
    map = {}
    for line in lines:
        (user, movie, rate, _) = line.split("::")
        if not (movie in map):
            map[movie] = []
        map[movie].append((user, rate))
    return map


def map(lines):
    u"""Contabiliza usuários/filmes."""
    map = {}
    for line in lines:
        obj = line.rstrip().split("::")
        map[obj[0]] = obj[1:]
    return map

'''
    Método principal do programa
'''


def tree(map, attributes, default):
    u"""Gera a árvore de decisões."""
    if len(map) == 0:
        return default
    elif same_rates(map):
        return map.itervalues().next()[1]
    elif len(attributes) == 0:
        return major_value(map)
    else:
        best = choose_attr(map, attributes)
        tree = Node(best)
        m = major_value(map)
        best_values = []
        for value in best_values:
            submap = filter(map, best, value)
            subattributes = sub_attr(attributes, best)
            subtree = tree(submap, subattributes, m)
            tree.children.append((value, subtree))
    return tree


'''
    Auxiliares do principal
'''


def choose_attr(map, attributes):
    u"""Escolhe atributo que minimiza entropia."""
    return attributes[0]


def sub_attr(attributes, attribute):
    u"""Lista de atributos sem atributo."""
    attributes.remove(attribute)
    return attributes


def filter(map, attribute, value):
    u"""Filtra o mapa, com atributo valor."""
    filtered = {}
    for rate in map:
        # Arrumar os atributos de forma inteligente
        #  fácil de acessar index e valores assumíveis
        if users[rate[0]][attribute] == value:
            filtered.append(rate)
    return filtered


def major_value(map):
    u"""Determina o valor da maioria."""
    rates = [0, 0, 0, 0, 0]
    for rate in map:
        rates[int(rate[1])] += 1
    return rates.index(max(rates))


def same_rates(map):
    u"""Verifica se todas avaliações são iguais."""
    same = map.itervalues().next()[1]
    for rate in map:
        if rate[1] != same:
            return False
    return True

'''
    Chamada do programa
'''

[ratings, users, movies] = [
    map_ratings(open("ml-1m/ratings.dat", "r").readlines()),
    map(open("ml-1m/users.dat", "r").readlines()),
    map(open("ml-1m/movies.dat", "r").readlines())
]
movie = "2"
# attributes = []
# decision_tree = tree(ratings[movie], attributes, 3)

# Arrumar os atributos de forma inteligente
#  fácil de acessar index e valores assumíveis
# Pensei num Map de atributos, dando numa lista de valores possíveis
