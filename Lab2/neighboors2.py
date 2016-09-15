# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Problema dos vizinhos de Einstein."""
from pprint import pprint
import copy


def restricoes(info, analysis):
    u"""Nro restrições quebradas."""
    restricoes = [
        undefined(["ingles", "vermelha"], info, analysis) or
        info["ingles"] == info["vermelha"],

        undefined(["espanhol", "cachorro"], info, analysis) or
        info["espanhol"] == info["cachorro"],

        undefined(["kool", "amarela"], info, analysis) or
        info["kool"] == info["amarela"],

        undefined(["chesterfield", "raposa"], info, analysis) or
        abs(info["chesterfield"] - info["raposa"]) == 1,

        undefined(["noruegues", "azul"], info, analysis) or
        abs(info["noruegues"] - info["azul"]) == 1,

        undefined(["winston", "caramujos"], info, analysis) or
        info["winston"] == info["caramujos"],

        undefined(["lucky_strike", "suco_laranja"], info, analysis) or
        info["lucky_strike"] == info["suco_laranja"],

        undefined(["ucraniano", "cha"], info, analysis) or
        info["ucraniano"] == info["cha"],
        undefined(["japones", "parliament"], info, analysis) or
        info["japones"] == info["parliament"],

        undefined(["kool", "cavalo"], info, analysis) or
        abs(info["kool"] - info["cavalo"]),

        undefined(["cafe", "verde"], info, analysis) or
        info["cafe"] == info["verde"],

        undefined(["verde", "marfim"], info, analysis) or
        info["verde"] == info["marfim"] + 1,

        undefined(["leite"], info, analysis) or
        info["leite"] == 2,
    ]
    return len(restricoes) - sum(restricoes)


def undefined(fields, info, analysis):
    u"""Verifica se algum campo é nulo."""
    global grau
    for field in fields:
        if analysis:
            grau[field] += 1
        elif info[field] == -1:
            return True
    return False


def analyse_grau():
    u"""Ordena map por número de graus."""
    global grau
    global info
    restricoes(info, True)
    grau = sorted(grau.items(), key=lambda x: x[1], reverse=True)


def pretty_print(info):
    u"""Imprime a solução de forma elegante."""
    info = sorted(info.items(), key=lambda x: x[1])
    pprint(info)


def select_var(info):
    u"""Seleciona variável não atribuída."""
    # Usa heurística de menor domínio
    p_var = []
    min_domain = 5
    for i in range(5):
        for group in groups:
            if info[group[i]] == -1:
                domain = select_domain(info, group)
                if len(domain) < min_domain:
                    p_var = [(i, group)]
                    min_domain = len(domain)
                elif len(domain) == min_domain:
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
    if restricoes(info, False) != 0:
        return False
    for i in range(5):
        for group in groups:
            if info[group[i]] == -1:
                return False
    return True


def backtracking(info):
    u"""Verifica se algum campo é nulo."""
    info = copy.deepcopy(info)
    if is_solved(info):
        return info
    p_var = select_var(info)
    for s_var in p_var:
        (var, group) = s_var
        for value in select_domain(info, group):
            new_info = copy.deepcopy(info)
            new_info[group[var]] = value
            if restricoes(new_info, False) == 0:
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
grau = {}
for i in range(5):
    info[cores[i]] = info[pessoas[i]] = info[marcas[i]] = \
        info[bebidas[i]] = info[animais[i]] = -1
    grau[cores[i]] = grau[pessoas[i]] = grau[marcas[i]] = \
        grau[bebidas[i]] = grau[animais[i]] = 0

# analyse_grau()
pretty_print(backtracking(info))

# Rotina main()
print "*************************************"
print "*                                   *"
print "* Problema dos vizinhos de Einstein *"
print "*                                   *"
print "*************************************"
