# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Clássico jogo da velha."""
from pprint import pprint
from graphics import *
import copy


def tic_tac_toe_o(win, p1x, p1y):
    """Draw tic_tac_toe_o.

    Circle the winner's photo.
    Parameters:
    - win: the window
    - winner_center: the center of the winner's picture (as a Point).
    """
    board[p1y][p1x] = 'o'
    pprint(board)
    circle = Circle(
        Point((p1x + 0.5) * boxsize, (p1y + 0.5) * boxsize),
        boxsize / 2
    )
    circle.setOutline('red')
    circle.setWidth(5)
    circle.draw(win)


def tic_tac_toe_x(win, p1x, p1y):
    """Draw tic_tac_toe_x.

    Cross out the loser's photo
    Parameters:
    - win: the window
    - loser_center: the center of the loser's picture (as a Point).
    """
    board[p1y][p1x] = 'x'
    pprint(board)
    for i in range(1, 3):
        pos_x = p1x * boxsize
        pos_y = p1y * boxsize
        line = Line(
            Point(pos_x, pos_y + (i / 2) * boxsize),
            Point(pos_x + boxsize, pos_y + (i % 2) * boxsize)
        )
        line.setFill('blue')
        line.setWidth(5)
        line.draw(win)


def points(board, x, y, player):
    u"""Verifica se jogada é vitoriosa."""
    board = copy.deepcopy(board)
    board[x][y] = player
    col = row = diag = rdiag = 0
    for i in range(0, squares):
        if board[2 - i][i] == player:
            rdiag += 1
        if board[x][i] == player:
            col += 1
        if board[i][y] == player:
            row += 1
        if board[i][i] == player:
            diag += 1

    if col == squares or row == squares or \
            diag == squares or rdiag == squares:
        return 1
    return 0


def minimax_x(board, x, y):
    results = []
    moves = []
    board = copy.deepcopy(board)
    board[x][y] = 'o'
    for i in range(0, squares):
        for j in range(0, squares):
            if board[i][j] == '':
                point = points(board, i, j, 'x')
                if point == 0:
                    # Continua buscando nós
                    results.append(minimax_o(board, i, j)[0])
                else:
                    # Nó. Ponto. Voltar
                    results.append(-1)
                moves.append((i, j))

    if len(results) == 0:
        return (0, None)
    min_id = results.index(min(results))
    return (results[min_id], moves[min_id])


def minimax_o(board, x, y):
    results = []
    moves = []
    board = copy.deepcopy(board)
    board[x][y] = 'x'
    for i in range(0, squares):
        for j in range(0, squares):
            if board[i][j] == '':
                point = points(board, i, j, 'o')
                if point == 0:
                    # Continua buscando nós
                    results.append(minimax_x(board, i, j)[0])
                else:
                    # Nó. Ponto. Voltar
                    results.append(1)
                moves.append((i, j))

    if len(results) == 0:
        return (0, None)
    max_id = results.index(max(results))
    return (results[max_id], moves[max_id])


def minimax(board, x, y, player):
    u"""O jogador jogou na posição (x, y)."""
    if player == 'x':
        print("Turno - Player o")
        (result, move) = minimax_o(board, x, y)
    else:
        print("Turno - Player x")
        (result, move) = minimax_x(board, x, y)
    return (move[0], move[1])


def input(player):
    u"""Captura jogada válida."""
    print("Turno - Player " + player)
    valido = False
    while not valido:
        mouse = win.getMouse()
        x = mouse.getX() / boxsize
        y = mouse.getY() / boxsize
        if board[y][x] == '':
            valido = True
    return (x, y)


def main():
    """Game Engine."""
    global win
    global boxsize
    global board
    global squares

    # Mecânica do jogo
    board = [
        ['', '', ''],
        ['', '', ''],
        ['', '', '']
    ]

    # Configurações de jogo
    windowsize = 600
    squares = 3
    boxsize = windowsize / squares

    # Desenhando tabuleiro
    win = GraphWin("Tic Tac Toe", windowsize, windowsize)
    for i in range(squares - 1):
        position = (boxsize) * (i + 1)
        Line(Point(0, position), Point(windowsize, position)).draw(win)
        Line(Point(position, 0), Point(position, windowsize)).draw(win)

    # Jogadas do jogo
    for i in range((squares ** 2) // 2):

        (x, y) = input('x')
        tic_tac_toe_x(win, x, y)
        if points(board, y, x, 'x') == 1:
            print("Player 1 venceu!")
            return

        # (x, y) = input('o')
        (y, x) = minimax(board, y, x, 'x')
        tic_tac_toe_o(win, x, y)
        if points(board, y, x, 'o') == 1:
            print("Player 2 venceu!")
            return

    (x, y) = input('x')
    tic_tac_toe_x(win, x, y)
    if points(board, y, x, 'x') == 1:
        print("Player 1 won!")
        return

    print("Deu velha!")


# Rotina main()
print "*************************************"
print "*                                   *"
print "*            Jogo da Velha          *"
print "*                                   *"
print "*************************************"
main()
