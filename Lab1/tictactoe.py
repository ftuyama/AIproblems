# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Clássico jogo da velha."""
from pprint import pprint
from graphics import *


def tic_tac_toe_o(win, p1x, p1y):
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


def tic_tac_toe_x(win, p1x, p1y):
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


def main():
    """Game Engine."""
    global win
    global boxsize
    global board

    # Mecânica do jogo
    turn = True
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

        print("Player 1: click a square.")
        p1mouse = win.getMouse()
        tic_tac_toe_x(win, p1mouse.getX() / boxsize, p1mouse.getY() / boxsize)
        turn = not turn
        pprint(board)

        print("Player 2: click a square.")
        p2mouse = win.getMouse()
        tic_tac_toe_o(win, p2mouse.getX() / boxsize, p2mouse.getY() / boxsize)
        turn = not turn
        pprint(board)

    if squares % 2 == 1:
        print("Player 1: click a square.")
        p1mouse = win.getMouse()
        tic_tac_toe_x(win, p1mouse.getX() / boxsize, p1mouse.getY() / boxsize)
        turn = not turn

# Rotina main()
print "*************************************"
print "*                                   *"
print "*            Jogo da Velha          *"
print "*                                   *"
print "*************************************"
main()
