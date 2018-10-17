from math import *
import random

class GameSetting:
    def __init__(self, G, P, M, N, K, verbose):
        self.G = G
        self.P = P
        self.M = M
        self.N = N
        self.K = K
        self.verbose = verbose


class NimState:
    """ A state of the game Nim. In Nim, players alternately take 1,2 or 3 chips with the
        winner being the player to take the last chip.
        In Nim any initial state of the form 4n+k for k = 1,2,3 is a win for player 1
        (by choosing k) chips.
        Any initial state of the form 4n is a win for player 2.
    """

    def __init__(self, game_setting):
        #self.playerJustMoved = 2  # At the root pretend the player just moved is p2 - p1 has the first move
        #self.chips = ch
        self.stones_remaining = game_setting.N
        self.playerJustMoved = game_setting.P
        self.game_setting = game_setting

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = NimState(self.game_setting)
        st.playerJustMoved = self.playerJustMoved
        return st

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerJustMoved.
        """
        #assert move >= 1 and move <= 3 and move == int(move)
        self.stones_remaining -= move
        self.playerJustMoved = 3 - self.playerJustMoved

    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        K = self.game_setting.K

        if K > self.stones_remaining:
            return [i for i in range(1, self.stones_remaining+1)]
        else:
            return [i for i in range(1, K+1)]
        
        #return [i for i in range(1, min([4, self.stones_remaining + 1]))]

    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm.
        """
        assert self.stones_remaining == 0
        if self.playerJustMoved == playerjm:
            return 1.0  # playerjm took the last chip and has won
        else:
            return 0.0  # playerjm's opponent took the last chip and has won


class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """

    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parentNode = parent  # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves()  # future child nodes
        self.playerJustMoved = state.playerJustMoved  # the only part of the state that the Node needs later

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key=lambda c: c.wins / c.visits + sqrt(2 * log(self.visits) / c.visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move=m, parent=self, state=s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(
            self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
            s += c.TreeToString(indent + 1)
        return s

    def IndentString(self, indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
            s += str(c) + "\n"
        return s


def UCT(rootstate, itermax, verbose=False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    root = Node(state=rootstate)

    for i in range(itermax):
        node = root
        state = rootstate.Clone()

        # Select
        while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)

        # Expand
        if node.untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            node = node.AddChild(m, state)  # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []:  # while state is non-terminal
            state.DoMove(random.choice(state.GetMoves()))

        # Backpropagate
        while node != None:  # backpropagate from the expanded node and work back to the root node
            node.Update(state.GetResult(
                node.playerJustMoved))  # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode

    # Output some information about the tree - can be omitted
    # Noe dritt man egentlig ikke trenger
    """
    if (verbose == True):
        print(root.TreeToString(0))
    else:
        print(root.ChildrenToString())
    """
    return sorted(root.childNodes, key=lambda c: c.visits)[-1].move  # return the move that was most visited


def UCTPlayGame(G,P,M,N,K,verbose):
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    game_setting = GameSetting(G,P,M,N,K,verbose)
    
    state = NimState(game_setting)  # uncomment to play Nim with the given number of starting stones
    while (state.GetMoves() != []):
        #print(str(state))
        #print("test")
        if state.playerJustMoved == 1:
            m = UCT(rootstate=state, itermax=M, verbose=verbose)  # play with values for itermax and verbose = True
        else:
            m = UCT(rootstate=state, itermax=M, verbose=verbose)
        #print("Best Move: " + str(m) + "\n")
        state.DoMove(m)
        if state.stones_remaining == 1 and m == 1:
            print("Player " + str(state.playerJustMoved) + " selects " + str(m) + " stone. " + str(state.stones_remaining) + " stone remaining.")
        elif state.stones_remaining == 1:
            print("Player " + str(state.playerJustMoved) + " selects " + str(m) + " stones. " + str(
                state.stones_remaining) + " stone remaining.")
        elif m == 1:
            print("Player " + str(state.playerJustMoved) + " selects " + str(m) + " stone. " + str(
                state.stones_remaining) + " stones remaining.")
        else:
            print("Player " + str(state.playerJustMoved) + " selects " + str(m) + " stones. " + str(
                state.stones_remaining) + " stones remaining.")

    if state.GetResult(state.playerJustMoved) == 1.0:
        print("Player " + str(state.playerJustMoved) + " wins!")
    elif state.GetResult(state.playerJustMoved) == 0.0:
        print("Player " + str(3 - state.playerJustMoved) + " wins!")


if __name__ == "__main__":
    """ Play a single game to the end using UCT for both players. 
    """
    UCTPlayGame(5, 2, 1000, 15, 6, False)
