# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Problema dos vizinhos de Einstein."""
from pprint import pprint


class House:
    u"""Objeto casa."""

    cor = ""
    pessoa = ""
    marca = ""
    bebida = ""
    animal = ""


def restricoes(house):
    u"""Nro restrições quebradas."""



cores = ["vermelha", "amarela", "azul", "laranja", "verde"]
pessoas = ["ingles", "espanhol", "noruegues", "ucraniano", "japones"]
marcas = ["kool", "chesterfield", "winston", "lucky_strike", "parliament"]
bebidas = ["suco_laranja", "cha", "cafe", "leite", "agua"]
animais = ["cachorro", "raposa", "caramujos", "cavalo", "zebra"]

houses = [House() for i in range(5)]
pprint(houses)
# Rotina main()
print "*************************************"
print "*                                   *"
print "* Problema dos vizinhos de Einstein *"
print "*                                   *"
print "*************************************"
