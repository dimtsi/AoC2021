from typing import List, Dict, Tuple, Set
from copy import deepcopy


def parse(filename: str):

    with open(filename, "r") as f:

        seq, boards = f.read().split("\n\n", 1)
        seq = list(map(int, seq.split(",")))

        boards = boards.split("\n\n")
        new_boards = [board.split("\n") for board in boards]

        final_boards = []
        for board in new_boards:
            final_b = [list(map(int, line.split())) for line in board]
            final_boards.append(final_b)

        return seq, final_boards


def to_dict(board: List[List[int]]) -> Dict[int, Tuple[int, int]]:
    # dict returning indices for quick lookups
    lookup = {}

    for i in range(len(board)):
        for j in range(len(board[0])):
            lookup[board[i][j]] = (i, j)

    return lookup


def load_data(
    filename: str,
) -> Tuple[List[int], List[Dict[int, Tuple[int, int]]], List[List[List[bool]]]]:
    seq, boards = parse(filename)
    board_lookups = [to_dict(board) for board in boards]
    masks = init_masks(boards)
    return seq, board_lookups, masks


def check_if_complete(board_mask: List[List[bool]]):
    # check rows
    for row in board_mask:
        if all(row):
            return True
    # check cols
    for j in range(len(board_mask[0])):
        if all([board_mask[i][j] for i in range(len(board_mask))]):
            return True
    return False


def init_masks(boards: List):
    nrows = len(boards[0])
    ncols = len(boards[0][0])
    mask = [ncols * [False] for _ in range(nrows)]
    return [deepcopy(mask) for _ in boards]


def return_unchecked(board: Dict, visited: Set) -> Set:
    unvisited = set(board.keys()) - visited
    return unvisited


def play(
    seq: List,
    boards: List[Dict[int, Tuple[int, int]]],
    masks: List[List[List[bool]]],
    part: int,
):
    visited = [set() for _ in masks]
    has_won = [False for _ in masks]

    while seq:
        num = seq.pop(0)

        for k in range(len(boards)):
            if num in boards[k]:
                i, j = boards[k][num]
                masks[k][i][j] = True
                visited[k].add(num)
                if check_if_complete(masks[k]):
                    if part == 1:
                        seq = []  # get out of both loops
                        break

                    elif part == 2:
                        has_won[k] = True
                        if all(has_won):
                            seq = []  # get out of both loops
                            break
    unchecked = return_unchecked(boards[k], visited[k])
    score = sum(unchecked) * num
    return score


if __name__ == "__main__":

    sample = "sample.txt"
    input = "input.txt"

    inp = input

    seq, board_lookups, masks = load_data(inp)
    score = play(seq, board_lookups, masks, 1)
    print(f"p1: {score}")
    print()
    seq, board_lookups, masks = load_data(inp)
    score = play(seq, board_lookups, masks, 2)
    print(f"p2: {score}")
