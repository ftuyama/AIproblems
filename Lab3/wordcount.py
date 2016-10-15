# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Preditor rústico de avaliação."""


def map(lines):
    u"""Avalia a função f(x, y) em dado ponto."""
    map = {}
    # Map
    for line in lines:
        (_, movie, rank, _) = line.split("::")
        if not (movie in map):
            map[movie] = [0, 0, 0, 0, 0, 0]
        map[movie][int(rank)] += 1

    # Reduce
    for movie in map:
        total = sum(map[movie])
        for i in range(1, 6):
            map[movie][0] += i * map[movie][i]
        map[movie][0] = map[movie][0] / total

    return map

advice = map(open("ml-1m/ratings.dat", "r").readlines())

print advice["2"]
