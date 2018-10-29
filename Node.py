from math import *
import random

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of player_just_moved.
        Crashes if state not specified.
    """

    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parentNode = parent  # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = state.get_moves()  # child nodes
        self.player_just_moved = state.player_just_moved

    def select_child(self):
        """
        Heuristikk hentet fra https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
        
        c.wins stands for the number of wins for the node considered after the i-th move
        c.visits stands for the number of simulations for the node considered after the i-th move
        self.visits stands for the total number of simulations after the i-th move
        """
        s = max(self.childNodes, key=lambda c: c.wins / c.visits + sqrt(2 * log(self.visits) / c.visits))
        return s

    def add_child(self, m, s):
        """ Remove m from untried_moves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move=m, parent=self, state=s)
        self.untried_moves.remove(m)
        self.childNodes.append(n)
        return n

    def update(self, result):
        """
        Oppdaterer antallet visits og wins på en node
        """
        self.visits += 1
        self.wins += result

    def children_to_string(self):
        """
        Brukes for å gi kontinuerlig statistikk om rollout-prosessen underveis i spillet.
        """
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s

    def __repr__(self):
        return "[Move: " + str(self.move) + ", Wins/Visits: " + str(int(self.wins)) + "/" + str(int(self.visits)) + "]"