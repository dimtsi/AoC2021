from collections import defaultdict, Counter
from typing import Dict, List
import re

from utils import timing_val


def parse(filename: str) -> List[int]:
    with open(filename, "r") as f:
        lines = re.findall("\d+", f.read())
        lines = list(map(int, lines))

        fish = [lines.count(i) for i in range(9)]
    return fish


@timing_val
def simulate(fish: List[int], days: int) -> int:
    day = 0
    while day < days:
        fish.append(fish[0])
        fish[7] += fish[0]
        fish = fish[1:]

        day += 1
    return sum(fish)


if __name__ == "__main__":

    sample = "sample.txt"
    input = "input.txt"

    inp = input

    fish = parse(inp)
    total = simulate(fish, days=80)
    print(f"p1: {total}")
    print()
    # # p2
    fish = parse(inp)
    total = simulate(fish, days=256)
    print(f"p2: {total}")

