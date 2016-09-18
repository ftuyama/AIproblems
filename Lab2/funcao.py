# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Algoritmo do Máximo de f(x)."""
import math
from random import randint, uniform


def funcao(x, y):
    u"""Avalia a função f(x, y) em dado ponto."""
    termo1 = 4 * math.exp(-1 * (x**2 + y**2))
    termo2 = math.exp(-1 * ((x - 5)**2 + (y - 5)**2))
    termo3 = math.exp(-1 * ((x + 5)**2 + (y + 5)**2))
    termo4 = math.exp(-1 * ((x + 5)**2 + (y - 5)**2))
    termo5 = math.exp(-1 * ((x - 5)**2 + (y + 5)**2))
    return termo1 + termo2 + termo3 + termo4 + termo5


def tempera_simulada(x, y, temp, step):
    u"""Essa função tem quatro argumentos."""
    u"""(x, y) de início, temperatura e step."""

    fx = funcao(x, y)
    (xm, ym, f_max) = (x, y, fx)

    while temp > 0.01:

        xx = x + uniform(-1 * step, step)
        yy = y + uniform(-1 * step, step)
        fxx = funcao(xx, yy)

        delta = (fxx - fx) / fx
        if fxx > f_max:
            (xm, ym, f_max) = (xx, yy, fxx)

        if delta > 0:
            (x, y, fx) = (xx, yy, fxx)
        else:
            if randint(0, 100) < 100 * math.exp(10 * delta / temp):
                (x, y, fx) = (xx, yy, fxx)

        temp = temp - 0.01

    return (xm, ym)


# Rotina main()
print "*************************************"
print "*                                   *"
print "*     Problema do Máximo de f(x)    *"
print "*                                   *"
print "*************************************"

solution = tempera_simulada(5.0, 3.0, 10.0, 1.0)
print solution
print funcao(solution[0], solution[1])
