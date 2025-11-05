class Player(): 

    def __init__(self, hand: list[tuple]): 
        self.hand = hand

    def get_hand(self): 
        return self.hand