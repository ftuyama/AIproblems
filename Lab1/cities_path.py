# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Algoritmos greedy e A*."""
from graphics import *
from Queue import PriorityQueue
import copy
import math


def print_map():
    u"""Desenha o grafo de rotas a partir do mapa lido."""
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

    # Desenhando percurso
    last_city = graph[path[0]]
    for city_id in path:
        city = graph[city_id]
        line = Line(
            Point(last_city[1], last_city[2]),
            Point(city[1], city[2])
        )
        line.setFill('red')
        line.draw(win)
        last_city = city

    # Desenhando origem e destino
    cir = Circle(Point(graph[path[0]][1], graph[path[0]][2]), 5)
    cir.setFill('red')
    cir.draw(win)
    z = len(path) - 1
    cir = Circle(Point(graph[path[z]][1], graph[path[z]][2]), 5)
    cir.setFill('red')
    cir.draw(win)

    win.getMouse()
    win.close()


def resize_map():
    u"""Ajusta tamanhos para exibição no mapa."""
    for city_id in graph:
        city = graph[city_id]
        city[1] = 200 * (city[1] - 30)
        city[2] = 100 * (city[2] - 52.5)
        graph[city_id] = city


def read_map(file_name):
    u"""Lê o mapa .csv e retorna grafo das rotas."""
    with open(file_name, 'r') as file:
        for line in file:
            line = line.replace(",", ".")
            data = ' '.join(line.split(';')).split()
            data[1] = float(data[1])
            data[2] = float(data[2])
            graph[data[0]] = data
    return graph


def distance(id_city1, id_city2):
    u"""Calcula distância em linha reta."""
    city1 = graph[id_city1]
    city2 = graph[id_city2]
    return math.hypot(city2[2] - city1[2], city2[1] - city1[1])


def find_path_a(id_origin, id_destination):
    u"""Encontra o menor caminho usando A*."""
    # Fila de prioridade - algoritmo guloso
    id_current = id_origin
    queue = PriorityQueue()
    queue.put((
        distance(id_origin, id_destination),
        id_origin, [id_current], [id_current]
    ))

    while not queue.empty():
        # Pega a tupla com menor distância estimada
        (_, id_current, visited, solution) = queue.get()

        # Procura caminhos a partir da cidade atual
        for i, id_city in enumerate(graph[id_current]):
            # Se a cidade já foi visitada, não é incluída
            if i < 3 or id_city in visited:
                continue

            # Distância da cidade atual até a adjacente
            current_city_distance = total_distance(solution)
            # Estima distância da cidade adjacente até o destino
            city_destination_distance = distance(id_city, id_destination)
            # Estimativa da distância total através da cidade adjacente
            estimated_current_distance =\
                current_city_distance + city_destination_distance

            visited.append(id_city)
            path = copy.deepcopy(solution)
            path.append(id_city)
            queue.put((estimated_current_distance, id_city, visited, path))

            # Verifica se o destino foi alcançado
            if id_city == id_destination:
                return path


def find_path_greedy(id_origin, id_destination):
    u"""Encontra o menor caminho usando greedy."""
    # Fila de prioridade - algoritmo guloso
    id_current = id_origin
    queue = PriorityQueue()
    queue.put((
        distance(id_origin, id_destination),
        id_origin, [id_current], [id_current]
    ))

    while not queue.empty():
        # Pega a tupla com menor distância estimada
        (_, id_current, visited, solution) = queue.get()

        # Procura caminhos a partir da cidade atual
        for i, id_city in enumerate(graph[id_current]):
            # Se a cidade já foi visitada, não é incluída
            if i < 3 or id_city in visited:
                continue
            # Estima distância da cidade adjacente até o destino
            city_destination_distance = distance(id_city, id_destination)
            visited.append(id_city)
            path = copy.copy(solution)
            path.append(id_city)
            queue.put((city_destination_distance, id_city, visited, path))

            # Verifica se o destino foi alcançado
            if id_city == id_destination:
                return path


def total_distance(path):
    u"""Calcula distância total do caminho."""
    id_current = path[0]
    total_distance = 0
    for id_city in path:
        total_distance += distance(id_current, id_city)
        id_current = id_city
    return total_distance


def find_path(id_origin, id_destination):
    u"""Encontra o menor caminho usando algoritmo."""
    global path
    # path = find_path_greedy(id_origin, id_destination)
    path = find_path_a(id_origin, id_destination)

    # Imprimindo a solução
    print path
    print "Menor distância = " + str(total_distance(path))


path = []
graph = {}

# Rotina main()
print "*************************************"
print "*                                   *"
print "*       Algoritmos Greedy & A*      *"
print "*                                   *"
print "*************************************"
read_map('Uruguay.csv')
find_path("202", "601")
resize_map()
print_map()
