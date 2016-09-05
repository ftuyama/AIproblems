# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Algoritmo das N-Rainhas."""
from graphics import *


def print_board():
    u"""Desenha o grafo de rotas a partir do mapa lido."""
    win = GraphWin('N-Rainhas', 850, 650)
    win.setBackground(color_rgb(188, 237, 145))
    title = Text(Point(400, 30), "N-Rainhas")
    title.setSize(20)
    title.draw(win)

    rect = Rectangle(
        Point(150 - 5, 100 - 5),
        Point(650 + 5, 600 + 5)
    )
    rect.setFill('brown')
    rect.draw(win)

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
                if board[i][j] == 1:
                    cir = Circle(
                        Point(x + 0.5 * square, y + 0.5 * square), 20
                    )
                    cir.setFill('blue')
                    cir.draw(win)

    win.getMouse()
    win.close()


# Rotina main()
print "*************************************"
print "*                                   *"
print "*       Problema das N-Rainhas      *"
print "*                                   *"
print "*************************************"
N = 8
board = [[0] * N for i in range(N)]
for i in range(N):
    board[i][i] = 1
print_board()
