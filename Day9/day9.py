from collections import Counter, defaultdict, deque
from typing import (
    List,
    Tuple,
    Set,
    Dict,
    Iterable,
    DefaultDict,
)
from functools import reduce


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
    return neighbors


def get_neighbors_and_values(
    matrix: List[List[int]], i: int, j: int
) -> Tuple[List[Tuple[int, int]], List[int]]:

    neighbors = get_neighbors(matrix, i, j)
    vals = [matrix[x][y] for (x, y) in neighbors]
    return neighbors, vals


def check_if_lower_than_neighbors(matrix: List[List[int]], i: int, j: int):
    neighbors, neigh_vals = get_neighbors_and_values(matrix, i, j)

    if matrix[i][j] < min(neigh_vals):
        return True
    return False


def find_minimums(
    matrix: List[List[int]],
) -> Tuple[List[int], List[Tuple[int, int]]]:
    mins = []
    min_positions = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if check_if_lower_than_neighbors(matrix, i, j):
                mins.append(matrix[i][j])
                min_positions.append((i, j))
    return mins, min_positions


def find_basins(matrix: List[List[int]]) -> List[Set[Tuple[int, int]]]:
    basins = []

    mins, min_positions = find_minimums(matrix)

    for min_pos in min_positions:
        basin = {min_pos}
        q = deque([min_pos])
        while q:
            curr = q.popleft()  # bfs
            curr_val = matrix[curr[0]][curr[1]]
            neighbors, neigh_vals = get_neighbors_and_values(matrix, *curr)
            for neigh, val in zip(neighbors, neigh_vals):
                if neigh not in basin and val > curr_val and val != 9:
                    q.append(neigh)
                    basin.add(neigh)
        basins.append(len(basin))
    return basins


def find_topk_basins(matrix: List[List[int]], k: int):
    basins = find_basins(matrix)
    topk = sorted(basins, reverse=True)[:k]
    return topk


if __name__ == "__main__":
    from time import time

    start = time()
    sample = "sample.txt"
    input = "input.txt"

    inp = input
    start = time()
    matrix = parse(inp)
    mins, _ = find_minimums(matrix)
    minsum = sum(map(lambda x: x + 1, mins))
    print(f"p1: {minsum}")
    # p2
    topk_basins = find_topk_basins(matrix, 3)
    prod = reduce(lambda x, y: x * y, topk_basins)
    end = time()
    print(f"p2: {prod}")
    print(end - start)
