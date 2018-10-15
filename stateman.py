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

class Statemanager(object):
    # Litt uklart hva som skal ligge
    def __init__(self,data):
        pass

class NimGame(object):
    def __init__(self,G,P,M,N,K, verbose):
        self.G = G
        self.P = P
        self.M = M
        self.N = N
        self.K = K
        self.verbose_mode = verbose

class NimState(object):
    def __init__(self, chips):
        self.chips = chips

    def Actions(self, K, chips):
        if chips >= K:
            return [i for i in range(1,K+1)]
        else:
            return [i for i in range(1,chips+1)]

    def DoAction(self,action):
        self.chips -= action

class Node(object):
    def __init__(self,move, parent, state):
        self.move = move
        self.parentNode = parent
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.Actions()

    def add_child(self, move, state):
        node = Node(move = move, parent = self, state = state)
        self.childNodes.append(node)

class UCT(object):
    def __init__(self,data):