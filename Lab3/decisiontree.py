# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Árvore de decisão para avaliação."""
from graphics import *
import math

'''
    Estrutura de dados da árvore de decisão
'''


def print_tree(tree):
    u"""Imprime a árvore de decisões."""
    win = GraphWin('Decision Tree', 1200, 600)
    win.setBackground(color_rgb(188, 237, 145))
    title = Text(Point(500, 30), "Decision Tree")
    title.setSize(20)
    title.draw(win)
    print_node(win, tree, 1, 1)
    win.getMouse()
    win.close()


def print_node(win, node, width, depth):
    u"""Imprime os nós recursivamente."""
    cir = Circle(Point(50 * width, 100 * depth), 5)
    cir.setFill('red')
    cir.draw(win)

    if not (node.attribute is None):
        attr = Text(Point(50 * width, 100 * depth - 20), node.attribute[:5])
        attr.setSize(14)
        attr.draw(win)
        print node.attribute
    print "children:" + str(depth)
    for i, child in enumerate(node.children):
        if not (child.decision is None):
            dec = Text(Point(50 * (i + 1), 100 * depth + 50), child.decision)
            dec.setSize(12)
            dec.draw(win)
            print node.decision
        print_node(win, child, i + 1, depth + 1)
    if len(node.children) == 0:
        attr = Text(Point(50 * width, 100 * depth + 30), node.rate)
        attr.setSize(12)
        attr.draw(win)
        print "leaf"
        print node.rate


class Node(object):
    u"""Nó de decisão da árvore."""

    def __init__(self):
        u"""Inicializa Nó."""
        self.children = []
        self.attribute = self.decision = self.rate = None

    def father(self, children, attribute):
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
    # Se todas as avaliações são iguais
    elif all(rate[1] == ratings[0][1] for rate in ratings):
        return Node().leaf(ratings[0][1])
    # Se não há mais atributos
    elif len(attributes) == 0:
        return Node().leaf(major_value(ratings)[1])
    else:
        # Variável que minimiza entropia
        best = choose_attr(ratings, attributes)
        tree = Node().father([], best)
        m = major_value(ratings)[1]
        # Gera subárvores de decisão
        for value in attributes[best]:
            subratings = filter(lambda rate:
                                get_attribute(rate, best) == value, ratings)
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
    best = None
    min_entropy = sys.maxint
    for attribute in attributes:
        if entropy(ratings, attribute) < min_entropy:
            best = attribute
    return best


def get_attribute(rate, attr):
    u"""Retorna o valor de um dado atributo."""
    return {
        "Gender": users[rate[0]][0],
        "Age": users[rate[0]][1],
        "Occupation": users[rate[0]][2],
        "Genre": movies[rate[2]][1],
        "Movie": rate[2]
    }[attr]


def major_value(ratings):
    u"""Determina o valor da maioria."""
    rates = [0, 0, 0, 0, 0]
    for rate in ratings:
        rates[int(rate[1]) - 1] += 1
    return (rates, rates.index(max(rates)))


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
movie = "2"
attributes = {
    "Gender": ["M", "F"],
    "Age": ["1", "18", "25", "35", "45", "50", "56"],
    "Occupation": [str(i) for i in range(0, 21)],
    "Movie": [str(i) for i in range(1, len(movies))]
}

#     "Genre": [
#         "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime",
#         "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical",
#         "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
#     ]

# Navigate in the decision tree
me = {
    "Gender": "M",
    "Age": 18,
    "Occupation": 12,
    "Movie": movie,
    "Genre": movies[movie][1]
}

# print ratings.values()
decision_tree = gen_tree(ratings[movie], attributes, 3)
print_tree(decision_tree)
print navigate(decision_tree)

# Implementar ganho de informação
# Limite de ganho de informação para decisão
# Calcular média em vez de maioria quando acaba atributos
# Validação cruzada?

# Implementar escolha de atributos
# Visualizar árvore construída
# Pensar num jeito esperto de tratar a lista de gêneros
