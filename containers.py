from dataclasses import dataclass
from enum import Enum
from typing import Self


@dataclass
class Square:
    r: int
    c: int

    def idx(self) -> int:
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
    
    def as_tuple(self) -> tuple:
        return (self.r, self.c)
    
    def as_name(self) -> str:
        return "abcdefgh"[self.c] + "87654321"[self.r]


class Tile(Enum):
    OPEN = 0
    ADJ = 1
    BLACK = 2
    WHITE = 3

    def __str__(self) -> str:
        return " ·OX"[self.value]
    
    def other(self) -> Self:
        return [self.OPEN, self.ADJ, self.WHITE, self.BLACK][self.value]