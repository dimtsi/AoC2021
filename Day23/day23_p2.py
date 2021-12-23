from collections import Counter, defaultdict, deque
from dataclasses import dataclass
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

from heapq import heappop, heappush
from copy import deepcopy
import re
from math import floor, ceil
from itertools import permutations, product

COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}
BUCKET_TO_ENTRANCE = {"A": 2, "B": 4, "C": 6, "D": 8}
ENTRANCE_TO_BUCKET = {v: k for k, v in BUCKET_TO_ENTRANCE.items()}
ALL_STATES_COSTS = defaultdict(lambda: float("inf"))

TARGET_POS = {
    "A": [11, 12, 13, 14],
    "B": [15, 16, 17, 18],
    "C": [19, 20, 21, 22],
    "D": [23, 24, 25, 26],
}
BUCKET_POS_TO_TARGET = {
    11: "A",
    12: "A",
    13: "A",
    14: "A",
    15: "B",
    16: "B",
    17: "B",
    18: "B",
    19: "C",
    20: "C",
    21: "C",
    22: "C",
    23: "D",
    24: "D",
    25: "D",
    26: "D",
}


def pprint(state):
    hallway = "".join(state[:11])
    printed = f"""
    #############
    #{hallway}#
    ###{state[11]}#{state[15]}#{state[19]}#{state[23]}###
      #{state[12]}#{state[16]}#{state[20]}#{state[24]}#
      #{state[13]}#{state[17]}#{state[21]}#{state[25]}#
      #{state[14]}#{state[18]}#{state[22]}#{state[26]}#
      #########
    """
    print(printed)


def move_to_empty(init, final, state):
    new_state = list(state)
    assert new_state[final] == "."
    new_state[init], new_state[final] = new_state[final], new_state[init]
    return tuple(new_state)


def find_new_droid_positions(
    state, start, must_land, elem=None
) -> Tuple[int, int]:

    elem = elem or state[start]
    assert elem in ["A", "B", "C", "D"], "Trying to move empty point"

    pos_dist = []

    dist = 0
    for i in range(start + 1, 11):
        dist += 1
        if state[i] != ".":  # blocked
            break
        elif i in ENTRANCE_TO_BUCKET:
            if elem == ENTRANCE_TO_BUCKET[i]:
                has_foreign = False
                bucket_values = [state[TARGET_POS[elem][k]] for k in range(4)]
                for depth, value in enumerate(bucket_values):
                    if value not in {elem, "."}:
                        has_foreign = True
                        break
                    if value == ".":
                        deepest_empty = depth
                if not has_foreign:
                    pos_dist.append(
                        (
                            TARGET_POS[elem][deepest_empty],
                            dist + deepest_empty + 1,
                        )
                    )
            else:
                continue
        else:
            if not must_land:
                pos_dist.append((i, dist))

    dist = 0
    for i in range(start - 1, -1, -1):
        dist += 1
        if state[i] != ".":
            break
        elif i in ENTRANCE_TO_BUCKET:
            if elem == ENTRANCE_TO_BUCKET[i]:
                has_foreign = False
                bucket_values = [state[TARGET_POS[elem][k]] for k in range(4)]
                for depth, value in enumerate(bucket_values):
                    if value not in {elem, "."}:
                        has_foreign = True
                        break
                    if value == ".":
                        deepest_empty = depth
                if not has_foreign:
                    pos_dist.append(
                        (
                            TARGET_POS[elem][deepest_empty],
                            dist + deepest_empty + 1,
                        )
                    )
            else:
                continue
        else:
            if not must_land:
                pos_dist.append((i, dist))
    return pos_dist


def get_new_states(state):

    for pos in range(11, 27):  # bucket positions

        elem = state[pos]
        target_elem = BUCKET_POS_TO_TARGET[pos]

        if state[pos] == ".":
            continue

        depth = (pos - 10) % 4
        if depth == 0:
            depth = 4

        next_k = (
            [state[pos + k] for k in range(1, 5 - depth)] if depth != 0 else []
        )
        prev_k = [state[pos - k] for k in range(1, depth)]

        if target_elem == elem and (
            all([el == target_elem for el in next_k]) or not next_k
        ):
            continue
        elif any([el != "." for el in prev_k]):
            continue
        else:

            for new_pos, dist in find_new_droid_positions(
                state,
                BUCKET_TO_ENTRANCE[target_elem],
                must_land=False,
                elem=elem,
            ):
                new_state = (
                    move_to_empty(pos, new_pos, state),
                    (dist + depth) * COSTS[elem],
                )
                yield new_state

    for pos in range(0, 11):  # hallway
        if state[pos] == ".":
            continue
        elem = state[pos]

        for new_pos, dist in find_new_droid_positions(
            state, pos, must_land=True, elem=elem
        ):
            new_state = move_to_empty(pos, new_pos, state), dist * COSTS[elem]
            yield new_state


def parse(filename: str) -> List:

    with open(filename, "r") as f:
        data = f.read().strip()
    target_pos = deepcopy(TARGET_POS)

    initial_state = ["." for _ in range(27)]

    for line in data.split("\n"):
        row = re.findall("[a-zA-Z]", line)
        if not row:
            continue
        for bucket, occ in zip(["A", "B", "C", "D"], row):
            if occ:
                initial_state[target_pos[bucket].pop(0)] = occ
    pprint(initial_state)
    return tuple(initial_state)


def min_cost(init_state):
    final_pos = tuple(list("...........AAAABBBBCCCCDDDD"))

    pq = [(0, init_state)]
    visited = set()
    ALL_STATES_COSTS[init_state] = 0

    while pq:
        cost, state = heappop(pq)

        visited.add(state)
        for new_state, val in get_new_states(state):
            if (
                not new_state in visited
                and ALL_STATES_COSTS[new_state] > cost + val
            ):
                ALL_STATES_COSTS[new_state] = cost + val
                heappush(pq, (cost + val, new_state))
                if new_state == final_pos:
                    pprint(new_state)
    out = ALL_STATES_COSTS[final_pos]
    return out


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    # p1
    init_position = parse(filename)
    answer_b = min_cost(init_position)
    x = ALL_STATES_COSTS
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample2.txt"
    input = "input2.txt"

    sample_b_answer = 44169
    _, answer_b = main(sample)

    if answer_b:
        assert (
            answer_b == sample_b_answer
        ), f"AnswerB incorrect: Actual: {answer_b}, Expected: {sample_b_answer}"
        print("sampleB correct")

    # Test on your input and submit
    ALL_STATES_COSTS.clear()
    answer_a, answer_b = main(input)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    # try:
    #     submit_answer(answer_a, "a")
    # except AocdError:
    submit_answer(answer_b, "b")
