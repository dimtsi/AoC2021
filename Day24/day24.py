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


def get_block_params(cmds: List):
    DIVZs, ADDXs, ADDYs = [], [], []
    start_idx = 0
    for _ in range(14):
        divz5 = cmds[start_idx + 4][-1]
        addx6 = cmds[start_idx + 5][-1]
        addy15 = cmds[start_idx + 15][-1]

        DIVZs.append(divz5)
        ADDXs.append(addx6)
        ADDYs.append(addy15)
        start_idx += 18
    return DIVZs, ADDXs, ADDYs


def parse(filename: str) -> Tuple[List, List]:
    points = []
    states = []
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        commands = []
        for line in lines:
            split = line.split()
            if re.findall("-?\d+", split[-1]):
                split[-1] = int(split[-1])
            commands.append(split[:])
    return commands


def backward(addx, addy, divz, z_after, w):
    z_prev = []
    x_eq = z_after - w - addy
    if x_eq % 26 == 0:
        z_prev.append((x_eq // 26) * divz)
    if 0 <= w - addx < 26:
        z_prev.append(w - addx + z_after * divz)

    return z_prev


def solve(cmds, p2=False):
    zs = {0}
    result = defaultdict(tuple)

    DIVZs, ADDXs, ADDYs = get_block_params(cmds)

    if not p2:
        ws = range(1, 10)
    else:
        ws = range(9, 0, -1)
    for divz, addx, addy in reversed(list(zip(DIVZs, ADDXs, ADDYs))):

        z_prev_set = set()
        for w, z in product(ws, zs):
            z_prevs = backward(addx, addy, divz, z, w)
            if len(z_prevs) > 1:
                print(z_prevs)
            for z0 in z_prevs:
                z_prev_set.add(z0)
                result[z0] = tuple([w]) + result[z]
        zs = z_prev_set
    res = "".join(str(i) for i in result[0])
    print(res)
    return res


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    # p1
    commands = parse(filename)
    answer_a = solve(commands, 1)
    answer_b = solve(commands, 2)
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    # sample = "input.txt"
    input = "input.txt"

    sample_a_answer = 739785
    sample_b_answer = 444356092776315
    answer_a, answer_b = main(input)
    # assert (
    #     answer_a == sample_a_answer
    # ), f"AnswerA incorrect: Actual: {answer_a}, Expected: {sample_a_answer}"
    # print("sampleA correct")
    # if answer_b:
    #     assert (
    #         answer_b == sample_b_answer
    #     ), f"AnswerB incorrect: Actual: {answer_b}, Expected: {sample_b_answer}"
    #     print("sampleB correct")
    #
    # # Test on your input and submit
    #
    # answer_a, answer_b = main(input)
    # print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    # try:
    #     submit_answer(answer_a, "a")
    # except AocdError:
    #     submit_answer(answer_b, "b")
