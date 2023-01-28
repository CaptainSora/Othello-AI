from game_state import GameState, Square


"""
TODO:
- End game check
- Legal move dict generator
"""


class InputManager:
    def welcome(self) -> None:
        print("Welcome to Othello.\n")

    def get_console_input(self) -> Square:
        while True:
            user_input = input("Choose a square: ").lower()
            try:
                col = "abcdefgh".index(user_input[0])
                row = "87654321".index(user_input[1])
            except ValueError:
                print("Invalid input. Please enter a square like 'a4'.")
                continue
            else:
                break
        return Square(row, col)


class GameManager:
    def __init__(self) -> None:
        self.gs = GameState()
        self.im = InputManager()
    
    def move(self):
        print(str(self.gs))
        print(f"{str(self.gs.turn)} to move.")
        new_gs = None
        while new_gs is None:
            sq = self.im.get_console_input()
            new_gs = self.gs.move(sq)
            if new_gs is None:
                print("Invalid move.")
        self.gs = new_gs


gm = GameManager()
while True:
    gm.move()
