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
        m = mean_value(ratings)
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
    Validação cruzada
'''


def cross_val(tree, ratings):
    u"""Realiza validação cruzada."""
    changed = True
    while changed:
        changed = False

        # for sub_leaf in sub_leafs:
        #     if better:
        #         tree = cross_val(new_tree, ratings)

    return tree


'''
    Navegação na árvore de decisão
'''


def navigate(node, person):
    u"""Realiza indicação de avaliação."""
    if node.rate is None:
        for child in node.children:
            if child.decision == person[node.attribute]:
                return navigate(child, person)
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
    return rates[major - 1] >= 0.8 * sum(rates)


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
    Realiza a avaliação de um dado filme
'''


def avaliate(movie, person):
    u"""Realiza avaliação de um dado filme."""
    # Árvore de decisão usando todas as avaliações
    # rates = [rate for subrates in ratings.values() for rate in subrates]

    # Árvore de decisão com avaliações do filme
    database = ratings[movie][1::2]  # Ímpares
    training = ratings[movie][0::2]  # Pares
    # Gerando a árvore de decisões
    decision_tree = gen_tree(database, attributes, 3)
    # Treinando a árvore de decisões
    decision_tree = cross_val(decision_tree, training)
    # Imprimindo a árvore de decisões
    # print_node(decision_tree, 0)
    # Navegando na árvore de decisões
    return navigate(decision_tree, person)


'''
    Análise dos dados recolhidos
'''


def analyse():
    u"""Analisa o classificador."""
    # Teste das minhas avaliações
    my_rates = {"1": 5, "73": 2, "260": 4, "1210": 5, "1274": 3,
                "1566": 5, "1721": 2, "1907": 4, "2571": 5, "3054": 3}

    # Parâmetros de comparação
    taxa_acerto = erro_quadratico = kappa = 0
    matriz_confusao = [[0 for x in range(5)]
                       for y in range(5)]

    for movie, my_rate in my_rates.iteritems():
        avaliation = avaliate(movie, me)
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

me = {
    "Gender": "M",
    "Age": "18",
    "Occupation": "17",
    # "Genre": movies[movie][1],
    # "Movie": movie
}


'''
    Demonstração do programa
'''

print "Our advice: " + str(avaliate("1", me))
analyse()

# Poda da árvore de decisão
# Validação cruzada?
