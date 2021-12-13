from collections import Counter, defaultdict, deque
from typing import (
    List,
    Tuple,
    Set,
    Dict,
    Iterable,
    DefaultDict,
    Optional,
)
from copy import deepcopy


def parse(filename: str) -> Tuple[Set[Tuple[int, int]], List[Tuple[str, int]]]:

    with open(filename, "r") as f:
        init_pos, folds_raw = f.read().strip().split("\n\n")
    hash_positions: Set[Tuple[int, int]] = set()  # type: ignore

    for pos in init_pos.split("\n"):
        hash_positions.add(tuple((map(int, pos.split(",")))))  # type: ignore

    folds = []
    for fold in folds_raw.split("\n"):
        parsed = fold.split("fold along ")[1]
        parsed_dir: str = parsed[0]
        parsed_row_col: str = parsed[2:]
        folds.append((parsed_dir, int(parsed_row_col)))
    return hash_positions, folds


def get_new_hash_position(
    init_pos: Tuple[int, int], hv: bool, fold_row_column: int
) -> Tuple[int, int]:
    if hv:  # horizontal fold:
        target_y = init_pos[1]
        target_x = fold_row_column - abs(fold_row_column - init_pos[0])
    else:  # vertical
        target_x = init_pos[0]
        target_y = fold_row_column - abs(fold_row_column - init_pos[1])
    return target_x, target_y


def fold(
    hash_positions: Set[Tuple[int, int]], transformation: Tuple[str, int]
) -> Set[Tuple[int, int]]:
    hv, fold_row_col = transformation
    to_add = set()
    to_remove = set()
    if hv == "x":
        for x, y in hash_positions:
            if x > fold_row_col:
                target_x, target_y = get_new_hash_position(
                    (x, y), True, fold_row_col
                )
                to_add.add((target_x, target_y))
                to_remove.add((x, y))
            elif x == fold_row_col:
                to_remove.add((x, y))
    elif hv == "y":
        for x, y in hash_positions:
            if y > fold_row_col:
                target_x, target_y = get_new_hash_position(
                    (x, y), False, fold_row_col
                )
                to_add.add((target_x, target_y))
                to_remove.add((x, y))
            elif y == fold_row_col:
                to_remove.add((x, y))

    new_positions = (hash_positions - to_remove) | to_add
    return new_positions


def fold_n(
    hash_positions: Set[Tuple[int, int]],
    fold_commands: List[Tuple[str, int]],
    n_folds: int,
) -> Set[Tuple[int, int]]:
    for i in range(n_folds):
        transformation = fold_commands[i]
        hash_positions = fold(hash_positions, transformation)
    return hash_positions


def create_and_print_grid(hash_positions: Set[Tuple[int, int]]) -> None:
    max_x = max(hash_positions, key=lambda x: x[0])[0]
    max_y = max(hash_positions, key=lambda x: x[1])[1]

    G = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    print()
    for i, j in hash_positions:
        G[j][i] = "#"
    for row in G:
        print("".join(row))
    print()


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    answer_a, answer_b = None, None

    start = time()
    initial_positions, folds = parse(filename)
    hash_positions = fold_n(initial_positions, folds, 1)
    answer_a = len(hash_positions)

    # p2
    hash_positions = fold_n(initial_positions, folds, len(folds))
    create_and_print_grid(hash_positions)
    ###  #  # #  # #### ####  ##  #  # ###
    #  # # #  #  # #       # #  # #  # #  #
    #  # ##   #### ###    #  #    #  # ###
    ###  # #  #  # #     #   # ## #  # #  #
    # #  # #  #  # #    #    #  # #  # #  #
    #  # #  # #  # #    ####  ###  ##  ###
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 17
    sample_b_answer = None

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
    # try:
    #     submit_answer(answer_a, "a")
    # except AocdError:
    #     submit_answer(answer_b, "b")

    print()
