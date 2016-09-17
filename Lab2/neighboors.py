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
        if 'number' in piece1.joints() and 'number' in piece2.joints():
            return abs(piece1.dicty['number'] - piece2.dicty['number']) == 1

    def neighboors_right(self, piece1, piece2):
        u"""Verifica se as peças são vizinhas."""
        if 'number' in piece1.joints() and 'number' in piece2.joints():
            return piece1.dicty['number'] - piece2.dicty['number'] == 1

    def board_restriction(self, piece1, piece2, repeat):
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

        if not repeat:
            if piece1.has({'casa': 'verde'}) and \
                    piece2.has({'casa': 'marfim'}):
                if not self.neighboors_right(piece1, piece2):
                    return False

        return True

    def board_fits(self, piece1, piece2):
        u"""Verifica se a peça se encaixa no tabuleiro."""
        return self.board_restriction(piece1, piece2, False) and \
            self.board_restriction(piece2, piece1, True)

    def piece_fits(self, piece1, piece2):
        u"""Verifica se a peça se encaixa."""
        intersection = piece1.joints() & piece2.joints()
        if len(intersection) == 0:
            return True
        for key in intersection:
            if piece1.dicty[key] != piece2.dicty[key]:
                return False
        return True

    def fits(self, piece1, piece2):
        u"""Verifica se encaixe é possível."""
        return self.piece_fits(piece1, piece2) and \
            self.board_fits(piece1, piece2)

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
            return (pieces5, pieces1)
        if len(pieces4) > 0:
            if len(pieces2) > 0:
                return (pieces4, pieces2)
            return (pieces4, pieces1)
        if len(pieces3) > 1:
            return (pieces3, pieces3)
        if len(pieces3) > 0:
            if len(pieces2) > 0:
                return (pieces3, pieces2)
            return (pieces3, pieces1)
        if len(pieces2) > 1:
            return (pieces2, pieces2)
        if len(pieces2) > 0:
            return (pieces2, pieces1)
        return (pieces1, pieces1)

    def backtracking(self, pieces):
        u"""Usa backtracking para resolver."""
        if len(pieces) == 5:
            return pieces
        (pieces1, pieces2) = self.select_pieces(pieces)
        for piece1 in pieces1:
            for piece2 in pieces2:
                if not piece1.same(piece2):
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
