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

    def size(self):
        u"""Retorna tamanho do dicionário."""
        return len(self.dicty.keys())

    def same(self, piece):
        u"""Verifica se duas peças são a mesma."""
        inteserctions = set(self.dicty.items()) & set(piece.dicty.items())
        return len(inteserctions) == self.size()


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
        if 'numero' in piece1.joints() and 'numero' in piece2.joints():
            return abs(piece1.dicty['numero'] - piece2.dicty['numero']) == 1
        return False

    def neighboors_right(self, piece1, piece2):
        u"""Verifica se as peças são vizinhas."""
        if 'numero' in piece1.joints() and 'numero' in piece2.joints():
            return piece2.dicty['numero'] - piece1.dicty['numero'] == 1
        return False

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

        if piece1.has({'casa': 'marfim'}) and \
                piece2.has({'casa': 'verde'}):
            if not self.neighboors_right(piece1, piece2):
                return False

        return True

    def board_restric(self, piece1, piece2):
        u"""Aplica verificação simétrica."""
        return self.board_restriction(piece1, piece2) and \
            self.board_restriction(piece2, piece1)

    def board_fits(self, pieces, piece1, piece2):
        u"""Verifica se a peça se encaixa no tabuleiro."""
        if not self.board_restric(piece1, piece2):
            return False
        for piece in pieces:
            if not (self.board_restric(piece, piece1) and
                    self.board_restric(piece, piece2)):
                return False
        return True

    def piece_fits(self, piece1, piece2):
        u"""Verifica se a peça se encaixa."""
        intersection = piece1.joints() & piece2.joints()
        if len(intersection) == 0:
            return True
        for key in intersection:
            if piece1.dicty[key] != piece2.dicty[key]:
                return False
        return True

    def fits(self, pieces, piece1, piece2):
        u"""Verifica se encaixe é possível."""
        return self.piece_fits(piece1, piece2) and \
            self.board_fits(pieces, piece1, piece2)

    def remove(self, pieces, piece):
        u"""Remove uma peça do quebra-cabeças."""
        for a_piece in pieces:
            if a_piece.same(piece):
                pieces.remove(a_piece)
                return

    def connect_pieces(self, pieces, piece1, piece2):
        u"""Encaixa duas peças no quebra-cabeças."""
        self.remove(pieces, piece1)
        self.remove(pieces, piece2)
        new_dicty = piece1.dicty
        new_dicty.update(piece2.dicty)
        pieces.append(Piece(new_dicty))

    def divide(self, pieces):
        u"""Seleciona peças para tentativas."""
        size_pieces = [[], [], [], [], []]
        for piece in pieces:
            if piece.size() != 6:
                size_pieces[piece.size() - 1].append(piece)
        return size_pieces

    def select_pieces(self, pieces):
        u"""Seleciona peças para tentativas."""
        (pieces1, pieces2, pieces3, pieces4, pieces5) = self.divide(pieces)
        possible = []

        if len(pieces5) > 0:
            possible.append((pieces5, pieces1))
        if len(pieces4) > 0:
            if len(pieces2) > 0:
                possible.append((pieces4, pieces2))
            possible.append((pieces4, pieces1))
        if len(pieces3) > 1:
            possible.append((pieces3, pieces3))
        if len(pieces3) > 0:
            if len(pieces2) > 0:
                possible.append((pieces3, pieces2))
            possible.append((pieces3, pieces1))
        if len(pieces2) > 1:
            possible.append((pieces2, pieces2))
        if len(pieces2) > 0:
            possible.append((pieces2, pieces1))
        possible.append((pieces1, pieces1))
        return possible

    def backtracking(self, pieces):
        u"""Usa backtracking para resolver."""
        if len(pieces) == 5:
            return pieces
        possible = self.select_pieces(pieces)
        for (pieces1, pieces2) in possible:
            for piece1 in pieces1:
                for piece2 in pieces2:
                    if not piece1.same(piece2):
                        if self.fits(pieces, piece1, piece2):
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
        self.pieces = self.backtracking(self.pieces)
        self.print_puzzle(self.pieces)


print "*************************************"
print "*                                   *"
print "* Problema dos vizinhos de Einstein *"
print "*                                   *"
print "*************************************"
visited = []
puzzle = Puzzle()
puzzle.create_pieces()
puzzle.solve()
# puzzle.pieces = [
#     Piece({
#         'numero': 1,
#         'cor': 'amarela',
#         'cigarro': 'kool',
#         'bebida': 'agua',
#         'animal': 'raposa',
#         'pessoa': 'noruegues'
#     }),
#     Piece({
#         'numero': 2,
#         'animal': 'cavalo',
#         'bebida': 'cha',
#         'pessoa': 'ucraniano',
#         'cor': 'azul',
#         'cigarro': 'chesterfield'
#     }),
#     Piece({
#         'numero': 3,
#         'cigarro': 'winston',
#         'cor': 'vermelha',
#         'animal': 'caramujos',
#         'bebida': 'leite',
#         'pessoa': 'ingles'
#     }),
#     Piece({
#         'numero': 4,
#         'bebida': 'suco_laranja',
#         'animal': 'cachorro',
#         'cigarro': 'lucky_strike',
#         'pessoa': 'espanhol',
#         'cor': 'marfim'
#     }),
#     Piece({
#         'bebida': 'cafe',
#         'pessoa': 'japones',
#         'cigarro': 'parliament',
#         'cor': 'verde',
#         'animal': 'zebra'
#     }),
#     Piece({
#         'numero': 5
#     })
# ]
