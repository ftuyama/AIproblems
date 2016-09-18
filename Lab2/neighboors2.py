# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Problema dos vizinhos de Einstein."""
from pprint import pprint
import copy


def restricoes(info):
    u"""Nro restrições quebradas."""
    restricoes = [
        undefined(["ingles", "vermelha"], info) or
        info["ingles"] == info["vermelha"],

        undefined(["espanhol", "cachorro"], info) or
        info["espanhol"] == info["cachorro"],

        undefined(["noruegues"], info) or
        info["noruegues"] == 0,

        undefined(["kool", "amarela"], info) or
        info["kool"] == info["amarela"],

        undefined(["chesterfield", "raposa"], info) or
        abs(info["chesterfield"] - info["raposa"]) == 1,

        undefined(["noruegues", "azul"], info) or
        abs(info["noruegues"] - info["azul"]) == 1,

        undefined(["winston", "caramujos"], info) or
        info["winston"] == info["caramujos"],

        undefined(["lucky_strike", "suco_laranja"], info) or
        info["lucky_strike"] == info["suco_laranja"],

        undefined(["ucraniano", "cha"], info) or
        info["ucraniano"] == info["cha"],

        undefined(["japones", "parliament"], info) or
        info["japones"] == info["parliament"],

        undefined(["kool", "cavalo"], info) or
        abs(info["kool"] - info["cavalo"]),

        undefined(["cafe", "verde"], info) or
        info["cafe"] == info["verde"],

        undefined(["verde", "marfim"], info) or
        info["verde"] == info["marfim"] + 1,

        undefined(["leite"], info) or
        info["leite"] == 2,
    ]
    return len(restricoes) - sum(restricoes)


def undefined(fields, info):
    u"""Verifica se algum campo é nulo."""
    for field in fields:
        if info[field] == -1:
            return True
    return False


def pretty_print(info):
    u"""Imprime a solução de forma elegante."""
    pprint(sorted(info.items(), key=lambda x: x[1]))


def select_var(info):
    u"""Seleciona variável não atribuída."""
    # Usa heurística de menor domínio
    p_var = []
    min_domain = 5
    for i in range(5):
        for j in range(5):
            if info[groups[j][i]] == -1:
                domain = select_domain(info, i, groups[j])
                if len(domain) < min_domain:
                    p_var = [(i, j, domain)]
                    min_domain = len(domain)
                elif len(domain) == min_domain:
                    p_var.append((i, j, domain))
    return p_var


def select_domain(info, val, group):
    u"""Seleciona domínio da variável."""
    domain = [0, 1, 2, 3, 4]
    for i in range(5):
        if info[group[i]] != -1:
            if info[group[i]] in domain:
                domain.remove(info[group[i]])
        if i in domain:
            inspect = copy.deepcopy(info)
            inspect[group[val]] = i
            if restricoes(inspect) != 0:
                domain.remove(i)

    return domain


def is_solved(info):
    u"""Verifica se foi resolvido."""
    return not (-1 in info.values())


def backtracking(info):
    u"""Verifica se algum campo é nulo."""
    if is_solved(info):
        return info
    for (var, group, domain) in select_var(info):
        for value in domain:
            new_info = copy.deepcopy(info)
            new_info[groups[group][var]] = value
            if not (new_info in visited):
                visited.append(new_info)
                result = backtracking(new_info)
                if result is not None:
                    return result
    return None

print "*************************************"
print "*                                   *"
print "* Problema dos vizinhos de Einstein *"
print "*                                   *"
print "*************************************"

cores = ["vermelha", "amarela", "azul", "marfim", "verde"]
pessoas = ["ingles", "espanhol", "noruegues", "ucraniano", "japones"]
marcas = ["kool", "chesterfield", "winston", "lucky_strike", "parliament"]
bebidas = ["suco_laranja", "cha", "cafe", "leite", "agua"]
animais = ["cachorro", "raposa", "caramujos", "cavalo", "zebra"]
groups = [cores, pessoas, marcas, bebidas, animais]

neigh = {}
visited = []
for i in range(5):
    neigh[cores[i]] = neigh[pessoas[i]] = neigh[marcas[i]] = \
        neigh[bebidas[i]] = neigh[animais[i]] = -1

pretty_print(backtracking(neigh))
