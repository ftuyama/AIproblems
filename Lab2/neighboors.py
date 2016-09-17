# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Problema dos vizinhos de Einstein."""
from pprint import pprint
import copy

'''
Nessa solução, temos vários objetos "Peças" que
correspondem a restrições impostas. Em seguida,
elas são conectadas como um quebra-cabeças.
'''


class Piece(object):
    u"""Peça de informação."""

    def __init__(self, dicty):
        u"""Inicializa peça."""
        self.dicty = dicty

    def joints(self):
        u"""Retorna chaves do dicionário."""
        return set(self.dicty.keys())

    def has(self, dic):
        u"""Verifica se contém a propriedade."""
        return set(dic.items()).issubset(set(self.dicty.items()))

    def length(self):
        u"""Retorna tamanho do dicionário."""
        return len(self.dicty.keys())


class Puzzle(object):
    u"""Engine do jogo de quebra cabeças."""

    def print_puzzle(self, pieces):
        u"""Mostra o quebra cabeça."""
        print "\nPuzzle:"
        for piece in pieces:
            pprint(piece.dicty)

    def create_pieces(self):
        u"""Cria as peças iniciais."""
        self.pieces = [
            Piece({'pessoa': 'ingles', 'casa': 'vermelha'}),
            Piece({'pessoa': 'espanhol', 'animal': 'cachorro'}),
            Piece({'pessoa': 'noruegues', 'numero': 1}),
            Piece({'cigarro': 'kool', 'casa': 'amarela'}),
            Piece({'cigarro': 'winston', 'animal': 'caramujos'}),
            Piece({'cigarro': 'lucky_strike', 'bebida': 'suco_laranja'}),
            Piece({'pessoa': 'ucraniano', 'bebida': 'cha'}),
            Piece({'pessoa': 'japones', 'cigarro': 'parliament'}),
            Piece({'bebida': 'cafe', 'casa': 'verde'}),
            Piece({'bebida': 'leite', 'numero': 3}),

            Piece({'casa': 'marfim'}), Piece({'casa': 'laranja'}),
            Piece({'cigarro': 'chesterfield'}), Piece({'bebida': 'agua'}),
            Piece({'animal': 'raposa'}), Piece({'animal': 'cavalo'}),
            Piece({'animal': 'zebra'}), Piece({'numero': 2}),
            Piece({'numero': 4}), Piece({'numero': 5}),
        ]

    def neighboors(self, piece1, piece2):
        u"""Verifica se as peças são vizinhas."""
        if 'number' in piece1.joints() and 'number' in piece2.joints():
            return abs(piece1.dicty['number'] - piece2.dicty['number']) == 1

    def neighboors_right(self, piece1, piece2):
        u"""Verifica se as peças são vizinhas."""
        if 'number' in piece1.joints() and 'number' in piece2.joints():
            return piece1.dicty['number'] - piece2.dicty['number'] == 1

    def board_restriction(self, piece1, piece2):
        u"""Verifica restrições do tabuleiro."""
        if piece1.has({'cigarro': 'chesterfield'}) and \
                piece2.has({'animal': 'raposa'}):
            if not self.neighboors(piece1, piece2):
                return False

        if piece1.has({'pessoa': 'noruegues'}) and \
                piece2.has({'casa': 'azul'}):
            if not self.neighboors(piece1, piece2):
                return False

        if piece1.has({'cigarro': 'kool'}) and \
                piece2.has({'animal': 'cavalo'}):
            if not self.neighboors(piece1, piece2):
                return False

        if piece1.has({'casa': 'verde'}) and \
                piece2.has({'casa': 'marfim'}):
            if not self.neighboors_right(piece1, piece2):
                return False

        return True

    def board_fits(self, piece1, piece2):
        u"""Verifica se a peça se encaixa no tabuleiro."""
        return self.board_restriction(piece1, piece2) and \
            self.board_restriction(piece2, piece1)

    def piece_fits(self, piece1, piece2):
        u"""Verifica se a peça se encaixa."""
        return len(piece1.joints() & piece2.joints()) == 0

    def fits(self, piece1, piece2):
        u"""Verifica se encaixe é possível."""
        return self.piece_fits(piece1, piece2) and \
            self.board_fits(piece1, piece2)

    def connect_pieces(self, pieces, piece1, piece2):
        u"""Encaixa duas peças no quebra-cabeças."""
        pieces.remove(piece1)
        pieces.remove(piece2)
        pieces.append(
            Piece(dict(piece1.dicty.items() + piece2.dicty.items()))
        )

    def select_pieces(self, pieces):
        u"""Seleciona peças para tentativas."""

    def backtracking(self, pieces):
        u"""Usa backtracking para resolver."""
        if len(pieces) == 5:
            return pieces
        for piece1 in pieces:
            for piece2 in pieces:
                if piece1.length() + piece2.length() > 5:
                    pass
                if self.fits(piece1, piece2):
                    self.print_puzzle(pieces)
                    new_pieces = copy.copy(pieces)
                    self.connect_pieces(new_pieces, piece1, piece2)
                    if not (new_pieces in visited):
                        visited.append(pieces)
                        result = self.backtracking(new_pieces)
                        if result is not None:
                            return result
        return None

    def solve(self):
        u"""Resolve o quebra-cabeças."""
        puzzle.print_puzzle(self.backtracking(self.pieces))


print "*************************************"
print "*                                   *"
print "* Problema dos vizinhos de Einstein *"
print "*                                   *"
print "*************************************"
visited = []
puzzle = Puzzle()
puzzle.create_pieces()
puzzle.solve()
