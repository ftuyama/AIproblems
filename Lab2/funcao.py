# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Algoritmo do Máximo de f(x)."""
import math
from random import randint
from random import uniform


def funcao(x, y):
    u"""Avalia a função f(x, y) em dado ponto."""
    termo1 = 4 * math.exp(-1 * (x**2 + y**2))
    termo2 = math.exp(-1 * ((x - 5)**2 + (y - 5)**2))
    termo3 = math.exp(-1 * ((x + 5)**2 + (y + 5)**2))
    termo4 = math.exp(-1 * ((x + 5)**2 + (y + 5)**2))
    return termo1 + termo2 + termo3 + termo4


def tempera_simulada():
    u"""Forjando a melhor espada - máximo da função."""
    temp = 1024.0
    x = 10
    y = 10
    while True:
        if temp < 1:
            return (x, y)

        xx = x + uniform(-0.5, 0.5)
        yy = y + uniform(-0.5, 0.5)
        delta = funcao(x, y) - funcao(xx, yy)
        if delta >= 0:
            x = xx
            y = yy
        else:
            if randint(0, 100) < 100 * math.exp(delta / temp):
                x = xx
                y = yy

        temp = temp / 2


# Rotina main()
print "*************************************"
print "*                                   *"
print "*     Problema do Máximo de f(x)    *"
print "*                                   *"
print "*************************************"

demo = False
if demo:
    print funcao(-1, -1)
    print funcao(-1, 1)
    print funcao(0, 0)
    print funcao(1, -1)
    print funcao(1, 1)

    print funcao(5, 0)
    print funcao(5, 5)

solution = tempera_simulada()
print solution
print funcao(solution[0], solution[1])
