# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Problema dos vizinhos de Einstein."""
from pprint import pprint


def restricoes(info):
    u"""Nro restrições quebradas."""
    restricoes = [
        info["ingles"] == info["vermelha"] or
        undefined(["ingles", "vermelha"]),

        info["espanhol"] == info["cachorro"] or
        undefined(["espanhol", "cachorro"]),

        info["kool"] == info["amarela"] or
        undefined(["kool", "amarela"]),

        abs(info["chesterfield"] - info["raposa"]) == 1 or
        undefined(["chesterfield", "raposa"]),

        abs(info["noruegues"] - info["azul"]) == 1 or
        undefined(["noruegues", "azul"]),

        info["winston"] == info["caramujos"] or
        undefined(["winston", "caramujos"]),

        info["lucky_strike"] == info["suco_laranja"] or
        undefined(["lucky_strike", "suco_laranja"]),

        info["ucraniano"] == info["cha"] or
        undefined(["ucraniano", "cha"]),
        info["japones"] == info["parliament"] or
        undefined(["japones", "parliament"]),

        abs(info["kool"] - info["cavalo"]) or
        undefined(["kool", "cavalo"]),

        info["cafe"] == info["verde"] or
        undefined(["cafe", "verde"]),

        info["verde"] == info["marfim"] + 1 or
        undefined(["verde", "marfim"]),

        info["leite"] == 2 or
        undefined(["leite"])
    ]
    return len(restricoes) - sum(restricoes)


def undefined(fields):
    u"""Verifica se algum campo é nulo."""

cores = ["vermelha", "amarela", "azul", "marfim", "verde"]
pessoas = ["ingles", "espanhol", "noruegues", "ucraniano", "japones"]
marcas = ["kool", "chesterfield", "winston", "lucky_strike", "parliament"]
bebidas = ["suco_laranja", "cha", "cafe", "leite", "agua"]
animais = ["cachorro", "raposa", "caramujos", "cavalo", "zebra"]

info = {}
for i in range(5):
    info[cores[i]] = info[pessoas[i]] = info[marcas[i]] = \
        info[bebidas[i]] = info[animais[i]] = -1

points = restricoes(info)
pprint(info)
pprint(points)
# Rotina main()
print "*************************************"
print "*                                   *"
print "* Problema dos vizinhos de Einstein *"
print "*                                   *"
print "*************************************"
