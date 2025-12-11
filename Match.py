from game_types import Domino, Tail, Move
from Boneyard import Boneyard
from Player import Player
from Board import Board
from HumanPlayer import HumanPlayer
from MonteCarloPlayer import MonteCarloPlayer
from ExpectiMinimaxPlayer import ExpectiMinimaxPlayer

class Match(): 
    """Class to represent a match between two agents/players
    """

    """
    Match Class
        A match is a single round of the game, consisting of:
        1. A boneyard
        2. Random assignment of player hands until valid
        3. Taking moves in accordance to rules
        4. Determining winner of the match
        5. Score tracking

    """

    # Initialization of a match
    def __init__(self, player_1: Player, player_2: Player, display : bool = True):
        self.player_1 = player_1
        self.player_2 = player_2
        self.board = Board()
        self.boneyard = Boneyard()
        self.display = display

        # Check names, and make them unique
        if player_1.name == player_2.name:
            player_1.name += "_1"
            player_2.name += "_2"

    def valid_hands(self) -> bool:
        """
        Check if hands (all players) are valid (no more than 5 doubles in a single hand)
        Doubles are same-sided tiles
        """
        return self.valid_hand(self.player_1) and self.valid_hand(self.player_2)
    
    def valid_hand(self, player : Player):
        """
        Check if the hand of a single player is valid
        """
        double_count = 0
        for tile in player.get_hand():
            if tile[0] == tile[-1]:
                # If double, add to count
                double_count += 1

        return double_count < 5
    
    def play(self):
        """Game Rules and executing the game
        """
        # Initialize the board and boneyard
        self.board = Board()
        self.boneyard = Boneyard()

        # Each player is dealt a hand
        self.player_1.set_hand(self.boneyard.generate_random_hand())
        self.player_2.set_hand(self.boneyard.generate_random_hand())

        # Repeat until hands are valid
        while not self.valid_hands():
            self.boneyard.restart_boneyard()
            self.player_1.set_hand(self.boneyard.generate_random_hand())
            self.player_2.set_hand(self.boneyard.generate_random_hand())

        # The player with the highest double starts
        # If no player has a double, then the highest numbered
        # Tile goes first
        # Conversation is allowed to find out who is first

        # Order of domino tiles (which tile goes first)
        priority_order : list[Domino] = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 3), (3, 4), (3, 5), (3, 6), (4, 4), (4, 5), (4, 6), (5, 5), (5, 6), (6, 6)]
        
        # Ordering list according to priority rules
        priority_order.sort(key = lambda tile: (tile[0] + tile[-1]) + (100 if tile[0] == tile[-1] else 1), reverse=True)

        # Determine who goes first
        first_player = self.player_1
        second_player = self.player_2
        hand_1 = self.player_1.get_hand()
        hand_2 = self.player_2.get_hand()
        starting_tile = None
        for tile in priority_order:
            if tile in hand_1:
                # If the player 1 has the priority tile, 
                # then player 1 is first (default)
                starting_tile = tile
                break
            elif tile in hand_2:
                # If the player 2 has the priority tile, 
                # then player 2 is first
                first_player = self.player_2
                second_player = self.player_1
                starting_tile = tile
                break
        
        # Make the first move
        self.take_move(first_player, (starting_tile, 0))
        
        # Start the game
        while not self.terminal_state():
            # Second player takes a move
            self.take_turn(second_player)

            # Display board
            if self.display:
                self.board.print_board()

            # Check if terminal
            if self.terminal_state():
                break

            # First player takes a move
            self.take_turn(first_player)

            # Display board
            if self.display:
                self.board.print_board()

        # The winner is the player with the empty and or with the lowest hand score
        # If both players have the same hand score, then it's a tie
        # If a player wins, then the score of the other player is added to their total score
        p1_score = first_player.hand_score()
        p2_score = second_player.hand_score()
        if p1_score < p2_score:
            # First player wins
            first_player.add_score(p2_score)
            if self.display:
                # Show winner and current scores
                print(f"Match Over: {first_player.name} wins")
                print(f"Current Scores -> {first_player.name} : {first_player.score} | {second_player.name} : {second_player.score}")
            return first_player.name
        elif p2_score < p1_score:
            # Second player wins
            second_player.add_score(p1_score)
            if self.display:
                print(f"Match Over: {second_player.name} wins")
                print(f"Current Scores -> {first_player.name} : {first_player.score} | {second_player.name} : {second_player.score}")
            return second_player.name
        else:
            # Tie
            if self.display:
                print("Match Over: Tie")
            return "Tie"
    
    def take_turn(self, player : Player):
        # Choose a move
        move = player.move(self.board, len(self.boneyard.boneyard))

        if move:
            # If there is a move (not None)
            # Then take the move
            self.take_move(player, move)     
        else:
            # If no possible move and the boneyard is not empty
            # Then add new tile from boneyard and check again
            while not self.boneyard.is_boneyard_empty() and move == None:
                new_tile = self.boneyard.generate_random_tile()
                player.add_hand(new_tile)
                move = player.move(self.board, len(self.boneyard.boneyard))
            
            if move:
                # If possible move, then take it
                self.take_move(player, move) 
            else:
                # Pass
                if self.display:
                    print("No possible moves and empty boneyard")

    
    def take_move(self, player : Player, move : Move):
        # Taking a move implies:
        self.board.add_to_board(move) # Adding tile to the board
        player.use_tile(move[0]) #Removing tile from hand

    def terminal_state(self) -> bool:
        if len(self.player_1.get_hand()) == 0 or len(self.player_2.get_hand()) == 0:
            # A match can end if any player has an empty hand
            return True
        elif self.boneyard.is_boneyard_empty() and len(self.player_1.possible_moves(self.board)) == 0 and len(self.player_2.possible_moves(self.board)) == 0:
            # A match can end if the boneyard is empty and none of the players have possible moves
            return True
        else:
            # Else the game is not over
            return False
        






    
    

# Testing Section   
if __name__ == "__main__":
    print("------------------------")
    print("Testing Match Class")
    test_number = int(input("Test #: "))

    if test_number == 1:
        print("Initialization")
        p1 = Player()
        p2 = Player()
        m = Match(p1, p2)
        m.board.print_board()
        print("Boneyard")
        m.boneyard.print_boneyard_tiles()
        print(f"P1: {m.player_1.hand}")
        print(f"P2: {m.player_2.hand}")
        print()

        m.play()
        m.boneyard.print_boneyard_tiles()
        print(f"P1: {m.player_1.hand}")
        print(f"P2: {m.player_2.hand}")
    
    if test_number == 2:
        p1 = HumanPlayer()
        p2 = Player()
        m = Match(p1, p2)
        m.play()
        m.boneyard.print_boneyard_tiles()
        print(f"P1: {m.player_1.hand}")
        print(f"P2: {m.player_2.hand}")

    if test_number == 3:
        p1 = MonteCarloPlayer()
        p2 = Player()
        m = Match(p1, p2)
        m.play()
        m.boneyard.print_boneyard_tiles()
        print(f"P1: {m.player_1.hand}")
        print(f"P2: {m.player_2.hand}")
    
    if test_number == 4:
        p1 = MonteCarloPlayer()
        p2 = Player()
        m = Match(p1, p2, False)
        for i in range(10):
            print(f"\nMatch #{i}")
            m.play()
            m.boneyard.print_boneyard_tiles()
            print(f"P1: {m.player_1.hand}, Score: {m.player_1.score}")
            print(f"P2: {m.player_2.hand}, Score: {m.player_2.score}")
    
    if test_number == 5:
        # Match until score = 200
        p1 = MonteCarloPlayer()
        p2 = Player()
        m = Match(p1, p2, False)
        i = 1
        while p1.score < 200 and p2.score < 200:
            print(f"\nMatch #{i}")
            result = m.play()
            print(f"Result: {result}")
            m.boneyard.print_boneyard_tiles()
            print(f"P1: {m.player_1.hand}, Score: {m.player_1.score}")
            print(f"P2: {m.player_2.hand}, Score: {m.player_2.score}")
            i += 1
        
        print()
        if p1.score >= 200:
            print(f"{p1.name} is the winner")
        else:
            print(f"{p2.name} is the winner")
    
    if test_number == 6:
        # Match until score = 200
        p1 = MonteCarloPlayer(n = 10000)
        p2 = Player()
        m = Match(p1, p2, False)
        i = 1
        while p1.score < 200 and p2.score < 200:
            print(f"\nMatch #{i}")
            result = m.play()
            print(f"Result: {result}")
            m.boneyard.print_boneyard_tiles()
            print(f"P1: {m.player_1.hand}, Score: {m.player_1.score}")
            print(f"P2: {m.player_2.hand}, Score: {m.player_2.score}")
            i += 1
        
        print()
        if p1.score >= 200:
            print(f"{p1.name} is the winner")
        else:
            print(f"{p2.name} is the winner")
    
    if test_number == 7:
        games = 10
        p1_match = 0
        p2_match = 0
        p1_game = 0
        p2_game = 0
        matches = 0
        for j in range(games):
            # Match until score = 200
            p1 = MonteCarloPlayer()
            p2 = Player()
            m = Match(p1, p2, False)
            i = 1
            print(f"\nGame #{j+1}")
            while p1.score < 200 and p2.score < 200:
                matches += 1
                print(f"\nMatch #{i}")
                result = m.play()
                print(f"Result: {result}")
                m.boneyard.print_boneyard_tiles()
                print(f"P1: {m.player_1.hand}, Score: {m.player_1.score}")
                print(f"P2: {m.player_2.hand}, Score: {m.player_2.score}")
                if result == p1.name:
                    p1_match += 1
                if result == p2.name:
                    p2_match += 1
                i += 1

            print()
            if p1.score >= 200:
                print(f"{p1.name} is the winner")
                p1_game += 1
            else:
                print(f"{p2.name} is the winner")
                p2_game += 1
            
        print("\n Match Stats")
        print(f"P1 Match Winning Ratio: {p1_match / matches} after playing {matches} matches")
        print(f"P2 Match Winning Ratio: {p2_match / matches} after playing {matches} matches")

        print("\n Game Stats")
        print(f"P1 Game Winning Ratio: {p1_game / games} after playing {games} games")
        print(f"P2 Game Winning Ratio: {p2_game / games} after playing {games} games")

    if test_number == 8:
        games = 10
        p1_match = 0
        p2_match = 0
        p1_game = 0
        p2_game = 0
        matches = 0
        for j in range(games):
            # Match until score = 200
            p1 = MonteCarloPlayer(n = 3000)
            p2 = Player()
            m = Match(p1, p2, False)
            i = 1
            print(f"\nGame #{j+1}")
            while p1.score < 200 and p2.score < 200:
                matches += 1
                print(f"\nMatch #{i}")
                result = m.play()
                print(f"Result: {result}")
                m.boneyard.print_boneyard_tiles()
                print(f"P1: {m.player_1.hand}, Score: {m.player_1.score}")
                print(f"P2: {m.player_2.hand}, Score: {m.player_2.score}")
                if result == p1.name:
                    p1_match += 1
                if result == p2.name:
                    p2_match += 1
                i += 1

            print()
            if p1.score >= 200:
                print(f"{p1.name} is the winner")
                p1_game += 1
            else:
                print(f"{p2.name} is the winner")
                p2_game += 1
            
        print("\n Match Stats")
        print(f"P1 Match Winning Ratio: {p1_match / matches} after playing {matches} matches")
        print(f"P2 Match Winning Ratio: {p2_match / matches} after playing {matches} matches")

        print("\n Game Stats")
        print(f"P1 Game Winning Ratio: {p1_game / games} after playing {games} games")
        print(f"P2 Game Winning Ratio: {p2_game / games} after playing {games} games")

    if test_number == 9:
        games = 50
        p1_match = 0
        p2_match = 0
        p1_game = 0
        p2_game = 0
        matches = 0
        for j in range(games):
            # Match until score = 200
            p1 = ExpectiMinimaxPlayer()
            p2 = Player()
            m = Match(p1, p2, False)
            i = 1
            print(f"\nGame #{j+1}")
            while p1.score < 200 and p2.score < 200:
                matches += 1
                print(f"\nMatch #{i}")
                result = m.play()
                print(f"Result: {result}")
                m.boneyard.print_boneyard_tiles()
                print(f"P1: {m.player_1.hand}, Score: {m.player_1.score}")
                print(f"P2: {m.player_2.hand}, Score: {m.player_2.score}")
                if result == p1.name:
                    p1_match += 1
                if result == p2.name:
                    p2_match += 1
                i += 1

            print()
            if p1.score >= 200:
                print(f"{p1.name} is the winner")
                p1_game += 1
            else:
                print(f"{p2.name} is the winner")
                p2_game += 1
            
        print("\n Match Stats")
        print(f"P1 Match Winning Ratio: {p1_match / matches} after playing {matches} matches")
        print(f"P2 Match Winning Ratio: {p2_match / matches} after playing {matches} matches")

        print("\n Game Stats")
        print(f"P1 Game Winning Ratio: {p1_game / games} after playing {games} games")
        print(f"P2 Game Winning Ratio: {p2_game / games} after playing {games} games")

    if test_number == 10:
        games = 10
        p1_match = 0
        p2_match = 0
        p1_game = 0
        p2_game = 0
        matches = 0
        for j in range(games):
            # Match until score = 200
            p1 = ExpectiMinimaxPlayer(depth=5)
            p2 = MonteCarloPlayer(n = 1000)
            m = Match(p1, p2, False)
            i = 1
            print(f"\nGame #{j+1}")
            while p1.score < 200 and p2.score < 200:
                matches += 1
                print(f"\nMatch #{i}")
                result = m.play()
                print(f"Result: {result}")
                m.boneyard.print_boneyard_tiles()
                print(f"P1: {m.player_1.hand}, Score: {m.player_1.score}")
                print(f"P2: {m.player_2.hand}, Score: {m.player_2.score}")
                if result == p1.name:
                    p1_match += 1
                if result == p2.name:
                    p2_match += 1
                i += 1

            print()
            if p1.score >= 200:
                print(f"{p1.name} is the winner")
                p1_game += 1
            else:
                print(f"{p2.name} is the winner")
                p2_game += 1
            
        print("\n Match Stats")
        print(f"P1 Match Winning Ratio: {p1_match / matches} after playing {matches} matches")
        print(f"P2 Match Winning Ratio: {p2_match / matches} after playing {matches} matches")

        print("\n Game Stats")
        print(f"P1 Game Winning Ratio: {p1_game / games} after playing {games} games")
        print(f"P2 Game Winning Ratio: {p2_game / games} after playing {games} games")

    print("------------------------")