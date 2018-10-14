"""
1. Tree Search - Traversing the tree from the root to a leaf node by using the tree policy.
2. Node Expansion - Generating some or all child states of a parent state, and then connecting the tree
node housing the parent state (a.k.a. parent node) to the nodes housing the child states (a.k.a. child
nodes).
3. Leaf Evaluation - Estimating the value of a leaf node in the tree by doing a rollout simulation using
the default policy from the leaf node’s state to a final state.
4. Backpropagation - Passing the evaluation of a final state back up the tree, updating relevant data (see
course lecture notes) at all nodes and edges on the path from the final state to the tree root.
"""
import math

class State(object):
    def __init__(self):
        self.actions = []

        self.visited = 0
        self.visited_success = 0

    def add_action(self, obj):
        self.actions.append(obj)

    def policy(self, visited, visited_success):
        return



class Stateman(object):
    def __init__(self,data):

class Board(object):
    def start(self):
        # Returns a representation of the starting state of the game.
        pass

    def current_player(self, state):
        # Takes the game state and returns the current player's
        # number.
        pass

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        pass

    def legal_plays(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        pass

    def winner(self, state_history):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        pass

class MonteCarlo(object):
    def __init__(self, board, **kwargs):
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.
        pass

    def update(self, state):
        # Takes a game state, and appends it to the history.
        pass

    def get_play(self):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        pass

    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        pass