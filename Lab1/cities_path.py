# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Algoritmos greedy e A*."""
from pprint import pprint
from graphics import *
from Queue import PriorityQueue
import copy
import math
import sys


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
    id_current = id_origin
    total_distance = 0
    solution.append(id_current)
    while id_current != id_destination:
        # Resetando variáveis
        id_next_city = 0
        min_distance = sys.maxint
        # Procura caminhos a partir da cidade atual
        for i, id_city in enumerate(graph[id_current]):
            if i < 3 or id_city in solution:
                continue
            # Distância da cidade atual até a adjacente
            current_city_distance = distance(id_current, id_city)
            # Estima distância da cidade adjacente até o destino
            city_destination_distance = distance(id_city, id_destination)
            # Estimativa da distância total através da cidade adjacente
            estimated_current_distance =\
                current_city_distance + city_destination_distance

            # Verifica se o caminho é melhor que os já verificados
            if estimated_current_distance < min_distance:
                min_distance = estimated_current_distance
                id_next_city = id_city

        print id_current
        # Determina a melhor cidade adjacente para prosseguir viagem
        id_current = id_next_city
        total_distance += min_distance
        solution.append(id_current)

    # Exibe o resultado do menor caminho usando A*
    print "Menor distância = " + total_distance
    pprint(solution)


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
        tupla = queue.get()
        (_, id_current, visited, solution) = tupla
        solution = copy.copy(solution)

        # Procura caminhos a partir da cidade atual
        for i, id_city in enumerate(graph[id_current]):
            # Se a cidade já foi visitada, não é incluída
            if i < 3 or id_city in visited:
                continue
            # Estima distância da cidade adjacente até o destino
            city_destination_distance = distance(id_city, id_destination)
            visited.append(id_city)
            solution.append(id_city)
            queue.put((city_destination_distance, id_city, visited, solution))

            # Verifica se o destino foi alcançado
            if id_city == id_destination:
                return solution


def find_path(id_origin, id_destination):
    u"""Encontra o menor caminho usando algoritmo."""
    global path
    path = find_path_greedy("202", "601")
    # Calcula a menor distância do caminho solução
    id_current = id_origin
    total_distance = 0
    for id_city in path:
        total_distance += distance(id_current, id_city)
        id_current = id_city

    # Imprimindo a solução
    print(path)
    print "Menor distância = " + str(total_distance)


path = []
graph = {}

# Rotina main()
print "*************************************"
print "*                                   *"
print "*            Algoritmo A*           *"
print "*                                   *"
print "*************************************"
read_map('Uruguay.csv')
find_path("202", "601")
resize_map()
print_map()
