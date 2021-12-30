from collections import Counter, defaultdict, deque
from functools import lru_cache
from typing import (
    List,
    Tuple,
    Set,
    Dict,
    Iterable,
    DefaultDict,
    Optional,
    Union,
    Generator,
)
from copy import deepcopy
import re
from math import floor, ceil
from itertools import permutations, product


class Player:
    def __init__(self, start_position, board_size):
        self.pos: int = start_position
        self.score: int = 0
        self.board_len: int = board_size

    def move(self, n):
        self.pos = (self.pos + n) % (self.board_len)
        if self.pos == 0:
            self.pos = 10
        self.score += self.pos


STATES: Dict[Tuple[int, int, int, int, int], Tuple[int, int]] = {}


def parse(filename: str) -> List[Player]:
    with open(filename, "r") as f:
        data = f.read().strip()

    players = []
    for player in data.split("\n"):
        start = int(re.findall("\d+", player)[1])
        players.append(Player(start, 10))
    return players


def play_game(players: List[Player], dice_size: int) -> int:
    player1, player2 = players

    i = 1 % dice_size
    while True:
        move = (i % dice_size) + (i + 1) % dice_size + (i + 2) % dice_size
        player1.get_new_states(move)
        if player1.score >= 1000:
            winner = 1
            break
        i += 3
        move = (i % dice_size) + (i + 1) % dice_size + (i + 2) % dice_size
        player2.get_new_states(move)
        if player2.score >= 1000:
            winner = 2
            break
        i += 3

    loser_score = player1.score if winner == 2 else player2.score
    return (i + 2) * loser_score


def play_game_p2(
    players: List[Player], ways_to_move_k: Counter, is_moving: int = 1
) -> Tuple[int, int]:
    global STATES
    player1, player2 = players
    if player1.score >= 21:
        return 1, 0
    if player2.score >= 21:
        return 0, 1

    state = (player1.score, player1.pos, player2.score, player2.pos, is_moving)

    if state in STATES:
        return STATES[state]

    state_wins = [0, 0]
    for move in ways_to_move_k:
        if is_moving == 1:
            p1_copy = deepcopy(player1)
            p1_copy.get_new_states(move)
            wins1, wins2 = play_game_p2(
                [deepcopy(p1_copy), deepcopy(player2)],
                ways_to_move_k,
                is_moving=2,
            )
        else:
            p2_copy = deepcopy(player2)
            p2_copy.get_new_states(move)
            wins1, wins2 = play_game_p2(
                [deepcopy(player1), deepcopy(p2_copy)],
                ways_to_move_k,
                is_moving=1,
            )
        state_wins[0] += ways_to_move_k[move] * wins1
        state_wins[1] += ways_to_move_k[move] * wins2
    STATES[state] = (state_wins[0], state_wins[1])
    return STATES[state]


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    # p1
    players = parse(filename)
    score_a = play_game(players, dice_size=100)
    print()
    answer_a = score_a
    global STATES
    STATES = {}
    players = parse(filename)
    ways_to_move_k = Counter(sum(x) for x in product(range(1, 4), repeat=3))
    score_b = play_game_p2(players, ways_to_move_k=ways_to_move_k, is_moving=1)
    x = deepcopy(STATES)
    answer_b = max(score_b)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 739785
    sample_b_answer = 444356092776315
    answer_a, answer_b = main(sample)
    assert (
        answer_a == sample_a_answer
    ), f"AnswerA incorrect: Actual: {answer_a}, Expected: {sample_a_answer}"
    print("sampleA correct")
    if answer_b:
        assert (
            answer_b == sample_b_answer
        ), f"AnswerB incorrect: Actual: {answer_b}, Expected: {sample_b_answer}"
        print("sampleB correct")

    # Test on your input and submit

    answer_a, answer_b = main(input)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    try:
        submit_answer(answer_a, "a")
    except AocdError:
        submit_answer(answer_b, "b")
