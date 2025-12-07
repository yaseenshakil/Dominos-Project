from Player import Player
from Board import Board
from Boneyard import Boneyard
from game_types import Domino, Move, NUMBER_OF_TILES, ALL_TILES
from copy import deepcopy
from itertools import combinations
import random
from typing import Literal, Self
import numpy as np

 
class State():
    def __init__(self, player_hand : list[Domino], opponent_hand : list[Domino], boneyard : Boneyard, board : Board, turn : Literal[0, 1]):
        self.player = Player()
        self.player.set_hand(player_hand)
        self.opponent = Player()
        self.opponent.set_hand(opponent_hand)
        self.boneyard : Boneyard = boneyard
        self.board : Board = board

    def transition(self, move : Move | None) -> Self:
        # Return updated state based on the move
        new_state = deepcopy(self)

        if move != 0:
            # Handling PASS condition
            if move:
                new_state.board.add_to_board(move)
                new_state.player.hand.remove(move[0])
            elif not new_state.boneyard.is_boneyard_empty():
                new_tile = new_state.boneyard.generate_random_tile()
                new_state.player.hand.append(new_tile)

        op_actions = new_state.opponent.possible_moves(new_state.board)
        if len(op_actions) > 0:
            op_action = random.choice(op_actions)
            new_state.board.add_to_board(op_action)
            new_state.opponent.hand.remove(op_action[0])
        elif not new_state.boneyard.is_boneyard_empty():
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
        player_score = self.player.hand_score()
        opponent_score = self.opponent.hand_score()
        if player_score < opponent_score:
            return opponent_score
        elif opponent_score < player_score:
            return -player_score
        else:
            return 0

    def possible_actions(self) -> list[Move | None | Literal[0]]:
        actions = self.player.possible_moves(self.board)
        if len(actions) == 0 and not self.boneyard.is_boneyard_empty():
            actions = [None]
        if len(actions) == 0 and not self.is_terminal():
            actions = [0]
        return actions
    

class Node():
    def __init__(self):
        self.parent : Node = None
        self.action = None
        self.visit_count = 0
        self.total_reward = 0
        self.availability = 0
        self.children : list[Node] = []
        self.d : State = None
    
    def c(self, d : State) -> list[Self]:
        actions = d.possible_actions()
        return [child for child in self.children if child.action in actions]

    def u(self, d : State) -> list[Move | None | Literal[0]]:
        # List of possible actions from a node given a determinization
        actions = d.possible_actions()

        expanded_actions = [child.action for child in self.children]

        unexplored_actions = [a for a in actions if a not in expanded_actions]
        
        return unexplored_actions

class MonteCarloPlayer(Player):
    def __init__(self, name : str = "MonteCarloPlayer", n : int = 1000, c : float = 0.7):
        super().__init__(name) 

        # Last board after making a move
        self.last_board : Board = Board()

        # Last boneyard after making a move
        self.last_boneyard_size : int = 14

        # Last non-tile certainties (List of numbers from 0-6 it is certain that the opponent does not have)
        self.certainties : list[int] = []

        # Last length of player's hand
        self.last_hand_size : int = 0

        # Number of MCTS iterations
        self.MCTS_N = n

        # Exploration constant
        self.MCTS_C = c

    def record_last_state(self, board : Board, boneyard_size : int):
        # Record last board and boneyard size
        self.last_board = board
        self.last_boneyard_size = boneyard_size
        self.last_hand_size = len(self.hand)

    def move(self, board : Board, boneyard_size : int) -> Move | None:
        # Update certainties with every move
        self.update_certainty(board, boneyard_size)

        # Possible moves
        moves = self.possible_moves(board)

        # If no possible move, return None
        if not moves:
            # Board stays the same, but boneyard decreases if possible
            self.record_last_state(deepcopy(board), boneyard_size - 1 if boneyard_size > 0 else boneyard_size)
            return None
        
        # If only one move, make that move
        if len(moves) == 1:
            # Board gets updated by the move
            new_board = deepcopy(board)
            new_board.add_to_board(moves[0])
            self.record_last_state(new_board, boneyard_size)
            return moves[0]
        
        # If more than 1 option, run MCTS

        # Determine the list of possible determinizations
        determinizations = self.possible_determinizations(board, boneyard_size)

        # Create single-node tree
        v0 = Node() # Root

        # Repeat the following over the number of set iterations
        for _ in range(self.MCTS_N):
            # Select a random determinization
            d0 = random.choice(determinizations)

            v, d = self.select(v0, d0)
            if len(v.u(d)) > 0:
                v, d = self.expand(v, d)
            r = self.simulate(d)
            self.backpropagate(r, v, d)
        
        children = v0.children
        n = np.asarray([c.visit_count for c in children])
        move = children[np.argmax(n)].action

        # When a move is selected, the board changes are recorded
        new_board = deepcopy(board)
        new_board.add_to_board(move)
        self.record_last_state(new_board, boneyard_size)
        return move
        
    
    def select(self, v : Node, d : State) -> tuple[Node, State]:
        while not d.is_terminal() and len(v.u(d)) == 0:
            # List of children
            children = v.c(d)
            values = []
            for c in children:
                value = c.total_reward / c.visit_count + 0.7 * np.sqrt(np.log(c.availability) / c.visit_count)
                values.append(value)
            
            values = np.asarray(values)
            idx = np.argmax(values)
            v = children[idx]
            d = d.transition(children[idx].action)
        return v, d

    def expand(self, v : Node, d : State) -> tuple[Node, State]:
        a = random.choice(v.u(d))

        w = Node()
        w.parent = v
        w.action = a
        w.d = d

        v.children.append(w)
        d = d.transition(a)

        return w, d
    
    def simulate(self, d : State) -> int:
        while not d.is_terminal():
            actions = d.possible_actions()
            if actions:
                a = random.choice(actions)
                d = d.transition(a)
            else:
                d = d.transition(None)

        return d.utility()
    
    def backpropagate(self, r : int, v_l : Node, d0 : State):
        v = v_l
        while v.parent:
            v.visit_count += 1
            v.total_reward += r
            children = v.parent.c(v.d)
            for c in children: 
                c.availability += 1
            v = v.parent
        
        # Root node
        v.visit_count += 1
        v.total_reward += r
        v.availability += 1

    
    def update_certainty(self, board : Board, boneyard_size : int):
        # Determine tile numbers that the opponent does not have

        # This also initializes if another match starts
        # If the board has less tiles than the last checkpoint,
        # Then another match has started
        if len(board.get_board_tiles()) < len(self.last_board.get_board_tiles()):
            # Checkpoints and certainty initialization
            self.last_board : Board = Board()
            self.last_boneyard_size : int = 14
            self.last_hand_size : int = 0
            self.certainties : list[int] = []

        
        # How much has the board changed? What tiles have been added?
        added_tiles : list[Domino] = []
        for tile in board.get_board_tiles():
            if tile not in self.last_board.get_board_tiles():
                added_tiles.append(tile)
        
        # How much has the boneyard changed?
        boneyard_diff = self.last_boneyard_size - boneyard_size

        # How much has the player's hand changed?
        hand_diff = len(self.hand)  - self.last_hand_size

        # Certainties are only updated if the call is not a result 
        # of drawing from the boneyard. That is, the board has not 
        # changed, the boneyard has decreased, and the players hand
        # has increased

        if not (boneyard_diff > 0 and hand_diff > 0):
            # If the board has changed less than the boneyard,
            # forget every certainty
            if boneyard_diff > len(added_tiles):
                self.certainties = []

            # If the board, then it is certain 
            # that the opponent does not have the ends of the board
            if len(added_tiles) == 0 and len(board.get_board_tiles()) > 0:
                (end_1, end_2) = board.get_tails()
                if end_1 not in self.certainties:
                    self.certainties.append(end_1)
                if end_2 not in self.certainties:
                    self.certainties.append(end_2)
            
            # If the board and the boneyard change by exactly one, it is
            # certain theat the opponent does not have the unplayed end, 
            # nor the end before played tile (ends of the old board)
            if len(added_tiles) == 1 and boneyard_diff == 1:
                (end_1, end_2) = self.last_board.get_tails()
                if end_1 not in self.certainties:
                    self.certainties.append(end_1)
                if end_2 not in self.certainties:
                    self.certainties.append(end_2)

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
                    #if tile[0] not in self.certainties and tile[1] not in self.certainties :
                    # Testing without the certainties
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