from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Set, Generator
import re


def parse(filename: str):

    with open(filename, "r") as f:

        inp = []
        for line in f.readlines():
            points = re.findall("\d+", line)
            inp.append(list(map(int, points)))
    return inp


def get_line_points(x1, y1, x2, y2, diagonal=False) -> Generator[Tuple[int, int]]:
    original = (x1, y1, x2, y2)
    if x1 == x2:
        if y2 >= y1:
            for i in range(y1, y2 + 1):
                yield x1, i
        else:
            for i in range(y1, y2 - 1, -1):
                yield x1, i
    elif y1 == y2:
        if x2 >= x1:
            for i in range(x1, x2 + 1):
                yield i, y1
        else:
            for i in range(x1, x2 - 1, -1):
                yield i, y1
    else:
        if diagonal:
            yield x1, y1
            yield x2, y2

            if x2 < x1:
                x1, y1, x2, y2 = (
                    x2,
                    y2,
                    x1,
                    y1,
                )  # reverse to avoid multiple cases
            slope = (y2 - y1) / (x2 - x1)
            dx = 1
            dy = -1 if slope < 0 else 1

            while x1 + dx < x2:
                x = x1 + dx
                y = y1 + dy
                # print(x, y, original)
                yield x, y
                dx += 1
                dy = dy - 1 if slope < 0 else dy + 1


def formulate_grid(
    lines: List[int], diagonal=False
) -> Dict[Tuple[int, int], int]:
    grid = defaultdict(lambda: 0)
    for line in lines:
        gen: Generator = get_line_points(*line, diagonal)
        for point in gen:
            grid[point] += 1
    return grid


def count_above_two(grid: Dict[Tuple[int, int], int]):
    counter = Counter(grid.values())
    values = [v for (k, v) in counter.items() if k >= 2]
    return sum(values)


if __name__ == "__main__":

    sample = "sample.txt"
    input = "input.txt"

    inp = input
    lines = parse(input)

    grid = formulate_grid(lines)
    total = count_above_two(grid)

    print(f"p1: {total}")
    print()
    grid = formulate_grid(lines, diagonal=True)
    total2 = count_above_two(grid)
    print(f"p2: {total2}")
