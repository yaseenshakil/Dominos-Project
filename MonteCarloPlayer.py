from Player import Player
from Board import Board
from Boneyard import Boneyard
from game_types import Domino, Move, NUMBER_OF_TILES, ALL_TILES
from copy import deepcopy
from itertools import combinations
import random
from typing import Literal, Self
import numpy as np

# Describe a state in the game
class State():
    def __init__(self, player_hand : list[Domino], opponent_hand : list[Domino], boneyard : Boneyard, board : Board, turn : Literal[0, 1]):
        # A state is described by each player's hand, the boneyard, and the board
        self.player = Player()
        self.player.set_hand(player_hand)
        self.opponent = Player()
        self.opponent.set_hand(opponent_hand)
        self.boneyard : Boneyard = boneyard
        self.board : Board = board

    def transition(self, move : Move | None) -> Self:
        # Return updated state based on the move

        # Based on a copy of the current state
        new_state = deepcopy(self)

        # Handling PASS condition (Move = 0) (No move, and empty boneyard)
        if move != 0:
            if move:
                # Place a tile
                new_state.board.add_to_board(move)
                new_state.player.hand.remove(move[0])
            elif not new_state.boneyard.is_boneyard_empty():
                # Draw from boneyard
                while len(new_state.player.possible_moves(new_state.board)) == 0 and not new_state.boneyard.is_boneyard_empty():
                    new_tile = new_state.boneyard.generate_random_tile()
                    new_state.player.hand.append(new_tile)

        if move or move == 0:
            # The opponent is modeled as a random player
            # The opponent moves if the players makes a move or passes
            op_actions = new_state.opponent.possible_moves(new_state.board)
            if len(op_actions) > 0:
                # Random move
                op_action = random.choice(op_actions)
                new_state.board.add_to_board(op_action)
                new_state.opponent.hand.remove(op_action[0])
            elif not new_state.boneyard.is_boneyard_empty():
                # Draw from boneyard if available
                while len(new_state.opponent.possible_moves(new_state.board)) == 0 and not new_state.boneyard.is_boneyard_empty():
                    new_tile = new_state.boneyard.generate_random_tile()
                    new_state.opponent.hand.append(new_tile)

        return new_state

    def is_terminal(self) -> bool:
        if len(self.player.hand) == 0:
            # A state is terminal if the hand of the player is empty
            return True
        
        elif len(self.opponent.hand) == 0:
            # A state is terminal if the hand of the opponent is empty
            return True
        
        elif self.boneyard.is_boneyard_empty() and len(self.player.possible_moves(self.board)) == 0 and len(self.opponent.possible_moves(self.board)) == 0:
            # A state is terminal if the boneyard is empty and none of the players have possible moves
            return True
        
        else:
            return False
    
    def utility(self) -> int:
        # The utility denpends on the total score of each player's hand
        player_score = self.player.hand_score()
        opponent_score = self.opponent.hand_score()

        if player_score < opponent_score:
            # If the player has a lower scored hand
            # The player wins and gets the opponent's hand
            # as their score
            return opponent_score
        elif opponent_score < player_score:
            # If the player has a higher scored hand
            # The player loses and the opponent gets the
            # players hand as their score
            return -player_score
        else:
            # No utility in a tie
            return 0

    def possible_actions(self) -> list[Move | None | Literal[0]]:
        # The possible actions from a given state are:

        # The possible moves, if any
        actions = self.player.possible_moves(self.board)
        if len(actions) == 0 and not self.boneyard.is_boneyard_empty():
            # If no moves possible, and drawing is available 
            actions = [None]
        if len(actions) == 0 and not self.is_terminal():
            # If no moves possible, and the boneyard is empty
            # Also not a terminal state
            actions = [0]
        return actions
    
# Node in a Monte Carlo Tree
class Node():
    def __init__(self):
        self.parent : Node = None # Parent node
        self.action = None # Action that caused that produced the node
        self.visit_count = 0 # Number of times a node is visited
        self.total_reward = 0 # Sum of utilities
        self.availability = 0 # Number of alternative nodes available for selection
        self.children : list[Node] = [] # List of children
        self.d : State = None # Determinization of the corresponding node
    
    def c(self, d : State) -> list[Self]:
        # Children of node b compatible with determinization
        actions = d.possible_actions()
        return [child for child in self.children if child.action in actions]

    def u(self, d : State) -> list[Move | None | Literal[0]]:
        # List of possible unexplored actions from a node given a determinization 

        # Possible actions
        actions = d.possible_actions()

        # Explored actions
        expanded_actions = [child.action for child in self.children]

        # Unexplored actions
        unexplored_actions = [a for a in actions if a not in expanded_actions]
    
        return unexplored_actions

class MonteCarloPlayer(Player):
    def __init__(self, name : str = "MonteCarloPlayer", n : int = 1000, c : float = 0.7):
        super().__init__(name) 

        # Number of MCTS iterations
        self.MCTS_N = n

        # Exploration constant
        self.MCTS_C = c

    def move(self, board : Board, boneyard_size : int) -> Move | None:
        # Possible moves
        moves = self.possible_moves(board)

        # If no possible move, return None
        if not moves:
            return None
        
        # If only one move, make that move
        if len(moves) == 1:
            return moves[0]
        
        # If more than 1 option, run Single Observer Information Set Monte Carlo Tree Search (SO-ISMCTS)

        # Determine the list of possible determinizations
        determinizations = self.possible_determinizations(board, boneyard_size)

        # Create single-node tree
        v0 = Node() # Root

        # Repeat the following over the number of set iterations
        for _ in range(self.MCTS_N):
            # Select a random determinization
            d0 = random.choice(determinizations)

            # Select a node from the tree
            v, d = self.select(v0, d0)

            # If possible, expand the node
            if len(v.u(d)) > 0:
                v, d = self.expand(v, d)
            
            # Simulate with determinization
            # Calculate utility
            r = self.simulate(d)

            # Backpropagate utility through the tree
            self.backpropagate(r, v)
        
        # From the children of the root node
        # The action that creates the child with the most visits
        # is the chosen move
        children = v0.children
        n = np.asarray([c.visit_count for c in children])
        move = children[np.argmax(n)].action

        return move
        
    
    def select(self, v : Node, d : State) -> tuple[Node, State]:
        # Node selection

        while not d.is_terminal() and len(v.u(d)) == 0:
            # List of children
            children = v.c(d)
            values = []

            # UCB calculatation for each child
            for c in children:
                value = c.total_reward / c.visit_count + 0.7 * np.sqrt(np.log(c.availability) / c.visit_count)
                values.append(value)
            
            # A child with the best UCB is chosen as the new node
            values = np.asarray(values)
            idx = np.argmax(values)
            v = children[idx]

            # A new determinization (state) is obtained from
            # Applying the action of that child
            d = d.transition(children[idx].action)

            # Repeat until the no unexplored actions in the chosen node or terminal state
        
        # Return the selected node
        return v, d

    def expand(self, v : Node, d : State) -> tuple[Node, State]:
        # Node expansion

        # Choose a random action
        a = random.choice(v.u(d))

        # Definition of the child node 
        # with action and determinization
        w = Node()
        w.parent = v
        w.action = a
        w.d = d

        # Child is added to the children list
        v.children.append(w)

        # Determinization is updated
        d = d.transition(a)

        # Return child of the expanded node
        return w, d
    
    def simulate(self, d : State) -> int:
        # Simulate with random actions until terminal state
        while not d.is_terminal():
            actions = d.possible_actions()
            if actions:
                a = random.choice(actions)
                d = d.transition(a)
            else:
                d = d.transition(None)
        # Return the utility of the simulated terminal state
        return d.utility()
    
    def backpropagate(self, r : int, v_l : Node):
        # Starting from the given node
        v = v_l

        while v.parent:
            # Backpropagate to the ancestors until reaching root node
            v.visit_count += 1 # Add visit count
            v.total_reward += r # Add utility to total reward

            # Add availability to siblings compatible with determinization
            children = v.parent.c(v.d)
            for c in children: 
                c.availability += 1

            # Move to next ancestor
            v = v.parent
        
        # Updating Root node
        v.visit_count += 1
        v.total_reward += r
        v.availability += 1

    def possible_determinizations(self, board : Board, boneyard_size : int) -> list[State]:
        # Initial list of dominos that might be on the boneyard or the opponent hand
        initial_list : list[Domino] = []

        for tile in ALL_TILES:
            # Adding tiles that are not in the player's hand or the board
            if tile not in self.get_hand() and tile not in board.get_board_tiles():
                # They cannot appear in reverse either
                reverse = (tile[-1], tile[0])
                if reverse not in self.get_hand() and reverse not in board.get_board_tiles():
                    # Given that they do not have the certainties
                    initial_list.append(tile)
        
        # Number of tiles the opponent
        opponent_n : int = NUMBER_OF_TILES - len(board.board) - boneyard_size - len(self.get_hand())

        # The set of possible hands is every combination of of the initial list with 
        possible_hands : list[list[Domino]] = []
        for combo in combinations(initial_list, opponent_n):
            possible_hands.append(list(combo))

        # Set of possible determinizations
        possible_d : list[State] = []

        # For each possible opponent hand
        for hand in possible_hands:
            # Determine the boneyard
            boneyard_list: list[Domino] = []
            
            # The remaining tiles
            for tile in initial_list:
                if tile not in hand:
                    boneyard_list.append(tile)

            # Make it into a boneyard object
            boneyard = Boneyard()
            boneyard.boneyard = boneyard_list

            # Define the state (Turn is always for the player for the determinization list)
            new_state = State(self.hand, hand, boneyard, board, 0)
            
            # Add state to possible state determinizations
            possible_d.append(new_state)

        return possible_d


# Testing Section   
if __name__ == "__main__":
    print("------------------------")
    print("Testing Player Class")
    player = MonteCarloPlayer()
    player2 = Player()
    boneyard = Boneyard()
    board = Board()
    player.set_hand(boneyard.generate_random_hand())
    player2.set_hand(boneyard.generate_random_hand())
    user = " "
    while len(player.possible_moves(board)) > 0:
        print("Hand")
        print(player.get_hand())
        
        moves = player.possible_moves(board)
        print(f"Possible moves {moves}")
        
        move = player.move(board, len(boneyard.boneyard))
        print(f"Player 1 Selects {move}")

        board.add_to_board(move)
        player.use_tile(move[0])

        print("Board")
        board.print_board()

        move = player2.move(board, len(boneyard.boneyard))
        print(f"Player 2 Selects {move}")

        board.add_to_board(move)
        player2.use_tile(move[0])

        print("Board")
        board.print_board()

        input("NEXT")
        
    else:
        print("No more moves")
    print("Remaining hand")
    print(player.get_hand())
    print("------------------------")