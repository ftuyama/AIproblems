# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Árvore de decisão para avaliação."""
import math

'''
    Estrutura de dados da árvore de decisão
'''


def print_node(node, depth):
    u"""Imprime os nós recursivamente."""
    if node.father is not None and node.father.attribute is not None:
        print "Node[" + node.father.attribute + "]",
        if node.decision is not None:
            print " dec:" + str(node.decision)
    else:
        print "<root>"

    if node.rate is not None:
        print "<leaf> rate:" + str(node.rate),

    if node.attribute is not None:
        print "attr:" + str(node.attribute),

    print "    gen:" + str(depth)

    if node.rate is not None and depth != 3:
        print "YAHOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"

    for i, child in enumerate(node.children):
        print '---------'
        print_node(child, depth + 1)


class Node(object):
    u"""Nó de decisão da árvore."""

    def __init__(self):
        u"""Inicializa Nó."""
        self.children = []
        self.attribute = self.decision = \
            self.rate = self.father = None

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

    def leaf(self, rate):
        u"""Propriedade de avaliação."""
        self.rate = rate
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
        return Node().leaf(default)
    # Se avaliações são similares ou não há mais atributos
    elif similar_rates(ratings) or len(attributes) == 0:
        return Node().leaf(major_value(ratings)[1])
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
    Auxiliares do principal
'''


def entropy(ratings, attribute):
    u"""Calcula a entropia usando dado atributo."""
    rates = major_value(ratings)[0]
    total = len(ratings)

    return sum(
        (-1.0 * p / total * math.log(1.0 * p / total))
        for p in rates if p != 0)


def choose_attr(ratings, attributes):
    u"""Escolhe atributo que minimiza entropia."""
    entropies = [entropy(ratings, attr) for attr in attributes]
    return attributes.keys()[entropies.index(max(entropies))]


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


def navigate(node):
    u"""Realiza indicação de avaliação."""
    if node.rate is None:
        for child in node.children:
            if child.decision == me[node.attribute]:
                return navigate(child)
    return node.rate

'''
    Chamada do programa
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
    # ]
    "Movie": [str(i) for i in range(1, len(movies))]
}

movie = "2"

# Navigate in the decision tree
me = {
    "Gender": "M",
    "Age": 18,
    "Occupation": 12,
    "Movie": movie,
    "Genre": movies[movie][1]
}

# Usar todas as avaliações
# print ratings.values()
decision_tree = gen_tree(ratings[movie], attributes, 3)
print_node(decision_tree, 0)

print navigate(decision_tree)

# Calcular média em vez de maioria quando acaba atributos
# Implementar ganho de informação
# Poda da árvore de decisão
# Validação cruzada?
