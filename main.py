from Node import *
from NimState import *
from GameSetting import *




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


def UCTPlayGame(game_setting):
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    #game_setting = GameSetting(G,P,M,N,K,verbose)
    
    state = NimState(game_setting)  # uncomment to play Nim with the given number of starting stones
    while (state.GetMoves() != []):
        #print(str(state))
        #print("test")
        if state.playerJustMoved == 1:
            m = UCT(rootstate = state, itermax = game_setting.M, verbose = game_setting.verbose)  # play with values for itermax and verbose = True
        else:
            m = UCT(rootstate = state, itermax = game_setting.M, verbose = game_setting.verbose)
        #print("Best Move: " + str(m) + "\n")
        state.DoMove(m)
        if m == 1:
            print("Player " + str(state.playerJustMoved) + " selects " + str(m) + " stone. " + "Stones remaining = " + str(state.stones_remaining))
        else:
            print("Player " + str(state.playerJustMoved) + " selects " + str(m) + " stones. " + "Stones remaining = " + str(
                state.stones_remaining))

    if state.GetResult(state.playerJustMoved) == 1.0:
        print("Player " + str(state.playerJustMoved) + " wins")
    elif state.GetResult(state.playerJustMoved) == 0.0:
        print("Player " + str(3 - state.playerJustMoved) + " wins")

game_setting = GameSetting.GameSetting()
UCTPlayGame(game_setting)
