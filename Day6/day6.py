from collections import defaultdict, Counter
from typing import Dict
import re
from copy import deepcopy

from utils import timing_val


def parse(filename: str) -> Dict[int, int]:
    with open(filename, "r") as f:
        lines = re.findall("\d+", f.read())
        lines = map(int, lines)

        fish = defaultdict(lambda: 0)
        fish.update(Counter(lines))
    return fish


def step(val: int, fish: Dict, new_fish: Dict):
    if val == 0:
        new_fish[6] += fish[val]
        new_fish[8] += fish[val]
    else:
        new_fish[val - 1] += fish[val]
    new_fish[val] -= fish[val]


def simulate(fish: Dict[int, int], days: int) -> int:
    day = 0
    while day < days:
        new_fish = deepcopy(fish)
        [step(key, fish, new_fish) for key in fish.keys()]
        fish = deepcopy(new_fish)
        day += 1
    return sum(fish.values())


if __name__ == "__main__":

    from time import time

    start = time()
    sample = "sample.txt"
    input = "input.txt"

    inp = input

    fish = parse(inp)
    total_1 = simulate(deepcopy(fish), days=80)
    # # p2
    total_2 = simulate(deepcopy(fish), days=256)
    end = time()
    print(end - start)
    print(f"p1: {total_1}\np2: {total_2}")
