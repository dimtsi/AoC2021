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

TARGET_POS = {"A": [11, 12], "B": [13, 14], "C": [15, 16], "D": [17, 18]}
BUCKET_POS_TO_TARGET = {
    11: "A",
    12: "A",
    13: "B",
    14: "B",
    15: "C",
    16: "C",
    17: "D",
    18: "D",
}


def pprint(state: Tuple[int, ...]):
    hallway = "".join(state[:11])
    printed = f"""
    #############
    #{hallway}#
    ###{state[11]}#{state[13]}#{state[15]}#{state[17]}###
      #{state[12]}#{state[14]}#{state[16]}#{state[18]}#
      #########
    """
    print(printed)


def move_to_empty(init: int, final: int, state: Tuple[int, ...]) -> Tuple[int, ...]:
    new_state = list(state)
    assert new_state[final] == "."
    new_state[init], new_state[final] = new_state[final], new_state[init]
    return tuple(new_state)


def find_new_droid_positions(
    state: Tuple[int, ...], start: int, must_land: bool, elem: Optional[int] = None
) -> List[Tuple[int, int]]:

    elem = elem or state[start]
    if elem not in ["A", "B", "C", "D"]:
        raise Exception("Trying to move empty point")

    pos_dist = []
    dist = 0

    for i in range(start + 1, 11):
        dist += 1
        if state[i] != ".":  # blocked
            break
        elif i in ENTRANCE_TO_BUCKET:
            k = ENTRANCE_TO_BUCKET[i]
            if elem == ENTRANCE_TO_BUCKET[i]:
                value1, value2 = (
                    state[TARGET_POS[elem][0]],
                    state[TARGET_POS[elem][1]],
                )
                if value1 != ".":
                    continue
                elif value1 == value2 == ".":
                    pos_dist.append((TARGET_POS[elem][1], dist + 2))
                elif value1 == "." and value2 != elem:
                    continue
                elif value1 == "." and value2 == elem:
                    pos_dist.append((TARGET_POS[elem][0], dist + 1))

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
                value1, value2 = (
                    state[TARGET_POS[elem][0]],
                    state[TARGET_POS[elem][1]],
                )

                if value1 != ".":
                    continue
                elif value1 == value2 == ".":
                    pos_dist.append((TARGET_POS[elem][1], dist + 2))
                elif value1 == "." and value2 != elem:
                    continue
                elif value1 == "." and value2 == elem:
                    pos_dist.append((TARGET_POS[elem][0], dist + 1))
            else:
                continue
        else:
            if not must_land:
                pos_dist.append((i, dist))
    return pos_dist


def get_new_states(state: Tuple[int, ...]):
    for pos in range(11, 19):  # bucket positions

        elem = state[pos]
        target_elem = BUCKET_POS_TO_TARGET[pos]

        if state[pos] == ".":
            continue
        if pos % 2 == 0:  # bottom position
            if pos in TARGET_POS[state[pos]]:
                continue
            elif state[pos - 1] != ".":  # occupied directly above
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
                        (dist + 2) * COSTS[elem],
                    )
                    yield new_state
        else:  # top bucket
            if pos in TARGET_POS[elem]:
                if state[pos + 1] == elem:
                    continue
            for new_pos, dist in find_new_droid_positions(
                state,
                BUCKET_TO_ENTRANCE[target_elem],
                must_land=False,
                elem=elem,
            ):
                new_state = (
                    move_to_empty(pos, new_pos, state),
                    (dist + 1) * COSTS[elem],
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

    initial_state = ["." for _ in range(19)]
    count = 0
    for i, line in enumerate(data.split("\n")):
        row = re.findall("[a-zA-Z]", line)
        if not row:
            continue
        for bucket, occ in zip(["A", "B", "C", "D"], row):
            if occ:
                initial_state[target_pos[bucket].pop(0)] = occ
        count += 1

    return tuple(initial_state)


def min_cost(init_state):
    final_pos = tuple(list("...........AABBCCDD"))

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
    answer_a = min_cost(init_position)
    x = ALL_STATES_COSTS
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 12521
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
    ALL_STATES_COSTS.clear()
    answer_a, answer_b = main(input)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    try:
        submit_answer(answer_a, "a")
    except AocdError:
        submit_answer(answer_b, "b")
