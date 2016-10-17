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
        map[movie].append((user, rate, movie))
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


def tree(ratings, attributes, default):
    u"""Gera a árvore de decisões."""
    # Se não há mais avaliações
    if len(ratings) == 0:
        return default
    # Se todas as avaliações são iguais
    elif all(rate[1] == ratings[0][1] for rate in ratings):
        return ratings[0][1]
    # Se não há mais atributos
    elif len(attributes) == 0:
        return major_value(ratings)
    else:
        # Variável que minimiza entropia
        best = choose_attr(ratings, attributes)
        tree = Node(best)
        m = major_value(ratings)
        best_values = []
        # Gera subárvores de decisão
        for value in best_values:
            subratings = filter(lambda rate:
                                get_attribute(rate, best) == value, ratings)
            subattributes = {key: v for key,
                             v in attributes.items() if key != best}
            subtree = tree(subratings, subattributes, m)
            tree.children.append((value, subtree))
    return tree


'''
    Auxiliares do principal
'''


def choose_attr(ratings, attributes):
    u"""Escolhe atributo que minimiza entropia."""
    return attributes.keys()[0]


def get_attribute(rate, attr):
    u"""Retorna o valor de um dado atributo."""
    return {
        "Gender": users[rate[0]][1],
        "Age": users[rate[0]][2],
        "Occuptaion": users[rate[0]][3],
        "Genre": movies[rate[2]][2],
    }[attr]


def major_value(ratings):
    u"""Determina o valor da maioria."""
    rates = [0, 0, 0, 0, 0]
    for rate in ratings:
        rates[int(rate[1])] += 1
    return rates.index(max(rates))


'''
    Chamada do programa
'''
'''
[ratings, users, movies] = [
    map_ratings(open("ml-1m/ratings.dat", "r").readlines()),
    map(open("ml-1m/users.dat", "r").readlines()),
    map(open("ml-1m/movies.dat", "r").readlines())
]
movie = "2"
attributes = {
    "Gender": ["M", "F"],
    "Age": [1, 18, 25, 35, 45, 50, 56],
    "Occupation": range(0, 21),
    "Genre": [
        "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime",
        "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical",
        "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
    ]
}
'''

# decision_tree = tree(ratings[movie], attributes, 3)

# Arrumar os atributos de forma inteligente
#  fácil de acessar index e valores assumíveis
# Pensei num Map de atributos, dando numa lista de valores possíveis
