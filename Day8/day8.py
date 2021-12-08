from collections import Counter
import re


from collections import Counter, defaultdict
from typing import (
    List,
    Tuple,
    Set,
    Dict,
    Iterable,
    DefaultDict,
)

ORIGINAL_SEGMENTS = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}

ORIGINAL_SETS = {k: set(v) for k, v in ORIGINAL_SEGMENTS.items()}
ORIGINAL_STR_TO_NUMS = {
    "".join(sorted(v)): k for k, v in ORIGINAL_SETS.items()
}


ORIGINAL_LENGTHS = defaultdict(set)
for k, v in ORIGINAL_SEGMENTS.items():
    ORIGINAL_LENGTHS[len(v)].add(k)

UNIQUE_LENS = [len(ORIGINAL_SEGMENTS[i]) for i in [1, 4, 7, 8]]


def parse(filename: str) -> Tuple[List[List], List[List]]:
    with open(filename, "r") as f:
        lines = f.read()
        if "sample" in filename:
            lines = lines.replace("|\n", "| ")
    digits = []
    displays = []
    for line in lines.split("\n"):
        digit, disp = line.split(" | ")
        digits.append(digit.split(" "))
        displays.append(disp.split(" "))
    return digits, displays


def count_unique(outputs):
    count = 0
    for output in outputs:
        if len(output) in UNIQUE_LENS:
            count += 1
    return count


def find_pair_mapping(digits_reprs: Iterable[str]):
    """
    This function will match pairs of lengths of
    representations and their differnces in terms of characters.
    Initially there might be multiple possible values for 1 char difference.
    e.g (6, 7) -> {"a", "b"} if there are two different sets of length 6 and 7
    respectively that have a value one.

    In the end we will take the created pairs and corresponding
    potential one char differences and eliminate one by one
    until each pair can have a difference of a single character

    """
    pair_map: DefaultDict[Tuple[int, int], Set[str]] = defaultdict(set)
    for i in digits_reprs:
        for j in digits_reprs:
            diff = set(i) - set(j)
            if len(diff) == 1:
                sorted_tup: Tuple[int, int] = tuple( # type: ignore
                    sorted([len(i), len(j)])
                )  # sort key tuple to avoid mismatch with originals later
                pair_map[sorted_tup].add(list(diff)[0])  # type: ignore
    return eliminate(pair_map)


def eliminate(pair_map: DefaultDict[Tuple[int, int], Set[str]]):
    eliminated: Set[str] = set()
    eliminated_tuples = set()
    map_pair_to_char = {}
    while len(eliminated) < 6:
        for k, v in pair_map.items():
            if not v or k in eliminated_tuples:
                continue
            elif len(v) == 1:
                val = list(v)[0] # pop unique value from set
                eliminated.add(val)
                eliminated_tuples.add(k)
                map_pair_to_char[k] = val
        for key in pair_map:
            if pair_map[key]:  # If not empty set
                pair_map[key] -= eliminated
    return map_pair_to_char


def get_final_mapping(
    pair_mapping_original: Dict[Tuple[int, int], str],
    pair_mapping_new: Dict[Tuple[int, int], str],
):
    new_map = {}

    for key in pair_mapping_original.keys():
        if not key in pair_mapping_new:
            raise Exception("no key found")
        val_orig = pair_mapping_original[key]
        val_new = pair_mapping_new[key]

        new_map[val_new] = val_orig
    missing_old = (set("abcdefg") - set(new_map.values())).pop()
    missing_new = (set("abcdefg") - set(new_map.keys())).pop()
    new_map[missing_new] = missing_old
    return new_map


def map_new_string_to_old_number(string, letter_mapping):
    new_repr = "".join(sorted(map(lambda x: letter_mapping[x], list(string))))
    num = ORIGINAL_STR_TO_NUMS[new_repr]
    return num


def display_outputs(digits: Iterable[str], displayed, original_pair_mapping):
    new_mapping = find_new_cand(digits, original_pair_mapping)
    displayed_numbers = []
    for disp in displayed:
        displayed_numbers.append(new_mapping["".join(sorted(disp))])
    return int("".join([str(i) for i in displayed_numbers]))


def find_new_cand(digits: Iterable[str], original_pair_mapping):

    digit_lens = defaultdict(set)
    for d in digits:
        digit_lens[len(d)].add(d)

    new_pair_mapping = find_pair_mapping(digits)
    new_letter_mapping = get_final_mapping(
        original_pair_mapping, new_pair_mapping
    )
    new_num_mapping: Dict[str, int] = {}

    for digit in digits:
        new_num = map_new_string_to_old_number(digit, new_letter_mapping)
        new_num_mapping["".join(sorted(digit))] = new_num
    return new_num_mapping


if __name__ == "__main__":
    from time import time

    start = time()
    sample = "sample.txt"
    sample2 = "sample2.txt"

    input = "input.txt"

    inp = input
    start = time()
    digits, displays = parse(inp)

    unique_count = sum([count_unique(output) for output in displays])
    print(f"p1: {unique_count}")
    # p2
    digits, displays = parse(inp)

    original_pair_mapping = find_pair_mapping(ORIGINAL_SEGMENTS.values())
    final = [
        display_outputs(dig, disp, original_pair_mapping)
        for dig, disp in zip(digits, displays)
    ]
    print(f"p2: {sum(final)}")
