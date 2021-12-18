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
from math import floor, ceil

def parse(filename: str) -> str:
    with open(filename, "r") as f:
        strings = f.readlines()

    return strings


class Node:

    def __init__(self, string, left, right, parent, depth):
        self.left, self.right = None, None
        self.string = string
        self.parent = parent
        self.depth = depth
        if string:
            self.build_from_string(string)
            print()
        else:
            self.left: Union[Node, int] = left
            self.right: Union[Node, int] = right
        if self.depth == 3:
            self.check()
        print()


    def build_from_string(self, string):
        print(string)
        print(self.depth)
        if self.parent:
            print(self.parent.string)
        split_idx = get_split_idx(string)
        if not split_idx:
            if self.parent.left == self:
                self.parent.left = int(string)
            else:
                self.parent.right = int(string)
        else:
            left_str, right_str = string[1:split_idx], string[split_idx + 1: -1]
            self.left = Node(left_str, None, None, self, self.depth + 1)
            self.right = Node(right_str, None, None, self, self.depth + 1)

    def explode(self):
        if self.parent.right == self:
                self.parent.left = int(self.right) if not self.parent.left else self.parent.left + int(self.right)
                self.parent.right = 0
        else:
            self.parent.left = 0
            self.parent.right = int(self.left) if not self.parent.right else self.parent.right + int(
                self.left)
        return self.parent.check()

    def check(self):
        if not self.parent:
            return self
        elif self.depth == 4:
            self.explode()
        elif type(self.right) == int and self.right >= 10:
            self.right = self.split(self.right)
            self.right.check()
        elif type(self.left) == int and self.left >= 10:
            self.left = self.split(self.left)
            self.left.check()

    def split(self, val: int):
        assert type(val) == int
        return Node(None, floor(val // 2), ceil(val // 2), self, self.depth + 1)
#
# def evaluate(string, depth):
#     split_idx = get_split_idx(string)
#     if not split_idx:
#         return string
#     else:
#         string1, string2 = string[1:split_idx], string[split_idx + 1: -1]
#         if depth == 3:
#
#



    
    

def get_split_idx(string):
    if string.isdigit():
        return None
    opening_brackets_stack = []
    closing_brackets_stack = []
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

    assert(len(comma_idx) == 1)
    return comma_idx[0]
    # raise Exception ("No split found")























def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    strings = parse(filename)
    x = Node(strings[0], None, None, None, 0)
    # answer_a = ver_count
    # answer_b = val
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
