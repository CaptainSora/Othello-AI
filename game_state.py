from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Self
from itertools import product


class Tile(Enum):
    OPEN = 0
    ADJ = 1
    BLACK = 2
    WHITE = 3

    def __str__(self) -> str:
        return " ·OX"[self.value]
    
    def other(self) -> Self:
        return [self.OPEN, self.ADJ, self.WHITE, self.BLACK][self.value]


@dataclass
class Square:
    r: int
    c: int

    def num(self) -> int:
        return 8 * self.r + self.c
    
    def add(self, other: Self) -> None:
        self.r += other.r
        self.c += other.c
    
    def invert(self) -> None:
        self.r *= -1
        self.c *= -1
    
    def valid(self) -> bool:
        return (0 <= self.r <= 7) and (0 <= self.c <= 7)
    
    def copy(self) -> Self:
        return Square(self.r, self.c)


@dataclass
class Arrow:
    loc: Square
    dir: Square
    flip: bool = False

    def move(self) -> Self:
        self.loc.add(self.dir)
        return self
    
    def valid(self) -> bool:
        return self.loc.valid()
    
    def bounce(self) -> None:
        self.dir.invert()
        self.flip = True


class GameState:
    def __init__(self, grid: list[Tile] = [], turn: Tile = Tile.BLACK) -> None:
        self.turn = turn
        self.grid = grid[:]
        if not grid:
            for i in range(64):
                tile = Tile.OPEN
                if i in [27, 36]:
                    tile = Tile.WHITE
                elif i in [28, 35]:
                    tile = Tile.BLACK
                elif 2 <= i // 8 <= 5 and 2 <= i % 8 <= 5:
                    tile = Tile.ADJ
                self.grid.append(tile)
    
    def __str__(self) -> str:
        board = " #--------#\n"
        for i in range(8):
            board += f"{8-i}|"
            board += "".join([str(t) for t in self.grid[8*i:8*i+8]])
            board += "|\n"
        board += " #--------#\n"
        board += "  abcdefgh "
        return board
    
    def copy(self) -> Self:
        return GameState(self.grid, self.turn)
    
    def new_adjacent(self, sq: Square) -> None:
        for r, c in product([-1, 0, 1], repeat=2):
            d = Square(sq.r - r, sq.c - c)
            if d.valid() and self.grid[d.num()] == Tile.OPEN:
                self.grid[d.num()] = Tile.ADJ

    def move(self, sq: Square) -> Self | None:
        # Validate input
        try:
            if self.grid[sq.num()] != Tile.ADJ:
                return None
        except IndexError:
            print("Invalid location!")
            return None
        # Create next board state
        gs = self.copy()
        gs.grid[sq.num()] = gs.turn
        gs.new_adjacent(sq)
        gs.turn = gs.turn.other()
        arrows = deque([
            Arrow(sq.copy(), Square(x, y))
            for x, y in product([-1, 0, 1], repeat=2)
            if x != 0 or y != 0
        ])
        # Flip disks
        flipped = False
        while arrows:
            a = arrows.popleft()
            if a.move().valid():
                if a.loc == sq:
                    # Returned to start
                    continue
                elif gs.grid[a.loc.num()] == self.turn.other():
                    # Passthrough, flip if reversed
                    if a.flip:
                        gs.grid[a.loc.num()] = gs.grid[a.loc.num()].other()
                        flipped = True
                elif gs.grid[a.loc.num()] == self.turn:
                    # Reflect, should only reach this at most once
                    a.bounce()
                else:
                    # Reached empty cell
                    continue
                arrows.appendleft(a)
        # Validate move
        if flipped:
            return gs
        else:
            return None
