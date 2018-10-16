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
import random

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
    def __init__(self, P, chips, K):
        self.chips = chips
        self.player_moved = P   # Determines which player stats (1/2)
        self.K = K              # Maximum number of allowed chips to pick at once

    def Actions(self):
        if self.chips >= self.K:
            return [i for i in range(1,self.K+1)]
        else:
            return [i for i in range(1,self.chips+1)]

    def DoAction(self,action):
        self.chips -= action

    def get_result(self, player_moved):
        if self.chips == 0:
            if self.player_moved == 2:
                return 1
            elif self.player_moved == 1:
                return 0
        else:
            return 0

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
        self.untriedMoves.remove(move)
        self.childNodes.append(node)

    def select_child(self):
        s = sorted(self.childNodes, key=lambda c: c.wins / c.visits + math.sqrt(2 * math.log(self.visits) / c.visits))[-1]
        return s

    def update(self, result):
        self.visits += 1
        self.wins += result



def UCT(rootstate, itermax, verbose):
    root = Node(state = rootstate, parent = None, move = None)

    for i in range(itermax):
        node = root
        state = rootstate

        while len(node.untriedMoves) == 0 and len(node.childNodes) != 0:
            node = node.select_child()
            state.DoAction(random.choice(state.Actions()))

        if len(node.untriedMoves) != 0:
            move = random.choice(node.untriedMoves)
            state.DoAction(move)
            node = node.add_child(move, state)

        while len(state.Actions()) != 0:
            state.DoAction(random.choice(state.Actions()))

        while node != None:
            node.update(state.get_result(node.player_moved))
            node = node.parentNode

    #if verbose == 1:
    #    pass

def PlayGame(P,N,K):
    state = NimState(P = P, chips = N, K =K)
    while len(state.Actions()) != 0:
        if state.player_moved == 1:
            move = UCT(rootstate=state, itermax=1000, verbose=False)
        else:
            move = UCT(rootstate=state, itermax=1000, verbose=False)
        print("Best Move: " + str(move) + "\n")
        state.DoAction(move)
    if state.get_result(state.player_moved) == 1.0:
        print("Player " + str(state.player_moved) + " wins!")
    elif state.get_result(state.player_moved) == 0.0:
        print("Player " + str(3 - state.player_moved) + " wins!")
    else:
        print("Nobody wins!")

print(PlayGame(2,15,3))