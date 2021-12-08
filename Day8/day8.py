from collections import Counter
import re



from collections import Counter, defaultdict
import re
from copy import deepcopy
from typing import List, Tuple, Set, Dict

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
    9: "abcdfg"

}
ORIGINAL_SETS = {k: set(v) for k, v in ORIGINAL_SEGMENTS.items()}
ORIGINAL_STR_TO_NUMS = {"".join(sorted(v)): k for k, v in ORIGINAL_SETS.items()}
print()


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


def find_pair_mapping(segments):
    len_map_original = defaultdict(set)
    visited = set()
    for i in segments:
        for j in segments:
            if len(i) == len(j):
                continue
            diff = set(i) - set(j)
            if len(diff) == 1:
                len_map_original[tuple(sorted([len(i), len(j)]))].add(list(diff)[0])
    return eliminate(len_map_original)


def eliminate(map: Dict[Tuple, Set]):
    eliminated = set()
    eliminated_tuples = set()
    new_tuple_map = defaultdict(set)
    while len(eliminated) < 6:
        for k, v in map.items():
            if not v or k in eliminated_tuples:
                continue
            elif len(v) == 1:
                eliminated.add(list(v)[0])
                eliminated_tuples.add(k)
                new_tuple_map[k].update(v)
        for key in map:
                map[key] -= eliminated
    return new_tuple_map


def get_final_mapping(pair_mapping_original, pair_mapping_new):
    new_map = {}

    for key in pair_mapping_original.keys():
        if not key in pair_mapping_new:
            raise "no key found"
        val_orig = list(pair_mapping_original[key])[0]
        val_new = list(pair_mapping_new[key])[0]

        new_map[val_new] = val_orig
    missing_old = (set("abcdefg") - set(new_map.values())).pop()
    missing_new = (set("abcdefg") - set(new_map.keys())).pop()
    new_map[missing_new] = missing_old
    return new_map


def map_new_string_to_old_number(string, letter_mapping):
    new_repr = "".join(sorted(map(lambda x: letter_mapping[x], list(string))))
    num = ORIGINAL_STR_TO_NUMS[new_repr]
    return num


def display_outputs(digits: Set, displayed, original_pair_mapping):
    new_mapping = find_new_cand(digits, original_pair_mapping)
    displayed_numbers = []
    for disp in displayed:
        displayed_numbers.append(new_mapping["".join(sorted(disp))])
    return(int("".join([str(i) for i in displayed_numbers])))


def find_new_cand(digits: Set, original_pair_mapping):
    from copy import deepcopy

    digit_lens = defaultdict(set)
    for d in digits:
        digit_lens[len(d)].add(d)
    digits = sorted(digits, key=len)

    new_pair_mapping = find_pair_mapping(digits)

    new_letter_mapping = get_final_mapping(original_pair_mapping, new_pair_mapping)

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

    digits, displays = parse(inp)

    ordered_original = sorted(ORIGINAL_SEGMENTS.items(),
                              key=lambda x: len(x[1]))

    original_pair_mapping = find_pair_mapping(ORIGINAL_SEGMENTS.values())
    final = [display_outputs(dig, disp, original_pair_mapping) for dig, disp in zip(digits, displays)]
    print(sum(final))