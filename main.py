from Node import *
from NimState import *
from GameSetting import *

def UCT(rootstate, itermax, verbose=False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state=rootstate)

    for i in range(itermax):
        node = rootnode
        state = rootstate.clone()

        # Select
        while node.untried_moves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
            node = node.select_child()
            state.do_move(node.move)

        # Expand
        if node.untried_moves != []:  # if we can expand (i.e. state/node is non-terminal)
            moves = random.choice(node.untried_moves)
            state.do_move(moves)
            node = node.add_child(moves, state)  # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.get_moves() != []:  # while state is non-terminal
            state.do_move(random.choice(state.get_moves()))

        # Backpropagering
        while node != None:  # backpropagate from the expanded node and work back to the root node
            node.update(state.get_result(
                node.player_just_moved))  # state is terminal. Update node with result from POV of node.player_just_moved
            node = node.parentNode

    # Printer informasjon om rollout
    if game_setting.verbose == True:
        print(rootnode.children_to_string())
    return sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move  # return the move that was most visited


def play_game(game_setting):
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).

        Spiller et enkelt spill mellom to spillere
    """
    player_wins = [0,0]
    for i in range(game_setting.G):
        state = NimState(game_setting,game_setting.N)  # uncomment to play Nim with the given number of starting stones
        while (state.get_moves() != []):
            if state.player_just_moved == 1:
                move = UCT(rootstate = state, itermax = game_setting.M, verbose = game_setting.verbose)  # play with values for itermax and verbose = True
            else:
                move = UCT(rootstate = state, itermax = game_setting.M, verbose = game_setting.verbose)
            state.do_move(move)
            if game_setting.verbose == True:
                if move == 1:
                    print("Player " + str(state.player_just_moved) + " selects " + str(move) + " stone. " + "Stones remaining = " + str(state.stones_remaining))
                else:
                    print("Player " + str(state.player_just_moved) + " selects " + str(move) + " stones. " + "Stones remaining = " + str(
                        state.stones_remaining))

        if game_setting.verbose == True:
            if state.get_result(state.player_just_moved) == 1.0:
                print("Player " + str(state.player_just_moved) + " wins" + "\n")
            elif state.get_result(state.player_just_moved) == 0.0:
                print("Player " + str(3 - state.player_just_moved) + " wins" + "\n")

        player_wins[state.player_just_moved - 1] += 1


    print(player_wins)

game_setting = GameSetting()
play_game(game_setting)
