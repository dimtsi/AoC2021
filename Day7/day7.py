from collections import Counter
import re


def parse(filename: str) -> Counter:
    with open(filename, "r") as f:
        lines = list(map(int, re.findall("\d+", f.read())))
        lines = Counter(lines)
    return lines


def find_min_position(positions: Counter, p2=False):
    max_dist = max(positions.keys())

    if p2:
        step_costs = [i for i in range(max_dist + 1)]
        for i in range(1, len(step_costs)):
            step_costs[i] += step_costs[i - 1]

    min_fuel = float("inf")
    min_k = None
    for k in range(max_dist + 1):
        sum_diff = 0
        for val, count in positions.items():
            if p2:
                sum_diff += count * step_costs[abs(val - k)]
            else:
                sum_diff += count * abs(val - k)
            if sum_diff > min_fuel:  # stop loop if already higher
                break
        if sum_diff < min_fuel:
            min_fuel, min_k = sum_diff, k
    return min_fuel, min_k


if __name__ == "__main__":

    from time import time

    start = time()
    sample = "sample.txt"
    input = "input.txt"

    inp = input
    start = time()
    positions = parse(inp)
    min_fuel_1, min_k_1 = find_min_position(positions)
    # # # p2
    min_fuel_2, min_k_2 = find_min_position(positions, p2=True)
    end = time()
    print(end - start)
    print(f"p1: {min_fuel_1}\np2: {min_fuel_2}")
