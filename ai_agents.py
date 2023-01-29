from itertools import product, takewhile
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

    def move(self, gamestate: GameState, moveset: dict[tuple[int], GameState]
            ) -> Square:
        max_score = - float("inf")
        squares = []
        for sq, gs in moveset.items():
            score = self._score(gs)
            if score > max_score:
                max_score = score
                squares = [sq]
            elif score == max_score:
                squares.append(sq)
        return Square(*choice(squares))


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
    
    def _score(self, gamestate):
        return gamestate.count()[self._order()]


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


class Level3(Agent):
    def __init__(self, playernumber):
        super().__init__(playernumber, "Furret", "Level 3 AI")
    
    def _score(self, gamestate):
        # Static weight evaluation functions found online
        # Counts the triangle going along the edge working inwards
        samsoft = [99, -8, 8, 6, -24, -4, -3, 7, 4, 0]  #909
        uwash = [100, -10, 11, 6, -20, 1, 2, 5, 4, 2]  #898, 882.5
        gatech = [100, -20, 10, 5, -50, -2, -2, -1, -1, -1]  # 853
        nishida = [120, -20, 20, 5, -40, -5, -5, 15, 3, 3]  # 863
        # Compute board score
        total = 0
        for r, c in product(range(8), repeat=2):
            x, y = 3 - int(abs(3.5 - r) - 0.5), 3 - int(abs(3.5 - c) - 0.5)
            p, q = min(x, y), max(x, y)
            idx = 6 - int((3 - p) * (4 - p) / 2) + q
            m = samsoft[idx]  # Change as needed to pick evaluation type
            if gamestate.at(r, c) == self.color:
                total += m
            elif gamestate.at(r, c) == self.color.other():
                total -= m
        return total
