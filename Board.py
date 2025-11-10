class Board(): 
    
    def __init__(self):
        self.board = []

    def add_to_board(self, move: tuple[tuple[int, int], int]): 
        if (move[-1] != -1 or move[-1] != 0): 
            raise TypeError(f"Invalid Move Provided to add_to_board function: {move}")
        else: 
            self.board.insert(move[-1], move[0])

    def print_board(self): 
        print(f"------Domino Board--------\n {self.board}\n")
    
    def get_board_tiles(self): 
        return self.board
    
