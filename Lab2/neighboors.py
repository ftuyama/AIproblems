# -*- coding: utf-8 -*-
# !/usr/bin/env python
u"""Problema dos vizinhos de Einstein."""
from pprint import pprint
import copy
import sys

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

    def fits(self, piece):
        u"""Verifica se a peça se encaixa."""
        intersection = self.joints() & piece.joints()
        if len(intersection) == 0:
            return True
        for key in intersection:
            if self.dicty[key] != piece.dicty[key]:
                return False
        return True


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

            Piece({'casa': 'marfim'}), Piece({'casa': 'azul'}),
            Piece({'cigarro': 'chesterfield'}), Piece({'bebida': 'agua'}),
            Piece({'animal': 'raposa'}), Piece({'animal': 'cavalo'}),
            Piece({'animal': 'zebra'}), Piece({'numero': 2}),
            Piece({'numero': 4}), Piece({'numero': 5}),
        ]

    def neighboors(self, piece1, piece2):
        u"""Verifica se as peças são vizinhas."""
        if 'numero' in piece1.joints() and 'numero' in piece2.joints():
            return abs(piece1.dicty['numero'] - piece2.dicty['numero']) == 1
        return True

    def neighboors_right(self, piece1, piece2):
        u"""Verifica se as peças são vizinhas."""
        if 'numero' in piece1.joints() and 'numero' in piece2.joints():
            return piece2.dicty['numero'] - piece1.dicty['numero'] == 1
        return True

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
        pieces = copy.deepcopy(pieces)
        new_piece = self.connect_pieces(pieces, piece1, piece2)

        for piece in pieces:
            if not self.board_restric(piece, new_piece):
                return False
        return True

    def fits(self, pieces, piece1, piece2):
        u"""Verifica se encaixe é possível."""
        return piece1.fits(piece2) and \
            self.board_fits(pieces, piece1, piece2)

    def remove(self, pieces, piece):
        u"""Remove uma peça do quebra-cabeças."""
        for a_piece in pieces:
            if a_piece.same(piece):
                pieces.remove(a_piece)
                return

    def connect_pieces(self, pieces, piece1, piece2):
        u"""Encaixa duas peças no quebra-cabeças."""
        piece1 = copy.deepcopy(piece1)
        piece2 = copy.deepcopy(piece2)
        self.remove(pieces, piece1)
        self.remove(pieces, piece2)
        new_dicty = piece1.dicty
        new_dicty.update(piece2.dicty)
        new_piece = Piece(new_dicty)
        pieces.append(new_piece)
        return new_piece

    def select_domain(self, pieces, piece1):
        u"""Verifica peças encaixáveis."""
        domain = []
        for piece2 in pieces:
            if not piece1.same(piece2) and \
                    self.fits(pieces, piece1, piece2):
                domain.append(piece2)
        return domain

    def select_pieces(self, pieces):
        u"""Seleciona peças para tentativas."""
        p_var = []
        min_domain = sys.maxint
        for piece in pieces:
            if piece.size() < 6:
                domain = self.select_domain(pieces, piece)
                if len(domain) < min_domain:
                    p_var = [(piece, domain)]
                    min_domain = len(domain)
                elif len(domain) == min_domain:
                    p_var.append((piece, domain))
        return p_var

    def backtracking(self, pieces):
        u"""Usa backtracking para resolver."""
        if len(pieces) == 5:
            return pieces
        for (piece1, domain) in self.select_pieces(pieces):
            for piece2 in domain:
                new_pieces = copy.deepcopy(pieces)
                self.connect_pieces(new_pieces, piece1, piece2)
                result = self.backtracking(new_pieces)
                if result is not None:
                    return result
        return None

    def solve(self):
        u"""Resolve o quebra-cabeças."""
        self.print_puzzle(self.backtracking(self.pieces))


print "*************************************"
print "*                                   *"
print "* Problema dos vizinhos de Einstein *"
print "*                                   *"
print "*************************************"
puzzle = Puzzle()
puzzle.create_pieces()
puzzle.solve()
