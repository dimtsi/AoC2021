from collections import Counter, defaultdict, deque
from typing import (
    List,
    Tuple,
    Set,
    Dict,
    Iterable,
    DefaultDict,
    Iterator,
)
from functools import reduce


OPENING_BRACKETS = {"(", "[", "{", "<"}
CLOSING_BRACKETS = {")", "]", "}", ">"}

MATCH = {")": "(", "]": "[", "}": "{", ">": "<"}


def parse(filename: str) -> List[str]:
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
    return lines


def get_corruption_score(corrupted_breakpoint_chars: List[str]) -> int:
    """
    :param corrupted_breakpoint_chars: List of characters that first mismatch
        All elements in the list are strings of length 1 and contain only
        closing brackets.
    """

    corrupted_chars_score = {")": 3, "]": 57, "}": 1197, ">": 25137}

    total_corruption_score = 0
    for char in corrupted_breakpoint_chars:
        total_corruption_score += corrupted_chars_score[char]
    return total_corruption_score


def find_corrupted_and_incomplete(
    strings: List[str],
) -> Tuple[List[str], List[List[str]]]:

    corrupted_breakpoint_chars: List[str] = []
    incomplete_opened: List[List[str]] = []

    for string in strings:
        is_corrupted = False
        opening_brackets_stack = []
        for char in string:
            if char in OPENING_BRACKETS:
                opening_brackets_stack.append(char)
            elif char in CLOSING_BRACKETS:
                if opening_brackets_stack.pop() != MATCH[char]:
                    is_corrupted = True
                    corrupted_breakpoint_chars.append(char)
                    break

        # complete matches are already popped in the loop so we can use them
        # to get the incomplete_openings
        if opening_brackets_stack and not is_corrupted:
            incomplete_opened.append(opening_brackets_stack)

    return corrupted_breakpoint_chars, incomplete_opened


def calc_incomplete_stack_score(stack: Iterator[str]) -> int:
    missing_chars_score = {")": 1, "]": 2, "}": 3, ">": 4}
    score = 0

    for char in stack:
        score *= 5
        score += missing_chars_score[char]
    return score


def get_incomplete_score(incomplete_opened: List[List[str]]) -> int:
    """
    Order is important for calculating the score and the function inputs are
    unmatched opening characters. So we have to reverse and match to closing

    :param incomplete_opened: Calculated in the previous steps. Each element
        in the input list is a list of the unmatched opening characters
        calculated in the first step for the incomplete inputs.
    """

    rev_match = {v: k for k, v in MATCH.items()}

    closing_stacks = []
    for stack in incomplete_opened:
        rev_stack = reversed(stack)
        rev_stack = [rev_match[x] for x in rev_stack]  # type: ignore
        closing_stacks.append(rev_stack)
    incomp_scores = [
        calc_incomplete_stack_score(stack) for stack in closing_stacks
    ]

    total_inc_score = sorted(incomp_scores)[len(incomp_scores) // 2]
    return total_inc_score


if __name__ == "__main__":
    from time import time

    start = time()
    sample = "sample.txt"
    input = "input.txt"

    inp = input
    start = time()
    lines = parse(inp)

    corrupted_breakpoint_chars, incomplete = find_corrupted_and_incomplete(
        lines
    )
    corruption_score = get_corruption_score(corrupted_breakpoint_chars)
    print(f"p1: {corruption_score}")
    # p2
    incomplete_score = get_incomplete_score(incomplete)
    end = time()
    print(f"p2: {incomplete_score}")
    print(end - start)
