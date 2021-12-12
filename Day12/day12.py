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
PATHS_TO_END: Set[Tuple[str, ...]] = set()


def parse(filename: str) -> None:
    global RULES

    with open(filename, "r") as f:
        for line in f.read().strip().split("\n"):
            source, dest = line.split("-")
            RULES[source].add(dest)
            RULES[dest].add(source)


def find_path(curr_path: List[str], freeze: bool = False, p2: bool = False):

    curr_node = curr_path[-1]

    if (
        p2
        and not freeze
        and curr_node.islower()
        and Counter(curr_path)[curr_node] == 2
    ):
        freeze = True
    if curr_node == "end":
        PATHS_TO_END.add(tuple(curr_path))
    else:
        for connection in RULES[curr_node]:
            if connection.islower() and connection in curr_path:
                if p2 and not freeze and connection not in {"start", "end"}:
                    find_path(curr_path + [connection], freeze=freeze, p2=p2)
                else:
                    continue
            find_path(curr_path + [connection], freeze=freeze, p2=p2)


def main(filename: str) -> Tuple[int, int]:
    from time import time

    start = time()
    parse(filename)
    find_path(["start"])
    answer_a = len(PATHS_TO_END)

    # p2
    PATHS_TO_END.clear()
    find_path(["start"], freeze=False, p2=True)
    answer_b = len(PATHS_TO_END)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample3.txt"
    input = "input.txt"

    sample_a_answer = 226
    sample_b_answer = 3509

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
    PATHS_TO_END.clear()
    # Test on your input and submit
    answer_a, answer_b = main(input)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    try:
        submit_answer(answer_a, "a")
    except AocdError:
        submit_answer(answer_b, "b")

    print()
