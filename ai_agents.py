from random import choice

from containers import Square


class Agent:
    def __init__(self, playernumber, agentname, agenttype) -> None:
        self.pnum = playernumber
        self.agentname = agentname
        self.agenttype = agenttype
    
    def name(self) -> str:
        return self.agentname
    
    def fullname(self) -> str:
        return f"Player {self.pnum}: {self.agentname} ({self.agenttype})"

    def move(self, moveset) -> Square:
        pass


class Player(Agent):
    def __init__(self, playernumber) -> None:
        names = [
            "Roark", "Gardenia", "Maylene", "Crasher Wake", "Fantina",
            "Byron", "Candice", "Volkner"
        ]
        super().__init__(playernumber, f"{choice(names)}", "Human")
    
    def move(self, moveset) -> Square:
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
    def __init__(self, playernumber) -> None:
        super().__init__(playernumber, "Magikarp", "Level 0 AI")
    
    def move(self, moveset) -> Square:
        return Square(*choice(list(moveset.keys())))
