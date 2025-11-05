import random 

class Boneyard(): 
    """Class to represent the gamestate, boneyard, generate random hands, random tiles from a boneyard
    """

    def __init__(self): 
        self.boneyard = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 3), (3, 4), (3, 5), (3, 6), (4, 4), (4, 5), (4, 6), (5, 5), (5, 6), (6, 6)]

    def generate_random_hand(self):
        """Generates random hand of 7 tiles and removes those tiles from the full boneyard of tiles

        Returns:
            [tuple]: Returns an array of tuples of size 7
        """
        hand = []
        for i in range(7): 
            random_tile = random.choice(self.boneyard)
            self.boneyard.remove(random_tile)
            hand.append(random_tile)
        return hand
    
    def generate_random_tile(self): 
        """Generates a random tile from what is left in the boneyard

        Returns:
            tuple: A singular tile
        """
        if len(self.boneyard) == 0:
            return None
        random_tile = random.choice(self.boneyard)
        self.boneyard.remove(random_tile)
        return random_tile

    def print_boneyard_tiles(self): 
        """Prints the tiles in the boneyard
        """
        print(f"Tiles in Boneyard: {self.boneyard}")

    def is_boneyard_empty(self): 
        """Check if the boneyard is empty

        Returns:
            boolean: return true if boneyard is empty otherwise false
        """
        return len(self.boneyard) == 0 
