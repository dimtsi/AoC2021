# courtesy of hectormallot

from typing import List
import re


def parse(filename: str) -> List[int]:
    with open(filename, "r") as f:
        lines = re.findall("\d+", f.read())
        lines = list(map(int, lines))

        fish = [lines.count(i) for i in range(9)]
    return fish


def simulate(fish: List[int], days: int) -> int:
    i = 0
    for _ in range(days):
        fish[i], fish[7], fish[8] = fish[i] + fish[7], fish[8], fish[i]
        i = (i + 1) % 7
    return sum(fish)



if __name__ == "__main__":

    from time import time
    start = time()
    sample = "sample.txt"
    input = "input.txt"

    inp = input

    fish = parse(inp)
    total_1 = simulate(fish[:], days=80)
    # # p2
    total_2 = simulate(fish[:], days=256)
    end = time()
    print(end - start)
    print(f"p1: {total_1}\np2: {total_2}")

