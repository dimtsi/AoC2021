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
import numpy as np
from itertools import combinations


def parse(filename):

    with open(filename, "r") as f:
        lines: List[str] = f.read().rstrip().splitlines()

    empty = {}
    vert = defaultdict(lambda: None)
    horiz = defaultdict(lambda: None)
    n_rows = len(lines)
    n_cols = len(lines[0])
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == ">":
                horiz[i, j] = lines[i][j]
            elif lines[i][j] == "v":
                vert[i, j] = lines[i][j]
            else:
                empty[i, j] = lines[i][j]
    return empty, horiz, vert, n_rows, n_cols


def prev(i, j, n_rows, n_cols):
    if i < 0:
        i = n_rows + i
    if j < 0:
        j = n_cols + j
    return i, j


def pprint(horiz: Dict, vert: Dict, n_rows: int, n_cols: int):
    matrix = [["." for _ in range(n_cols)] for _ in range(n_rows)]

    for i, j in horiz:
        if horiz[i, j]:
            matrix[i][j] = ">"

    for i, j in vert:
        if vert[i, j]:
            matrix[i][j] = "v"

    for row in matrix:
        print("".join(row))


def step(empty: Dict, horiz: Dict, vert: Dict, n_rows: int, n_cols: int):
    move_count = 0
    new_empty = deepcopy(empty)
    new_horiz = deepcopy(horiz)
    new_vert = deepcopy(vert)

    for i, j in empty:
        prev_hor = prev(i, j - 1, n_rows, n_cols)
        if horiz[prev_hor]:
            new_empty.pop((i, j))
            new_horiz[i, j] = horiz[prev_hor]
            new_horiz.pop(prev_hor)
            new_empty[prev_hor] = "."
            move_count += 1

    empty = deepcopy(new_empty)
    for i, j in empty:
        prev_vert = prev(i - 1, j, n_rows, n_cols)
        if vert[prev_vert]:
            new_empty.pop((i, j))
            new_vert[i, j] = vert[prev_vert]
            new_vert.pop(prev_vert)
            new_empty[prev_vert] = "."
            move_count += 1

    return new_empty, new_horiz, new_vert, move_count


def run_steps(empty: Dict, horiz: Dict, vert: Dict, n_rows: int, n_cols: int):

    move_count = 1
    n_steps = 0
    while move_count != 0:
        empty, horiz, vert, move_count = step(
            empty, horiz, vert, n_rows, n_cols
        )
        n_steps += 1
    return n_steps


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    empty, horiz, vert, n_rows, n_cols = parse(filename)
    answer_a = run_steps(empty, horiz, vert, n_rows, n_cols)
    # answer_a, answer_b = calibrate(scanners)
    # answer_b = val
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 58
    sample_b_answer = 3621

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

    # # Test on your input and submit
    answer_a, answer_b = main(input)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    # try:
    #     submit_answer(answer_a, "a")
    # except AocdError:
    #     submit_answer(answer_b, "b")
