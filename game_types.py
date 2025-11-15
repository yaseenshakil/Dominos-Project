from typing import Literal

# Domino alias
Domino = tuple[int, int]
Tail = Literal[-1, 0]
Move = tuple[Domino, Tail]