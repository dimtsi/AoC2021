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
    Union,
    Generator,
)
from copy import deepcopy
import re


def parse(filename: str) -> str:
    with open(filename, "r") as f:
        string = f.read().strip()

    bin_repr = []
    for char in string:
        bin_repr.append(char_to_bin(char))
    return "".join(bin_repr)


def char_to_bin(char) -> str:
    scale = 16
    num_of_bits = 4
    bin_str = bin(int(char, scale))[2:].zfill(num_of_bits)
    return bin_str


def bin_to_int(bin_str: str) -> int:
    return int(bin_str, 2)


def evaluate(vals: List[int], id: int) -> int:
    vals = list(map(int, vals))
    if id == 0:
        return sum(vals)
    elif id == 1:
        return reduce(lambda x, y: x * y, vals)
    elif id == 2:
        return min(vals)
    elif id == 3:
        return max(vals)
    elif id == 5:
        assert len(vals) == 2
        return 1 if vals[0] > vals[1] else 0
    elif id == 6:
        assert len(vals) == 2
        return 1 if vals[0] < vals[1] else 0
    elif id == 7:
        assert len(vals) == 2
        return 1 if vals[0] == vals[1] else 0
    else:
        raise Exception("Wrong id detected")


def parse_fixed_length(
    s: str, start_idx: int, length: int, ver_count: int, id: int
) -> Tuple[int, int, int]:
    final_idx = start_idx + length
    vals = []
    while start_idx < final_idx:
        ver_count, end_idx, val = parse_string(s, start_idx, ver_count)
        start_idx = end_idx
        vals.append(val)
    result = evaluate(vals, id)
    return ver_count, end_idx, result


def parse_n_packets(
    s: str, start_idx: int, n_packets: int, ver_count: int, id: int
) -> Tuple[int, int, int]:
    count = 0
    vals = []
    while count < n_packets:
        ver_count, end_idx, val = parse_string(s, start_idx, ver_count)
        start_idx = end_idx
        count += 1
        vals.append(val)
    result = evaluate(vals, id)
    return ver_count, end_idx, result


def parse_operator(
    s: str, start_idx: int
) -> Tuple[Optional[int], Optional[int]]:
    subpacket_len, n_subpackets = None, None

    if s[start_idx] == "0":
        subpacket_len = bin_to_int(s[start_idx + 1 : start_idx + 16])
    if s[start_idx] == "1":
        n_subpackets = bin_to_int(s[start_idx + 1 : start_idx + 12])
    return subpacket_len, n_subpackets


def parse_literal(
    s: str, start_idx: int, version_sum: int
) -> Tuple[int, int, int]:
    literal_l = []
    i = start_idx
    while True:
        if s[i] == "1":
            literal_l.append(s[i + 1 : i + 5])
            i += 5
        else:
            literal_l.append(s[i + 1 : i + 5])
            i += 5
            break
    end_idx = i

    literal_s: str = "".join(literal_l)
    literal_int = bin_to_int(literal_s)
    return literal_int, end_idx, version_sum


def parse_string(
    s: str, start_idx: int, version_sum: int
) -> Tuple[int, int, int]:
    version = bin_to_int(s[start_idx : start_idx + 3])
    version_sum += version
    id = bin_to_int(s[start_idx + 3 : start_idx + 6])

    if id != 4:
        l, n_sub = parse_operator(s, start_idx + 6)
        if l:
            version_sum, end_idx, val = parse_fixed_length(
                s, start_idx + 6 + 1 + 15, l, version_sum, id
            )
        elif n_sub:
            version_sum, end_idx, val = parse_n_packets(
                s, start_idx + 6 + 1 + 11, n_sub, version_sum, id
            )
    else:
        val, end_idx, version_sum = parse_literal(
            s, start_idx + 6, version_sum
        )

    return version_sum, end_idx, val


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    s = parse(filename)
    ver_count, end_idx, val = parse_string(s, 0, 0)
    answer_a = ver_count
    answer_b = val
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 20
    sample_b_answer = 1

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
