# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Clássico jogo da velha."""
from pprint import pprint
from graphics import *
import copy
import sys


def create_board():
    u"""Cria o tabuleiro de jogo."""
    global win
    global boxsize
    global squares

    windowsize = 600
    squares = 3
    boxsize = windowsize / squares

    # Desenhando tabuleiro
    win = GraphWin("Tic Tac Toe", windowsize, windowsize)
    for i in range(squares - 1):
        position = (boxsize) * (i + 1)
        Line(Point(0, position), Point(windowsize, position)).draw(win)
        Line(Point(position, 0), Point(position, windowsize)).draw(win)


def tic_tac_toe_victory(player):
    u"""Exibe mensagem de vitória na tela."""
    victory = Text(Point(300, 300), "Hi")
    if player is '-':
        victory.setText("Deu velha!")
        print("Deu velha!")
    else:
        victory.setText("Player " + player + " venceu!")
        print("Player " + player + " venceu!")

    victory.setSize(36)
    victory.draw(win)

    win.getMouse()
    win.close()


def tic_tac_toe_o(p1x, p1y):
    """Draw tic_tac_toe_o.

    Circle the winner's photo.
    Parameters:
    - win: the window
    - winner_center: the center of the winner's picture (as a Point).
    """
    board[p1y][p1x] = 'o'
    circle = Circle(
        Point((p1x + 0.5) * boxsize, (p1y + 0.5) * boxsize),
        boxsize / 2
    )
    circle.setOutline('red')
    circle.setWidth(5)
    circle.draw(win)


def tic_tac_toe_x(p1x, p1y):
    """Draw tic_tac_toe_x.

    Cross out the loser's photo
    Parameters:
    - win: the window
    - loser_center: the center of the loser's picture (as a Point).
    """
    board[p1y][p1x] = 'x'
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
        if board[squares - i - 1][i] == player:
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


def heuristics(board, player):
    u"""Heurística para tomar decisão."""
    board = copy.deepcopy(board)
    # Verifica todas possibilidades de vitória
    col = row = diag = rdiag = 0
    for i in range(0, squares):
        if board[squares - i - 1][i] != player:
            rdiag += 1
        if board[x][i] != player:
            col += 1
        if board[i][y] != player:
            row += 1
        if board[i][i] != player:
            diag += 1

    heur = 0
    if col == squares:
        heur += 1
    if row == squares:
        heur += 1
    if diag == squares:
        heur += 1
    if rdiag == squares:
        heur += 1
    return heur


def minimax_x(board, x, y):
    u"""Minimax para jogada de x."""
    results = []
    moves = []
    board = copy.deepcopy(board)
    board[x][y] = 'o'
    # Verifica profundidade máxima
    if heuristic:
        if n_plays(board) - depth >= max_depth:
            return (heuristics(board, 'o'), None)
    # Varre tabuleiro procurando jogadas
    for i in range(0, squares):
        for j in range(0, squares):
            if board[i][j] == '':
                point = points(board, i, j, 'x')
                if point == 0:
                    # Continua buscando nós
                    value = minimax_x(board, i, j)[0]
                    # Beta não pode diminuir
                    if heuristic and value < poda[n_plays(board)]:
                        # Poda da árvore de busca
                        return (0, None)
                    else:
                        results.append(minimax_o(board, i, j)[0])
                else:
                    # Nó. Ponto. Voltar
                    results.append(-1)
                moves.append((i, j))

    # Caso não haja mais jogadas
    if len(results) == 0:
        return (0, None)
    # Calcula a jogada com menor pontuação (Min)
    min_id = results.index(min(results))
    poda[n_plays(board)] = min(poda[n_plays(board)], results[min_id])
    return (results[min_id], moves[min_id])


def minimax_o(board, x, y):
    u"""Minimax para jogada de o."""
    results = []
    moves = []
    board = copy.deepcopy(board)
    board[x][y] = 'x'
    # Verifica profundidade máxima
    if heuristic:
        if n_plays(board) - depth >= max_depth:
            return (heuristics(board, 'x'), None)
    # Varre tabuleiro procurando jogadas
    for i in range(0, squares):
        for j in range(0, squares):
            if board[i][j] == '':
                point = points(board, i, j, 'o')
                if point == 0:
                    # Continua buscando nós
                    value = minimax_x(board, i, j)[0]
                    # Alpha não pode aumentar
                    if heuristic and value > poda[n_plays(board)]:
                        # Poda da árvore de busca
                        return (0, None)
                    else:
                        results.append(value)
                else:
                    # Nó. Ponto. Voltar
                    results.append(1)
                moves.append((i, j))

    # Caso não haja mais jogadas
    if len(results) == 0:
        return (0, None)
    # Calcula a jogada com maior pontuação (Max)
    max_id = results.index(max(results))
    poda[n_plays(board)] = max(poda[n_plays(board)], results[max_id])
    return (results[max_id], moves[max_id])


def minimax(board, x, y, player):
    u"""O jogador jogou na posição (x, y)."""
    global depth, max_depth, heuristic, poda
    # Características da AI
    depth = n_plays(board)  # Profundidade começa na jogada atual
    max_depth = 4           # Máxima profundidade de análise
    poda = []               # Ramo da árvore analisado
    heuristic = True        # Uso de heurística ou não
    # Realizando análise
    for i in range(squares ** 2):
        poda.append((-1)**(i % 2 + 1) * sys.maxint)
    if player == 'x':
        print("Turno - Player o")
        (result, move) = minimax_o(board, x, y)
    else:
        print("Turno - Player x")
        (result, move) = minimax_x(board, x, y)
    return (move[0], move[1])


def n_plays(board):
    u"""Número de jogadas feitas em board."""
    n_plays = 0
    for i in range(0, squares):
        for j in range(0, squares):
            if board[i][j] != '':
                n_plays += 1
    return n_plays


def input(player):
    u"""Captura jogada válida."""
    print("Turno - Player " + player)
    valido = False
    # Captura jogada válida
    while not valido:
        mouse = win.getMouse()
        x = mouse.getX() / boxsize
        y = mouse.getY() / boxsize
        if board[y][x] == '':
            valido = True
    return (x, y)


def play_tic_tac_toe(board):
    u"""Faz a jogada de player."""
    global x, y, player
    # Jogada de X (com input)
    if player == 'x':
        (x, y) = input('x')
        tic_tac_toe_x(x, y)
    # Jogada de O (com AI)
    if player == 'o':
        (y, x) = minimax(board, y, x, 'x')
        tic_tac_toe_o(x, y)

    # Verifica condição de vitória
    pprint(board)
    if points(board, y, x, player) == 1:
        tic_tac_toe_victory(player)
    else:
        player = 'x' if player == 'o' else 'o'


def main():
    """Game Engine."""
    global board, player
    board = [
        ['', '', ''],
        ['', '', ''],
        ['', '', '']
    ]
    player = 'x'

    create_board()

    # Loop principal de jogo
    for i in range(squares ** 2):
        play_tic_tac_toe(board)

    tic_tac_toe_victory('-')


# Rotina main()
print "*************************************"
print "*                                   *"
print "*            Jogo da Velha          *"
print "*                                   *"
print "*************************************"
main()
