# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Algoritmo das N-Rainhas."""
from graphics import *
from random import randint
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


def max_violations(board):
    u"""Peça que viola mais restrições."""
    max_violations = 0
    max_violeted = []
    for i in range(N):
        restricoes = 0
        for j in range(N):
            if i != j and check(board, i, j):
                restricoes += 1
        if restricoes > max_violations:
            max_violations = restricoes
            max_violeted = [i]
        elif restricoes == max_violations:
            max_violeted.append(i)
    return (max_violeted, max_violations)


def hill_climbing(board, max_steps):
    u"""Maximiza função de requisito."""
    for i in range(max_steps):
        # Número atual de restrições
        (best, current) = (0, restricoes(board))
        if current == 0:
            return board, i

        # Peças com maior número de violações e seu número
        (violated, violations) = max_violations(board)

        # Evita condição de mínimo local
        if violations < 5 and randint(0, 100) > 50:
            board[randint(0, len(board) - 1)] = randint(0, len(board) - 1)

        # Escolhe uma peça para avaliar
        j = violated[randint(0, len(violated) - 1)]
        # Inspeciona para determinar melhor escolha
        for i in range(N):
            if not (i in board):
                board[j] = i
                inspection = restricoes(board)
                if inspection <= current:
                    (best, current) = (i, inspection)
        board[j] = best
    return board, max_steps


def monte_carlo(n_squares, depth):
    u"""Run algorithm several times."""
    total_steps = 0
    start = timeit.default_timer()

    for i in range(depth):
        board = [0] * n_squares
        total_steps += hill_climbing(board, 20000)[1]

    stop = timeit.default_timer()
    print "Avarage time: " + str(((stop - start) * 1.0) / depth)
    print "Avarage steps: " + str((total_steps * 1.0) / depth)

# Rotina main()
print "*************************************"
print "*                                   *"
print "*       Problema das N-Rainhas      *"
print "*                                   *"
print "*************************************"
N = 8
demo = True
if demo:
    board = [0] * N
    (solution, steps) = hill_climbing(board, 1000)
    print "Solved in " + str(steps) + " steps"
    print_board(solution)
else:
    monte_carlo(N, 10)
