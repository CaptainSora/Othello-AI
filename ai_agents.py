from itertools import product
from random import choice

from containers import Square, Tile
from game_state import GameState


class Agent:
    def __init__(self, playernumber: int, agentname: str, agenttype: str
            ) -> None:
        self.pnum = playernumber
        self.agentname = agentname
        self.agenttype = agenttype
        self.color = Tile.NONE
    
    def name(self) -> str:
        return self.agentname
    
    def fullname(self) -> str:
        return f"Player {self.pnum}: {self.agentname} ({self.agenttype})"
    
    def set_color(self, tile) -> None:
        self.color = tile

    def _order(self) -> int:
        return self.color.order()
    
    def _score(self, gamestate: GameState) -> int:
        return 0

    # Must be overridden
    def move(self, gamestate: GameState, moveset: dict[tuple[int], GameState]
            ) -> Square:
        return Square(-1, -1)


class Player(Agent):
    def __init__(self, playernumber):
        names = [
            "Roark", "Gardenia", "Maylene", "Crasher Wake", "Fantina",
            "Byron", "Candice", "Volkner"
        ]
        super().__init__(playernumber, f"{choice(names)}", "Human")
    
    def move(self, gamestate, moveset):
        while True:
            user_input = input("Choose a square: ").lower()
            try:
                col = "abcdefgh".index(user_input[0])
                row = "87654321".index(user_input[1])
            except ValueError:
                print("Invalid input. Please enter a square like 'a4'.")
                continue
            if (row, col) in moveset:
                return Square(row, col)
            else:
                print("Illegal move.")


class Level0(Agent):
    def __init__(self, playernumber):
        super().__init__(playernumber, "Magikarp", "Level 0 AI")
    
    def move(self, gamestate, moveset):
        return Square(*choice(list(moveset.keys())))


class Level1(Agent):
    def __init__(self, playernumber):
        super().__init__(playernumber, "Bidoof", "Level 1 AI")
    
    def move(self, gamestate, moveset):
        scores = [
            [gs.count()[self._order()], sq]
            for sq, gs in moveset.items()
        ]
        scores.sort(reverse=True)
        return Square(*scores[0][1])


class Level2(Agent):
    def __init__(self, playernumber):
        super().__init__(playernumber, "Sudowoodo", "Level 2 AI")
    
    def _score(self, gamestate):
        # Center, Edge, Corner
        multiplier = [1, 2, 4]
        total = 0
        for r, c in product(range(8), repeat=2):
            m = multiplier[int(r == 0 or r == 7) + int(c == 0 or c == 7)]
            if gamestate.at(r, c) == self.color:
                total += m
        return total

    def move(self, gamestate, moveset):
        scores = [
            [self._score(gs), sq]
            for sq, gs in moveset.items()
        ]
        scores.sort(reverse=True)
        return Square(*scores[0][1])
