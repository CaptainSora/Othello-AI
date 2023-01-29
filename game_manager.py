from itertools import product
from random import shuffle

from ai_agents import Agent, Player, Level0
from containers import Square, Tile
from game_state import GameState


"""
TODO:
"""


class InputManager:
    def welcome(self) -> None:
        print("Welcome to Othello.\n")
    
    def select_players(self) -> dict[Tile, Agent]:
        playerdict = {
            "p": {
                "desc": "Player (via console)",
                "constructor": Player
            },
            "0": {
                "desc": "Level 0 AI (random move)",
                "constructor": Level0
            },
        }
        print("Who's playing?")
        for k, v in playerdict.items():
            print(f"  {k}: {v['desc']}")
        
        while True:
            user_input = input("Please enter two characters: ")
            user_input = user_input.strip().replace(" ", "").lower()
            if len(user_input) != 2:
                print("Please enter exactly two characters.")
            elif user_input[0] not in playerdict:
                print(f"Sorry, I couldn't recognize '{user_input[0]}'.")
            elif user_input[1] not in playerdict:
                print(f"Sorry, I couldn't recognize '{user_input[1]}'.")
            else:
                break
        
        playerlist = [
            playerdict[user_input[0]]['constructor'](1),
            playerdict[user_input[1]]['constructor'](2)
        ]
        shuffle(playerlist)
        players = dict(zip([Tile.BLACK, Tile.WHITE], playerlist))
        for t, p in players.items():
            print(f"{str(t)} - {p.fullname()}")
        
        return players


class GameManager:
    def __init__(self) -> None:
        self.gs = GameState()
        self.im = InputManager()
        self.players = {}
        self.prevskip = False
        self.active = False
        self.moveset = {}
    
    def _find_legal_moves(self):
        """
        Generates and saves a dictionary of all legal moves for the next
        player.
        """
        self.moveset.clear()
        for r, c in product(range(8), repeat=2):
            sq = Square(r, c)
            if self.gs.grid[sq.idx()] != Tile.ADJ:
                continue
            new_gs = self.gs.move(sq)
            if new_gs is not None:
                self.moveset[(r, c)] = new_gs
    
    def print_board_to_console(self):
        board = " #--------#\n"
        for r in range(8):
            board += f"{8-r}|"
            board += "".join([
                '+' if (r, c) in self.moveset else str(self.gs.grid[8*r+c])
                for c in range(8)
                # str(t) for t in self.grid[8*i:8*i+8]
            ])
            board += "|\n"
        board += " #--------#\n"
        board += "  abcdefgh "
        print(board)
    
    def move(self):
        self._find_legal_moves()
        self.print_board_to_console()
        turn = self.gs.turn
        print(f"{str(turn)} - {self.players[turn].name()}'s turn.")
        # Check for legal moves
        if not self.moveset:
            print(f"No legal moves for {str(turn)}.")
            if self.prevskip:
                self._game_end()
            self.prevskip = True
            return
        self.prevskip = False
        # Print legal moves
        print(
            "Legal moves: " + 
            ", ".join([
                "abcdefgh"[sq[1]] + "87654321"[sq[0]]
                for sq in self.moveset
            ])
        )
        # Get agent move
        sq = self.players[turn].move(self.moveset)
        print(f"{self.players[turn].name()} played {sq.as_name()}.")
        self.gs = self.moveset[sq.as_tuple()]
        if self.gs.placed >= 64:
            self._game_end()
    
    def game_start(self):
        self.active = True
        self.im.welcome()
        self.players = self.im.select_players()
        self._game_handler()
    
    def _game_end(self):
        self.active = False
        print("Game over!")
        black, white = self.gs.count()
        print(f"{str(Tile.BLACK)}: {black}")
        print(f"{str(Tile.WHITE)}: {white}")
        if black == white:
            print(f"=== The game is a draw! ===")
        else:
            winner = Tile.BLACK if black > white else Tile.WHITE
            print(
                f"=== {str(winner)} - {self.players[winner].name()} wins! ==="
            )
    
    def _game_handler(self):
        while self.active:
            self.move()


gm = GameManager()
gm.game_start()