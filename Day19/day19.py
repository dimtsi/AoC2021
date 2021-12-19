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
import numpy as np







def parse(filename):
    sample=True if "sample" in filename else False

    scanners_lst: List[Scanner] = []

    with open(filename, 'r') as f:
        scanners: List[str] = f.read().rstrip().split("\n\n")

    for scanner in scanners:
        beacons = []
        for i, line in enumerate(scanner.split("\n")):
            if i == 0:
                id = int(re.findall("\d+", line)[0])
            else:
                beacons.append(list(map(int,line.strip().split(","))))
        beacons = np.array(beacons)
        scanners_lst.append(Scanner(id, beacons, sample))
    return scanners_lst


class Scanner:
    orientations: List[np.ndarray]

    def __init__(self, id: int, array: np.ndarray, sample=False):
        self.id = id
        self.base = array
        self.found_orientation = False
        self.rotations: List[np.ndarray] = []
        self.sample = sample
        # self.get_orientations()
        # self.orientations_with_border = {}

    @classmethod
    def rotate(cls, image: np.ndarray):
        new_image = np.rot90(image)
        return new_image

    def update_final(self, val):
        if not self.final:
            self.final = val
            self.final_change_count += 1
        elif self.final != val:
            raise Exception("Trying to Change final orientation")



    def get_orientations(self):
        orientations = []
        rotation = self.base
        for i in range(4):
            rotation = np.rot90(rotation)
            orientations.append(rotation)
        self.orientations = orientations
        # if self.sample:
        #     assert self.match_orientations_for_sample(), f"Match not found for sample with id {self.id}"



def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    scanners = parse(filename)
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
