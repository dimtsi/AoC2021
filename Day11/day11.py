from collections import Counter, defaultdict, deque
from typing import (
    List,
    Tuple,
    Set,
    Dict,
    Iterable,
    DefaultDict,
)
from copy import deepcopy


FLASHED_DURING_STEP: Set[Tuple[int, int]] = set()
FLASH_COUNT = 0


def parse(filename: str) -> List[List[int]]:
    matrix = []

    with open(filename, "r") as f:
        for line in f.read().strip().split("\n"):
            matrix.append(list(map(int, line.strip())))
    return matrix


def get_neighbors(
    matrix: List[List[int]], i: int, j: int
) -> List[Tuple[int, int]]:
    neighbors = []

    num_rows = len(matrix)
    num_cols = len(matrix[i])

    if i - 1 >= 0:
        neighbors.append((i - 1, j))
    if i + 1 < num_rows:
        neighbors.append((i + 1, j))
    if j - 1 >= 0:
        neighbors.append((i, j - 1))
    if j + 1 < num_cols:
        neighbors.append((i, j + 1))
    # diagonal
    if i - 1 >= 0 and j - 1 >= 0:
        neighbors.append((i - 1, j - 1))
    if i - 1 >= 0 and j + 1 < num_cols:
        neighbors.append((i - 1, j + 1))
    if i + 1 < num_rows and j - 1 >= 0:
        neighbors.append((i + 1, j - 1))
    if i + 1 < num_rows and j + 1 < num_cols:
        neighbors.append((i + 1, j + 1))
    return neighbors


def flash(i: int, j: int, matrix: List[List[int]]) -> None:
    if matrix[i][j] >= 10:
        global FLASH_COUNT
        global FLASHED_DURING_STEP
        FLASH_COUNT += 1
        FLASHED_DURING_STEP.add((i, j))
        matrix[i][j] = 0
        neighbors = get_neighbors(matrix, i, j)
        for x, y in neighbors:
            if (x, y) not in FLASHED_DURING_STEP:
                matrix[x][y] += 1
                flash(x, y, matrix)


def step(matrix: List[List[int]]) -> None:
    global FLASHED_DURING_STEP
    FLASHED_DURING_STEP = set()
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] += 1

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            flash(i, j, matrix)


def run_k_steps(matrix: List[List[int]], k: int) -> None:
    for i in range(k):
        step(matrix)


def run_until_all_flash(matrix: List[List[int]]) -> int:
    steps = 0
    while True:
        steps += 1
        step(matrix)
        global FLASHED_DURING_STEP
        if len(FLASHED_DURING_STEP) == len(matrix) * len(matrix[0]):
            break
    return steps


def main(filename: str) -> Tuple[int, int]:
    from time import time

    answer_a, answer_b = None, None

    start = time()
    matrix = parse(filename)

    run_k_steps(deepcopy(matrix), 100)
    answer_a = FLASH_COUNT
    answer_b = run_until_all_flash(deepcopy(matrix))

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 1656
    sample_b_answer = 195

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

    FLASH_COUNT = 0

    # Test on your input and submit
    answer_a, answer_b = main(input)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    try:
        submit_answer(answer_a, "a")
    except AocdError:
        submit_answer(answer_b, "b")

    print()
