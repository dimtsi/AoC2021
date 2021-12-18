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


def parse(filename: str) -> str:
    with open(filename, "r") as f:
        strings = f.read().strip().split("\n")

    return strings


def check_for_explode(
    string,
) -> Tuple[bool, Tuple[Optional[int], Optional[int]]]:
    opening_brackets_stack = []
    is_explode = False
    explode_start = None
    explode_end = None
    for i, char in enumerate(string):
        if char == "[":
            opening_brackets_stack.append(char)
            if len(opening_brackets_stack) == 5:
                explode_start = i
                is_explode = True
                continue
        elif char == "]":
            opening_brackets_stack.pop()
            if is_explode:
                explode_end = i
                break

    return is_explode, (explode_start, explode_end)


def reformat_given_explode(string: str, span: Tuple[int, int]) -> str:
    # Get exploding tuple values
    left, right = re.findall("\d+", string[span[0] : span[1]])
    new_str = ""
    # Replace exploded with 0
    string = string[: span[0]] + "0" + string[span[1] + 1 :]
    # string = string[:span[0]]
    prev_num: re.Match = list(re.finditer("\d+", string[0 : span[0]]))
    next_num: re.Match = list(re.finditer("\d+", string[span[0] + 1 :]))

    if not prev_num and next_num:
        next_num = next_num[0]
        new_str = (
            string[: next_num.start() + span[0] + 1]
            + f"{int(next_num.group()) + int(right)}"
            + string[span[0] + 1 + next_num.end() :]
        )
    elif prev_num and not next_num:
        prev_num = prev_num[-1]
        new_str += (
            string[: prev_num.start()]
            + f"{int(prev_num.group()) + int(left)}"
            + string[prev_num.end() :]
        )

    else:
        prev_num, next_num = prev_num[-1], next_num[0]
        new_str = (
            string[: prev_num.start()]
            + f"{int(prev_num.group()) + int(left)}"
            + string[prev_num.end() : next_num.start() + span[0] + 1]
            + f"{int(next_num.group()) + int(right)}"
            + string[span[0] + 1 + next_num.end() :]
        )
    return new_str


def split_check_and_reformat(string) -> Tuple[bool, str]:
    nums = list(re.finditer("\d+", string))
    for num in nums:
        val, span = int(num.group()), num.span()
        if val >= 10:
            replacement = f"[{floor(val / 2)},{ceil(val / 2)}]"
            new_string = string[: span[0]] + replacement + string[span[1] :]
            return True, new_string
    return False, ""


def reduce(string):
    is_exploding, explode_span = check_for_explode(string)
    if is_exploding:
        string = reformat_given_explode(string, explode_span)
        string = reduce(string)
    is_split, split_string = split_check_and_reformat(string)
    if is_split:
        string = split_string
        string = reduce(string)
    return string


def addition(strings: List[str]):
    first = strings.pop(0)

    while strings:
        second = strings.pop(0)
        full = "[" + first + "," + second + "]"
        first = reduce(full)
    return evaluate_expression(first)


def evaluate_expression(string):
    split_idx = get_split_idx(string)
    if not split_idx:
        return int(string)
    string1 = string[1:split_idx]
    string2 = string[split_idx + 1 : -1]

    return 3 * evaluate_expression(string1) + 2 * evaluate_expression(string2)


def get_split_idx(string):
    if string.isdigit():
        return None
    opening_brackets_stack = []
    comma_idx = []
    for i, char in enumerate(string[1:-1], 1):
        if i == len(string) - 1:
            break
        elif char == "[":
            opening_brackets_stack.append(char)
        elif char == "]":
            opening_brackets_stack.pop()
            comma_idx.pop()
        elif char == ",":
            comma_idx.append(i)

    assert len(comma_idx) == 1
    return comma_idx[0]
    raise Exception("No split found")


def get_pair_with_max_addition(strings: List[str]) -> int:
    max_score = 0
    for s1 in strings:
        for s2 in strings:
            if s1 == s2:
                continue
            score = addition([s1, s2])
            if score > max_score:
                max_score = score
    return max_score


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    strings = parse(filename)
    addition_score = addition(strings)
    # reduce(strings[0])
    strings = parse(filename)
    max_pair_score = get_pair_with_max_addition(strings)
    # x = Node(strings[0], None, None, None, 0)
    answer_a = addition_score
    answer_b = max_pair_score
    # answer_b = val
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 4140
    sample_b_answer = 3993

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
