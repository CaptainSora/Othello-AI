from math import log
from itertools import combinations, pairwise

from game_manager import GameManager


def round_robin(players: str, repeat: int) -> tuple[int]:
    """
    Plays each player against the others in a round-robin tournament style
    repeat times. Uses a logistic Elo computation, with level 0 normalized
    to be 100.
    """
    scores = {p: {p: 0 for p in players} for p in players}
    # Replace with combinations(players, r=2) if round robin needed
    for p1, p2 in pairwise(players):
        print(p1 + p2)
        gm = GameManager(silent=True)
        for _ in range(repeat):
            gm.game_start(p1 + p2)
            u1, u2 = 0.5, 0.5
            if gm.winner == 1:
                u1, u2 = 1, 0
            elif gm.winner == 2:
                u1, u2 = 0, 1
            scores[p1][p2] += u1
            scores[p2][p1] += u2
    print(scores['3']['2'])
    # Calculates Elo based on the previous player
    base, scale = 10, 400
    elo = [100]
    for i in range(1, len(players)):
        # 0 < p < 1, enforced via e <= p <= 1 - e
        e = 0.0001
        p = min(max(scores[str(i)][str(i-1)] / repeat, e), 1 - e)
        next_elo = elo[i-1] - scale * log(1/p - 1, base)
        elo.append(next_elo)
    elo = [int(e) for e in elo]
    print(scores)
    print(elo)


if __name__ == "__main__":
    round_robin("0123", repeat=1000)
