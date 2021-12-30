from collections import Counter, defaultdict, deque
from functools import lru_cache
from typing import (
    List,
    Tuple,
    Set,
    Dict,
    Iterable,
    DefaultDict,
    Optional,
    Union,
    Generator,
)
from copy import deepcopy
import re
from math import floor, ceil
from itertools import permutations, product


class State:
    lighted_x: List
    lighted_y: List
    lighted_z: List


def parse(filename: str) -> Tuple[List, List]:
    points = []
    states = []
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        for line in lines:
            state, coords = line.split(" ")
            coords = tuple(map(int, re.findall("-?\d+", coords)))  # type: ignore
            states.append(True if state == "on" else False)
            points.append(coords)
    return states, points


def run_p1(
    states: List[bool], limits: List[Tuple[int, int, int, int, int, int, int]]
) -> int:

    states = states[:20]
    limits = limits[:20]

    on = set()
    for state, limit in zip(states, limits):
        coords = set()
        for x in range(limit[0], limit[1] + 1):
            for y in range(limit[2], limit[3] + 1):
                for z in range(limit[4], limit[5] + 1):
                    coord = (x, y, z)
                    if any(
                        filter(lambda k: k < -50, coord)
                        or any(filter(lambda k: k > 50, coord))
                    ):
                        continue
                    if state and coord not in on:
                        on.add(coord)
                    elif not state and coord in on:
                        on.remove(coord)
    return len(on)


def volume(kuboids: List[Tuple[int, int, int, int, int, int]]) -> int:
    total = 0
    for kuboid in kuboids:
        dx = kuboid[1] - kuboid[0] + 1
        dy = kuboid[3] - kuboid[2] + 1
        dz = kuboid[5] - kuboid[4] + 1
        prod = dx * dy * dz
        total += prod
    return total


def coord_intersect(
    old_min: int, old_max: int, new_min: int, new_max: int
) -> Optional[Tuple[int, int]]:
    if new_max < old_min or new_min > old_max:
        return None
    if new_min < old_min:
        if new_max > old_max:
            return old_min, old_max
        else:
            return old_min, new_max
    else:
        if new_max > old_max:
            return new_min, old_max
        else:
            return new_min, new_max


def get_intersection_cube(
    old: Tuple[int, int, int, int, int, int],
    new: Tuple[int, int, int, int, int, int],
) -> Optional[Tuple[int, int, int, int, int, int]]:
    x_min_old, x_max_old, y_min_old, y_max_old, z_min_old, z_max_old = old
    x_min_new, x_max_new, y_min_new, y_max_new, z_min_new, z_max_new = new

    inters_x = coord_intersect(x_min_old, x_max_old, x_min_new, x_max_new)
    if not inters_x:
        return None
    inters_y = coord_intersect(y_min_old, y_max_old, y_min_new, y_max_new)
    if not inters_y:
        return None
    inters_z = coord_intersect(z_min_old, z_max_old, z_min_new, z_max_new)
    if not inters_z:
        return None
    return *inters_x, *inters_y, *inters_z  # type: ignore


def run_p2(
    states: List[bool], coords: List[Tuple[int, int, int, int, int, int]]
) -> int:
    positive_cubes = [coords[0]]
    negative_cubes: List[Tuple[int, int, int, int, int, int]] = []

    for i, (state, coord) in enumerate(zip(states, coords)):
        new_positive = []
        new_negative = []
        if i == 0:
            continue
        else:
            for positive in positive_cubes:
                intersection = get_intersection_cube(positive, coord)
                if intersection:
                    new_negative.append(intersection)
            for negative in negative_cubes:
                intersection = get_intersection_cube(negative, coord)
                if intersection:
                    new_positive.append(intersection)

        if state:
            new_positive.append(coord)

        positive_cubes.extend(new_positive)
        negative_cubes.extend(new_negative)

    score = volume(positive_cubes) - volume(negative_cubes)
    return score


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    # p1
    if "sample" in filename:
        filename = "sample.txt"
    states, limits = parse(filename)
    answer_a = run_p1(states, limits)
    # p2
    if "sample" in filename:
        filename = "sample1.txt"
    states, limits = parse(filename)
    answer_b = run_p2(states, limits)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 590784
    sample_b_answer = 2758514936282235
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
