from collections import Counter, defaultdict, deque
from functools import reduce, lru_cache
from typing import (
    List,
    Tuple,
    Set,
    Dict,
    Iterable,
    DefaultDict,
    Optional, Union,
)
from copy import deepcopy
import re

def parse(filename: str) -> List[List[int]]:
    matrix = []
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")

    for line in lines:
        matrix.append(list(map(int, list(line))))

    return matrix


def get_neighbors_vals(
    matrix: List[List[Union[int, float]]], i: int, j: int
) -> List[int]:
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

    return [matrix[i][j] for (i, j) in neighbors]

 
def min_cost(matrix):

    n_rows, n_cols = len(matrix), len(matrix[0])
    costs = [[float("inf") for _ in range(n_cols)] for _ in range(n_rows)]

    costs[0][0] = 0
    prev_answer = -1
    answer = -2


    iters = 0
    has_changed = True
    while has_changed:  # does not converge on first try
        has_changed = False
        for i in range(n_rows):
            for j in range(n_cols):
                if i == 0 and j == 0:
                    continue
                neighbors = get_neighbors_vals(costs, i, j)
                new_val = min(neighbors) + matrix[i][j]
                old_val = costs[i][j]
                if not has_changed and old_val != new_val:
                    has_changed = True
                costs[i][j] = new_val
        answer = costs[n_rows-1][n_cols-1]
        iters += 1
    print(f"iters:{iters}")
    return answer


def construct_new_array(matrix):
    n_rows_old, n_cols_old = len(matrix), len(matrix[0])
    new_matrix = [[0 for _ in range(n_rows_old * 5)] for _ in range(n_cols_old * 5)]
    n_rows_new, n_cols_new = len(new_matrix), len(new_matrix[0])

    for i in range(n_rows_new):
        for j in range(n_cols_new):
            di = i // n_rows_old
            dj = j // n_cols_old
            new_matrix[i][j] = matrix[i % n_rows_old][j % n_cols_old] + di + dj
            if new_matrix[i][j] >= 10:
                new_matrix[i][j] %= 9
    return new_matrix


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    matrix = parse(filename)
    answer_a = min_cost(matrix)
    
    new_array = construct_new_array(matrix)
    answer_b = min_cost(new_array)
 
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample2.txt"
    input = "input.txt"

    sample_a_answer = 40
    sample_b_answer = 413

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
