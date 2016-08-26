# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Algoritmos greedy e A*."""
from pprint import pprint
from graphics import *


def print_map():
    u"""Desenha o grafo de rotas a partir do mapa lido."""
    pprint(graph)
    win = GraphWin('Uruguay', 1050, 650)
    win.setBackground(color_rgb(188, 237, 145))
    title = Text(Point(500, 30), "Uruguay")
    title.setSize(20)
    title.draw(win)
    for origin_id in graph:
        # Desenha a cidade
        origin = graph[origin_id]
        pt = Point(origin[1], origin[2])
        cir = Circle(pt, 5)
        cir.setFill('blue')
        cir.draw(win)
        # Desenha as rotas
        for i, destination_id in enumerate(origin):
            if i < 3:
                continue
            destination = graph[destination_id]
            line = Line(pt, Point(destination[1], destination[2]))
            line.draw(win)
    win.getMouse()
    win.close()


# Leitura do Arquivo de Entrada contendo Mapa
def read_map(file_name):
    u"""Lê o mapa .csv e retorna grafo das rotas."""
    with open(file_name, 'r') as file:
        for line in file:
            line = line.replace(",", ".")
            data = ' '.join(line.split(';')).split()
            data[1] = 200 * (float(data[1]) - 30)
            data[2] = 100 * (float(data[2]) - 52.5)
            graph[data[0]] = data
    return graph

graph = {}

# Rotina main()
print "*************************************"
print "*                                   *"
print "*            Algoritmo A*           *"
print "*                                   *"
print "*************************************"
read_map('Uruguay.csv')
print_map()
