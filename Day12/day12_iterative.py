from collections import Counter, defaultdict, deque
from typing import (
    List,
    Tuple,
    Set,
    Dict,
    Iterable,
    DefaultDict,
)
from copy import deepcopy


RULES: DefaultDict[str, Set[str]] = defaultdict(set)
TOTAL_COUNT = 0


def parse(filename: str) -> None:
    global RULES

    with open(filename, "r") as f:
        for line in f.read().strip().split("\n"):
            source, dest = line.split("-")
            RULES[source].add(dest)
            RULES[dest].add(source)


def find_path(p2=False):
    global TOTAL_COUNT
    stack = deque([("start", {"start"}, False)])

    while stack:
        curr_node, curr_path_unique, freeze = stack.pop()

        if curr_node == "end":
            TOTAL_COUNT += 1

        else:
            for connection in RULES[curr_node]:
                if connection.isupper() or connection not in curr_path_unique:
                    stack.append(
                        (connection, curr_path_unique | {connection}, freeze)
                    )
                elif p2 and not freeze and connection != "start":
                    stack.append(
                        (connection, curr_path_unique | {connection}, True)
                    )


def main(filename: str) -> Tuple[int, int]:
    from time import time

    global TOTAL_COUNT

    start = time()
    parse(filename)
    find_path(p2=False)
    answer_a = TOTAL_COUNT
    # p2
    TOTAL_COUNT = 0
    find_path(p2=True)
    answer_b = TOTAL_COUNT

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 10
    sample_b_answer = 36

    answer_a, answer_b = main(sample)
    print()
    assert (
        answer_a == sample_a_answer
    ), f"AnswerA incorrect: Actual: {answer_a}, Expected: {sample_a_answer}"
    print("sampleA correct")
    if answer_b:
        assert (
            answer_b == sample_b_answer
        ), f"AnswerB incorrect: Actual: {answer_b}, Expected: {sample_b_answer}"
        print("sampleB correct")

    RULES.clear()
    TOTAL_COUNT = 0
    # Test on your input and submit
    answer_a, answer_b = main(input)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    try:
        submit_answer(answer_a, "a")
    except AocdError:
        submit_answer(answer_b, "b")

    print()
