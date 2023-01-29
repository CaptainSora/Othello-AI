from collections import deque
from dataclasses import dataclass
from typing import Self
from itertools import product

from containers import Square, Tile


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
    def __init__(self, grid: list[Tile] = [], turn: Tile = Tile.BLACK, 
            placed: int = 4) -> None:
        self.turn = turn
        self.grid = grid[:]
        self.placed = placed
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
    
    def copy(self) -> Self:
        return GameState(self.grid, self.turn, self.placed)
    
    def at(self, r: int, c: int) -> Tile:
        return self.grid[Square(r, c).idx()]
    
    def count(self) -> tuple[int]:
        return (self.grid.count(Tile.BLACK), self.grid.count(Tile.WHITE))
    
    def _new_adjacent(self, sq: Square) -> None:
        for r, c in product([-1, 0, 1], repeat=2):
            d = Square(sq.r - r, sq.c - c)
            if d.valid() and self.grid[d.idx()] == Tile.OPEN:
                self.grid[d.idx()] = Tile.ADJ

    def move(self, sq: Square) -> Self | None:
        # Validate input
        try:
            if self.grid[sq.idx()] != Tile.ADJ:
                return None
        except IndexError:
            print("Invalid location!")
            return None
        # Create next board state
        gs = self.copy()
        gs.grid[sq.idx()] = gs.turn
        gs._new_adjacent(sq)
        gs.turn = gs.turn.other()
        gs.placed += 1
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
                elif gs.grid[a.loc.idx()] == self.turn.other():
                    # Passthrough, flip if reversed
                    if a.flip:
                        gs.grid[a.loc.idx()] = gs.grid[a.loc.idx()].other()
                        flipped = True
                elif gs.grid[a.loc.idx()] == self.turn:
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
