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


def parse(filename):
    with open(filename, 'r') as f:
        data = f.read()
    algo, image = data.rstrip().split("\n\n")

    image_d = {}
    for i, line in enumerate(image.split("\n")):
        for j, val in enumerate(list(line)):
            image_d[i, j] = val

    return algo.strip().replace("\n", ""), image_d


def bin_to_int(bin_str: str) -> int:
    return int(bin_str, 2)


def get_value_from_window(s, algo):
    bstring = s.replace("#", "1").replace(".", "0")
    index = bin_to_int(bstring)
    return algo[index]


def pprint(image: DefaultDict[Tuple[int, int], str]) -> None:
    max_x = max(image, key=lambda x: x[0])[0]
    max_y = max(image, key=lambda x: x[1])[1]

    for i in range(max_x + 1):
        row = ""
        for j in range(max_y + 1):
            row += image[i, j]


def count_lighted_after_n(image: Dict[Tuple[int, int], str], algo: str, n_steps: int) -> int:
    inf = "."
    image = defaultdict(lambda: inf, image)
    newimage = defaultdict(lambda: inf)
    max_x = max(image, key=lambda x: x[0])[0]
    max_y = max(image, key=lambda x: x[1])[1]

    for _ in range(n_steps):
        for i in range(-1, max_x + 2):
            for j in range(-1, max_y + 2):
                neighbors = []
                for wi in range(i-1, i+2):
                    for wj in range(j-1, j+2):
                        neighbors.append(image[wi, wj])
                val = get_value_from_window("".join(neighbors), algo)
                newimage[i+1, j+1] = val

        inf = algo[0] if inf == "." else algo[-1]
        image = deepcopy(newimage)
        newimage.clear()
        max_x += 2
        max_y += 2
    return Counter(image.values())["#"]


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    # p1
    algo, image = parse(filename)
    answer_a = count_lighted_after_n(image, algo, 2)
    answer_b = count_lighted_after_n(image, algo, 50)
    print()

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 35
    sample_b_answer = 3351

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
