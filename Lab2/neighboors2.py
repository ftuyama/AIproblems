# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Problema dos vizinhos de Einstein."""
from pprint import pprint
import copy


def restricoes(info):
    u"""Nro restrições quebradas."""
    restricoes = [
        info["ingles"] == info["vermelha"] or
        undefined(["ingles", "vermelha"], info),

        info["espanhol"] == info["cachorro"] or
        undefined(["espanhol", "cachorro"], info),

        info["kool"] == info["amarela"] or
        undefined(["kool", "amarela"], info),

        abs(info["chesterfield"] - info["raposa"]) == 1 or
        undefined(["chesterfield", "raposa"], info),

        abs(info["noruegues"] - info["azul"]) == 1 or
        undefined(["noruegues", "azul"], info),

        info["winston"] == info["caramujos"] or
        undefined(["winston", "caramujos"], info),

        info["lucky_strike"] == info["suco_laranja"] or
        undefined(["lucky_strike", "suco_laranja"], info),

        info["ucraniano"] == info["cha"] or
        undefined(["ucraniano", "cha"], info),
        info["japones"] == info["parliament"] or
        undefined(["japones", "parliament"], info),

        abs(info["kool"] - info["cavalo"]) or
        undefined(["kool", "cavalo"], info),

        info["cafe"] == info["verde"] or
        undefined(["cafe", "verde"], info),

        info["verde"] == info["marfim"] + 1 or
        undefined(["verde", "marfim"], info),

        info["leite"] == 2 or
        undefined(["leite"], info)
    ]
    return len(restricoes) - sum(restricoes)


def undefined(fields, info):
    u"""Verifica se algum campo é nulo."""
    for field in fields:
        if info[field] == -1:
            return True
    return False


def select_var(info):
    u"""Seleciona variável não atribuída."""
    p_var = []
    for i in range(5):
        for group in groups:
            if info[group[i]] == -1:
                p_var.append((i, group))
    return p_var


def select_domain(info, group):
    u"""Seleciona domínio da variável."""
    domain = []
    for i in range(5):
        if info[group[i]] == -1:
            domain.append(i)
    return domain


def is_solved(info):
    u"""Verifica se foi resolvido."""
    if restricoes(info) != 0:
        return False
    for i in range(5):
        for group in groups:
            if info[group[i]] == -1:
                return False
    return True


def backtracking(info):
    u"""Verifica se algum campo é nulo."""
    info = copy.deepcopy(info)
    # pprint(info)
    if is_solved(info):
        return info
    p_var = select_var(info)
    for s_var in p_var:
        (var, group) = s_var
        domain = select_domain(info, group)
        for value in domain:
            new_info = copy.deepcopy(info)
            new_info[group[var]] = value
            if restricoes(new_info) == 0:
                result = backtracking(new_info)
                if result is not None:
                    return result
    return None

cores = ["vermelha", "amarela", "azul", "marfim", "verde"]
pessoas = ["ingles", "espanhol", "noruegues", "ucraniano", "japones"]
marcas = ["kool", "chesterfield", "winston", "lucky_strike", "parliament"]
bebidas = ["suco_laranja", "cha", "cafe", "leite", "agua"]
animais = ["cachorro", "raposa", "caramujos", "cavalo", "zebra"]
groups = [cores, pessoas, marcas, bebidas, animais]

info = {}
for i in range(5):
    info[cores[i]] = info[pessoas[i]] = info[marcas[i]] = \
        info[bebidas[i]] = info[animais[i]] = -1

pprint(backtracking(info))

# Rotina main()
print "*************************************"
print "*                                   *"
print "* Problema dos vizinhos de Einstein *"
print "*                                   *"
print "*************************************"
