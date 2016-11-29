# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Algoritmo das N-Rainhas."""
from random import randint
from copy import deepcopy
from graphics import *
import timeit


def print_board(board):
    u"""Desenha o grafo de rotas a partir do mapa lido."""
    win = GraphWin('N-Rainhas', 850, 650)
    win.setBackground(color_rgb(188, 237, 145))
    title = Text(Point(400, 30), "N-Rainhas")
    title.setSize(20)
    title.draw(win)

    # Desenha tabuleiro principal
    rect = Rectangle(
        Point(150 - 5, 100 - 5),
        Point(650 + 5, 600 + 5)
    )
    rect.setFill('brown')
    rect.draw(win)

    # Desenha as casas no tabuleiro
    square = 500 / N
    for i in range(N):
        for j in range(N):
            if (i + j) % 2 == 0:
                x = 150 + i * square
                y = 100 + j * square
                rect = Rectangle(
                    Point(x, y),
                    Point(x + square, y + square)
                )
                rect.setFill('gray')
                rect.draw(win)

        # Desenha as peças no tabuleiro
        x = 150 + i * square
        y = 100 + board[i] * square
        cir = Circle(
            Point(x + 0.5 * square, y + 0.5 * square), 160 / N
        )
        cir.setFill('blue')
        cir.draw(win)

    win.getMouse()
    win.close()


def restricoes(board):
    u"""Número de restrições violadas."""
    restricoes = 0
    for i in range(N):
        for j in range(i):
            if check(board, i, j):
                restricoes += 1
    return restricoes


def check(board, i, j):
    u"""Número de ataques no tabuleiro."""
    return (board[i] == board[j]) or \
        (abs(i - j) == abs(board[i] - board[j]))


'''################# <Implementação da Evolução Diferencial> ###############'''


def check_solution(generation):
    u"""Verifica se problema foi resolvido."""
    # Calcula restrições para indivíduos da geração
    restrs = [restricoes(ind) for ind in generation]

    solution = []
    for i, retr in enumerate(restrs):
        if retr == 0:
            solution.append(generation[i])
    return solution, restrs


def initial_population(population):
    u"""Gera uma população inicial para algoritmo."""
    return [[randint(0, (N - 1)) for i in range(N)] for j in range(population)]


def diff_evolution(population, max_steps):
    u"""Realiza evolução diferencial."""
    gen_restrs, generations = [], []
    last_restrs, last_generation = [], []
    generation = initial_population(population)
    generations.append(generation)

    for steps in range(max_steps):
        # Verifica a solução
        solution, restrs = check_solution(generation)
        gen_restrs.append(restrs)
        if len(solution) > 0:
            return solution[0], generations, gen_restrs, steps

        # Realiza pedigree com gerações anteriores
        if len(last_generation) > 0:
            generation = pedigree(
                last_generation, last_restrs,
                generation, restrs)

        # Roda novo ciclo de evolução diferencial
        new_generation = []
        probabilities = evaluate_fitness(generation, restrs)
        for i in range(population / 2):
            [ind1, ind2] = fitness(generation, probabilities)
            [ind1, ind2] = crossover(ind1, ind2)
            new_generation += [mutation(ind1), mutation(ind2)]

        last_restrs, last_generation = restrs, generation
        generations.append(new_generation)
        generation = new_generation

    return [], generations, gen_restrs, -1


'''####### Funções de Fitness #######'''


def pedigree(generation, restrs, next_generation, next_restrs):
    u"""Mantém indíviduos da geração anterior."""
    population = len(generation)
    total_restrs = sorted(restrs + next_restrs)
    median = total_restrs[len(total_restrs) / 2]

    selection = []
    for i, restr in enumerate(next_restrs):
        if restr <= median and len(selection) < population:
            selection.append(next_generation[i])

    for i, restr in enumerate(restrs):
        if restr <= median and len(selection) < population:
            selection.append(mutation(generation[i]))

    return selection


'''####### Funções de Fitness #######'''


def evaluate_fitness(generation, restrs):
    u"""Retorna probabilidades para geração."""
    total = sum([1.0 / restr for restr in restrs])

    def calc_prob(restr, total, generation):
        return 100.0 / (total * restr)

    # Calcula probabilidade de seleção de indivíduos
    probabilities = []
    for restr in restrs:
        probabilities.append(calc_prob(restr, total, generation))
    return probabilities


def select_fitness(probabilities):
    u"""Seleciona indíviduo conforme probabilidade."""
    acc = 0
    n = randint(0, 100)
    for i, prob in enumerate(probabilities):
        if n <= acc + prob:
            return i
        acc += prob
    return select_fitness(probabilities)


def fitness(generation, probabilities):
    u"""Seleciona indíviduos para crossover."""
    ind1 = select_fitness(probabilities)
    ind2 = select_fitness(probabilities)
    while ind1 == ind2:
        ind2 = select_fitness(probabilities)
    return [generation[ind1], generation[ind2]]

'''####### Funções de Crossover #######'''


def crossover(board1, board2):
    u"""Realiza o crossover de dois indivíduos."""
    n = randint(0, N)
    return [board1[0:n] + board2[n:N], board2[0:n] + board1[n:N]]

'''####### Funções de Mutação #######'''


def mutation(board):
    u"""Substitui aleatoriamente um valor de uma posição aleatória do vetor."""
    restr = restricoes(board)
    if restr < 5 and restr > 2:
        for steps in range(100):
            index = randint(0, (N - 1))
            new_board = deepcopy(board)
            new_board[index] = randint(0, (N - 1))
            if restricoes(new_board) < restr:
                return new_board
    else:
        index = randint(0, (N - 1))
        board[index] = randint(0, (N - 1))
    return board

'''################ <Implementação da Evolução Diferencial/> ###############'''


def log_performance(steps, solution, gen_restrs):
    u"""Imprime estatísticas do resultado."""
    if steps > 0:
        print "Resolvido em " + str(steps) + " passos"
        print(solution)
    else:
        print "Não foi resolvido"
    print("###########################################################")
    print("Máximo: " + str([max(gen_restr) for gen_restr in gen_restrs]))
    print("Média: " + str([sum(gen_restr) / len(gen_restr)
                           for gen_restr in gen_restrs]))
    print("Mínimo: " + str([min(gen_restr) for gen_restr in gen_restrs]))
    if steps > 0:
        print_board(solution)


def monte_carlo(population, steps, depth):
    u"""Roda algoritmo várias vezes."""
    total_steps = 0
    start = timeit.default_timer()

    for i in range(depth):
        (solution, generations, gen_restrs, max_steps) =\
            diff_evolution(population, steps)
        total_steps += max_steps

    stop = timeit.default_timer()
    print "Média de tempo: " + str(((stop - start) * 1.0) / depth)
    print "Média de passos: " + str((total_steps * 1.0) / depth)

# Rotina main()
print "*************************************"
print "*                                   *"
print "*       Problema das N-Rainhas      *"
print "*                                   *"
print "*************************************"
N = 10
demo = True
if demo:
    (solution, generations, gen_restrs, steps) = diff_evolution(40, 100)
    log_performance(steps, solution, gen_restrs)
else:
    monte_carlo(40, 100, 20)
