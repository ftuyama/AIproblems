# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Quebrando arquivo entrada."""
# assume that an average line is about 80 chars long, and that we want about
# 40K in each file.
import threading

SIZE_HINT = 20 * 1000

# fo = open("ml-1m/ratings.dat", "r")
# fo.seek(SIZE_HINT, 0)
# print fo.readlines(SIZE_HINT)


class MapReduce (threading.Thread):
    u"""Avalia a função f(x, y) em dado ponto."""

    def __init__(self, thread_id, lines):
        u"""Avalia a função f(x, y) em dado ponto."""
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = "Thread" + str(thread_id)
        self.lines = lines

    def run(self):
        u"""Avalia a função f(x, y) em dado ponto."""
        print "Starting " + self.name
        map(self.lines)
        print "Exiting " + self.name


def map(lines):
    u"""Avalia a função f(x, y) em dado ponto."""
    map = {}
    for line in lines:
        (_, movie, rank, _) = line.split("::")
        if not (movie in map):
            map[movie] = [0, 0, 0, 0, 0]
        map[movie][int(rank) - 1] += 1
    # print map

lines = open("ml-1m/ratings.dat", "r").readlines()
map(lines)

# Tentativa de usar Threads
# n_threads = 10
# job = len(lines) / n_threads
# for i in range(0, n_threads):
#     MapReduce(i, lines[job * i: job * (i + 1)]).start()
# MapReduce(n_threads, lines[job * n_threads:]).start()
