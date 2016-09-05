# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Algoritmo do Máximo de f(x)."""
import math


def funcao(x, y):
    u"""Avalia a função f(x, y) em dado ponto."""
    termo1 = 4 * math.exp(-1 * (x**2 + y**2))
    termo2 = math.exp(-1 * ((x - 5)**2 + (y - 5)**2))
    termo3 = math.exp(-1 * ((x + 5)**2 + (y + 5)**2))
    termo4 = math.exp(-1 * ((x + 5)**2 + (y + 5)**2))
    return termo1 + termo2 + termo3 + termo4


# Rotina main()
print "*************************************"
print "*                                   *"
print "*     Problema do Máximo de f(x)    *"
print "*                                   *"
print "*************************************"

print funcao(-1, -1)
print funcao(-1, 1)
print funcao(0, 0)
print funcao(1, -1)
print funcao(1, 1)

print funcao(5, 0)
print funcao(5, 5)
