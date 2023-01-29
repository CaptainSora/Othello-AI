from itertools import product
from random import shuffle

from ai_agents import Agent, Player, Level0, Level1, Level2
from containers import Square, Tile
from game_state import GameState


"""
TODO:
"""


class InputManager:
    def __init__(self, silent: bool = False) -> None:
        self.silent = silent
        self.playerdict = {
            "p": {
                "desc": "Player (via console)",
                "constructor": Player
            },
            "0": {
                "desc": "Level 0 AI (random move)",
                "constructor": Level0
            },
            "1": {
                "desc": "Level 1 AI (most tiles)",
                "constructor": Level1
            },
            "2": {
                "desc": "Level 2 AI (weighted most tiles)",
                "constructor": Level2
            },
        }
    
    def print(self, output) -> None:
        if not self.silent:
            print(output)
    
    def welcome(self) -> None:
        self.print("Welcome to Othello.\n")
    
    def select_players(self) -> dict[Tile, Agent]:
        print("Who's playing?")
        for k, v in self.playerdict.items():
            print(f"  {k}: {v['desc']}")
        
        while True:
            user_input = input("Please enter two characters: ")
            user_input = user_input.strip().replace(" ", "").lower()
            if len(user_input) != 2:
                print("Please enter exactly two characters.")
            elif user_input[0] not in self.playerdict:
                print(f"Sorry, I couldn't recognize '{user_input[0]}'.")
            elif user_input[1] not in self.playerdict:
                print(f"Sorry, I couldn't recognize '{user_input[1]}'.")
            else:
                break
        return self.create_players(user_input)
    
    def create_players(self, players: str) -> dict[Tile, Agent]:
        playerlist = [
            self.playerdict[players[0]]['constructor'](1),
            self.playerdict[players[1]]['constructor'](2)
        ]
        shuffle(playerlist)

        players = dict(zip([Tile.BLACK, Tile.WHITE], playerlist))
        for t, p in players.items():
            p.set_color(t)
            self.print(f"{str(t)} - {p.fullname()}")
        
        return players


class GameManager:
    def __init__(self, silent: bool = False) -> None:
        self.gs = GameState()
        self.im = InputManager(silent)
        self.silent = silent
        self.players = {}
        self.prevskip = False
        self.active = False
        self.moveset = {}
    
    def print(self, output: str) -> None:
        if not self.silent:
            print(output)
        
    def print_board_to_console(self) -> None:
        board = " #--------#\n"
        for r in range(8):
            board += f"{8-r}|"
            board += "".join([
                '+' if (r, c) in self.moveset else str(self.gs.at(r, c))
                for c in range(8)
            ])
            board += "|\n"
        board += " #--------#\n"
        board += "  abcdefgh "
        self.print(board)
    
    def move(self) -> None:
        self.moveset = self.gs.get_legal_moves()
        self.print_board_to_console()
        turn = self.gs.turn
        self.print(f"{str(turn)} - {self.players[turn].name()}'s turn.")
        # Check for legal moves
        if not self.moveset:
            self.print(f"No legal moves for {str(turn)}.")
            if self.prevskip:
                self._game_end()
            self.prevskip = True
            self.gs.turn = self.gs.turn.other()
            return
        self.prevskip = False
        # Print legal moves
        self.print(
            "Legal moves: " + 
            ", ".join([
                "abcdefgh"[sq[1]] + "87654321"[sq[0]]
                for sq in self.moveset
            ])
        )
        # Get agent move
        sq = self.players[turn].move(self.gs, self.moveset)
        self.print(f"{self.players[turn].name()} played {sq.as_name()}.")
        self.gs = self.moveset[sq.as_tuple()]
        if self.gs.placed >= 64:
            self._game_end()
    
    def game_start(self) -> None:
        self.active = True
        self.im.welcome()
        self.players = self.im.select_players()
        self._game_handler()
    
    def _game_end(self) -> None:
        self.active = False
        self.print("Game over!")
        black, white = self.gs.count()
        self.print(f"{str(Tile.BLACK)}: {black}")
        self.print(f"{str(Tile.WHITE)}: {white}")
        if black == white:
            self.print(f"=== The game is a draw! ===")
        else:
            winner = Tile.BLACK if black > white else Tile.WHITE
            self.print(
                f"=== {str(winner)} - {self.players[winner].name()} wins! ==="
            )
    
    def _game_handler(self) -> None:
        while self.active:
            self.move()


gm = GameManager()
gm.game_start()