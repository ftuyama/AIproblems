# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Árvore de decisão para avaliação."""
import math

'''
    Estrutura de dados da árvore de decisão
'''


def tab(n):
    u"""Imprime n tabs."""
    for i in range(0, n):
        print '\t',


def print_node(node, depth):
    u"""Imprime os nós recursivamente."""
    tab(depth)
    if node.rate is not None:
        print "<leaf>[" + node.father.attribute + "]",
        print "\tdec: " + str(node.decision),
        print "\trat: " + str(node.rate),
        print "\tquo: " + str(node.rates)
    elif node.father is not None:
        print "<node> [" + node.father.attribute + "]",
        print "\tdec: " + str(node.decision)
    else:
        print "<root>"

    for i, child in enumerate(node.children):
        print_node(child, depth + 1)


class Node(object):
    u"""Nó de decisão da árvore."""

    def __init__(self):
        u"""Inicializa Nó."""
        self.children = []
        self.attribute = self.decision = \
            self.rate = self.rates = self.father = None

    def parent(self, children, attribute):
        u"""Inicializa Nó."""
        self.attribute = attribute
        self.children = children
        return self

    def child(self, father, decision):
        u"""Propriedade de decisão."""
        self.father = father
        self.decision = decision
        return self

    def leaf(self, rate, rates):
        u"""Propriedade de avaliação."""
        self.rate = rate
        self.rates = rates
        return self

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


def gen_tree(ratings, attributes, default):
    u"""Gera a árvore de decisões."""
    # Se não há mais avaliações
    if len(ratings) == 0:
        return Node().leaf(default, len(ratings))
    # Se avaliações são similares
    elif similar_rates(ratings):
        return Node().leaf(major_value(ratings)[1], len(ratings))
    # Se não há mais atributos de decisão
    elif len(attributes) == 0:
        return Node().leaf(mean_value(ratings), len(ratings))
    else:
        # Variável que minimiza entropia
        best = choose_attr(ratings, attributes)
        tree = Node().parent([], best)
        m = major_value(ratings)[1]
        # Gera subárvores de decisão
        for value in attributes[best]:
            subratings = filter(lambda rate:
                                is_value(rate, best, value), ratings)
            subattributes = {key: v for key,
                             v in attributes.items() if key != best}
            subtree = gen_tree(subratings, subattributes, m).child(tree, value)
            tree.children.append(subtree)
    return tree


'''
    Navegação na árvore de decisão
'''


def navigate(node):
    u"""Realiza indicação de avaliação."""
    if node.rate is None:
        for child in node.children:
            if child.decision == me[node.attribute]:
                return navigate(child)
    return node.rate


'''
    Cálculo de entropia e Ganho de informação
'''


def entropy(ratings):
    u"""Calcula a entropia de um conjunto."""
    return sum(
        (-1.0 * p / len(ratings) * math.log(1.0 * p / len(ratings)))
        for p in major_value(ratings)[0] if p != 0)


def entropy_gain(initial_entropy, ratings, attr):
    u"""Calcula o ganho de entropia para um atributo."""
    gain = initial_entropy
    for value in attributes[attr]:
        subratings = filter(lambda rate:
                            is_value(rate, attr, value), ratings)
        gain -= len(subratings) * entropy(subratings) / len(ratings)
    return gain


def choose_attr(ratings, attributes):
    u"""Escolhe atributo que maximiza ganho de informação."""
    gain = [entropy_gain(entropy(ratings), ratings, attr)
            for attr in attributes]
    return attributes.keys()[gain.index(max(gain))]


'''
    Verificação de valor de atributo
'''


def is_value(rate, attr, value):
    u"""Retorna o valor de um dado atributo."""
    if attr == "Genre":
        return value in get_attribute_value(rate, attr)
    return value == get_attribute_value(rate, attr)


def get_attribute_value(rate, attr):
    u"""Retorna o valor de um dado atributo."""
    return {
        "Gender": users[rate[0]][0],
        "Age": users[rate[0]][1],
        "Occupation": users[rate[0]][2],
        "Genre": movies[rate[2]][1].split('|'),
        "Movie": rate[2]
    }[attr]


'''
    Cálculo da maioria e da média de avaliações
'''


def similar_rates(ratings):
    u"""Verifica se avaliações são similares."""
    (rates, major) = major_value(ratings)
    return rates[major - 1] >= 0.5 * sum(rates)


def major_value(ratings):
    u"""Determina o valor da maioria."""
    rates = [0, 0, 0, 0, 0]
    for rate in ratings:
        rates[int(rate[1]) - 1] += 1
    return (rates, rates.index(max(rates)) + 1)


def mean_value(ratings):
    u"""Determina o valor da média."""
    return int(round(sum([int(rate[1]) for rate in ratings]) / len(ratings)))


'''
    Leitura das variáveis do programa
'''

# Ratings:  {movie: [(user, rate, movie)]}
# Users:    {user:  [gender, age, occupation, zipcode]}
# Movies:   {movie: [title, genre]}
[ratings, users, movies] = [
    map_ratings(open("ml-1m/ratings.dat", "r").readlines()),
    map(open("ml-1m/users.dat", "r").readlines()),
    map(open("ml-1m/movies.dat", "r").readlines())
]
attributes = {
    "Gender": ["M", "F"],
    "Age": ["1", "18", "25", "35", "45", "50", "56"],
    "Occupation": [str(i) for i in range(0, 21)],
    # "Genre":
    # [
    #     "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime",
    #     "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical",
    #     "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
    # ],
    # "Movie": [str(i) for i in range(1, len(movies))]
}

'''
    Gerando árvore de decisão
'''

# database = [rate for subratings in ratings.values() for rate in subratings]

movie = "1"
database = ratings[movie]
decision_tree = gen_tree(database, attributes, 3)
print_node(decision_tree, 0)


'''
    Navegando na árvore de decisão
'''

me = {
    "Gender": "M",
    "Age": "18",
    "Occupation": "12",
    # "Genre": movies[movie][1],
    # "Movie": movie
}

print "Based on: " + str(len(database)) + " ratings"
print "Our advice: " + str(navigate(decision_tree))

# Poda da árvore de decisão
# Validação cruzada?
# Fazer só subárvore para agilizar
