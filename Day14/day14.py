from collections import Counter, defaultdict, deque
from functools import reduce, lru_cache
from typing import (
    List,
    Tuple,
    Set,
    Dict,
    Iterable,
    DefaultDict,
    Optional,
)
from copy import deepcopy
import re


def parse(filename: str):

    with open(filename, "r") as f:
        rules = {}
        string_raw, rules_raw = f.read().strip().split("\n\n")

        for rule in rules_raw.split("\n"):
            k, v = rule.split(" -> ")
            rules[k] = v
    return string_raw, rules


def solve(rules: Dict[str, str], string: str, n_steps: int) -> int:

    # count rule occurences in original string
    rule_counts: DefaultDict[str, int] = defaultdict(lambda: 0)

    for rule in rules:
        rule_counts[rule] = len(re.findall(f"(?={rule})", string))

    updated_rule_counts = deepcopy(rule_counts)

    for _ in range(n_steps):
        for rule in rules:
            transformation = rules[rule]
            result_1, result_2 = (
                rule[0] + transformation,
                transformation + rule[1],
            )

            updated_rule_counts[result_1] += rule_counts[rule]
            updated_rule_counts[result_2] += rule_counts[rule]
            updated_rule_counts[rule] -= rule_counts[rule]

        rule_counts = deepcopy(updated_rule_counts)

    return get_max_min_char_diff_from_rule_counts(rule_counts)


def get_max_min_char_diff_from_rule_counts(
    rule_counts: DefaultDict[str, int]
) -> int:

    elem_counts: DefaultDict[str, int] = defaultdict(lambda: 0)

    for rule, count in rule_counts.items():
        ch1, ch2 = rule[0], rule[1]
        elem_counts[ch1] += count
        elem_counts[ch2] += count

    max_elem = max(elem_counts, key=elem_counts.get)
    min_elem = min(elem_counts, key=elem_counts.get)

    max_elem_count = (
        elem_counts[max_elem] // 2
        if elem_counts[max_elem] % 2 == 0
        else elem_counts[max_elem] // 2 + 1
    )
    min_elem_count = (
        elem_counts[min_elem] // 2
        if elem_counts[min_elem] % 2 == 0
        else elem_counts[min_elem] // 2 + 1
    )
    return max_elem_count - min_elem_count


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    string, rules = parse(filename)

    answer_a = solve(rules, string, 10)
    answer_b = solve(rules, string, 40)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 1588
    sample_b_answer = 2188189693529

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
