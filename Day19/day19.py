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
from itertools import combinations


ROTATIONS = lambda x, y, z: np.array(
    [
        np.array([x, y, z]).T,
        np.array([-y, x, z]).T,
        np.array([-x, -y, z]).T,
        np.array([y, -x, z]).T,
        np.array([-z, y, x]).T,
        np.array([-y, -z, x]).T,
        np.array([z, -y, x]).T,
        np.array([y, z, x]).T,
        np.array([-x, y, -z]).T,
        np.array([-y, -x, -z]).T,
        np.array([x, -y, -z]).T,
        np.array([y, x, -z]).T,
        np.array([z, y, -x]).T,
        np.array([-y, z, -x]).T,
        np.array([-z, -y, -x]).T,
        np.array([y, -z, -x]).T,
        np.array([x, -z, y]).T,
        np.array([z, x, y]).T,
        np.array([-x, z, y]).T,
        np.array([-z, -x, y]).T,
        np.array([x, z, -y]).T,
        np.array([-z, x, -y]).T,
        np.array([-x, -z, -y]).T,
        np.array([z, -x, -y]).T,
    ]
)


def parse(filename):
    sample = True if "sample" in filename else False
    beacons_from_origin: Set[Tuple] = set()
    scanners_lst: List[Scanner] = []

    with open(filename, "r") as f:
        scanners: List[str] = f.read().rstrip().split("\n\n")

    for scanner in scanners:
        beacons = []
        for i, line in enumerate(scanner.split("\n")):
            if i == 0:
                id = int(re.findall("\d+", line)[0])
            else:
                beacons.append(list(map(int, line.strip().split(","))))
        beacons = np.array(beacons)
        scanners_lst.append(Scanner(id, beacons))
    return scanners_lst


class Scanner:
    loc: Optional[Tuple[int, int, int]] = None
    is_ref = False
    beacons_from_origin: Optional[Set[Tuple[int, int, int]]]

    def __init__(self, id: int, array: np.ndarray):
        self.id = id
        self.beacons = array
        self.rotations = self.get_rotations()
        self.distances_pairs = [
            self.get_distances_between_beacons(rot) for rot in self.rotations
        ]

    def get_rotations(self):
        x, y, z = self.beacons.T
        return ROTATIONS(x, y, z)

    @staticmethod
    def get_distances_between_beacons(beacons: np.ndarray):
        dist_to_pair = dict()
        distances = set()
        for a, b in combinations(beacons, 2):
            dist = tuple(a - b)
            distances.add(tuple(a - b))
            dist_to_pair[dist] = [tuple(a), tuple(b)]
        return distances, dist_to_pair

    def align_to_origin(self, ref_scanner, common_point_ref: Tuple[int, int, int], common_point_self: Tuple[int, int, int]):
        origin_a = ref_scanner.loc
        self.loc = tuple(
            [
                a + b - c
                for a, b, c in zip(
                    origin_a, common_point_ref, common_point_self
                )
            ]
        )
        self.beacons_from_origin = set(
            tuple(beacon) for beacon in np.array(self.loc) + self.beacons
        )


def check_if_match_and_align(scanner_a: Scanner, scanner_b: Scanner):

    for i, rot_a in enumerate(scanner_a.rotations):
        if scanner_a.is_ref:
            if i > 0:
                assert False, "Trying to rotate reference scanner"

        distances_a, pairs_a = scanner_a.distances_pairs[i]
        for j, rot_b in enumerate(scanner_b.rotations):
            common_a = set()
            common_b = set()
            distances_b, pairs_b = scanner_b.distances_pairs[j]
            intersect = distances_a & distances_b
            if len(intersect) >= 12:
                for i, dist in enumerate(intersect):
                    if i == 0:  # only one pair for later calculation of origin
                        common_a_single = pairs_a[dist][0]
                        common_b_single = pairs_b[dist][0]
                    common_a.update(pairs_a[dist])
                    common_b.update(pairs_b[dist])
                if len(common_a) < 12 or len(common_b) < 12:
                    continue
                scanner_b.beacons = rot_b
                scanner_b.rotations = [rot_b]
                scanner_b.distances_pairs = [
                    scanner_b.distances_pairs[j]
                ]
                scanner_b.align_to_origin(
                    scanner_a, common_a_single, common_b_single
                )
                return True
    return False


def align_all(scanners: List[Scanner]):
    start = scanners[0]
    start.loc = (0, 0, 0)
    start.beacons_from_origin = set(tuple(beacon) for beacon in start.beacons)

    stack = [start]
    aligned_idx = {0}
    while stack:
        ref = stack.pop()
        unaligned = [
            scanner for scanner in scanners if scanner.id not in aligned_idx
        ]
        for j, cand in enumerate(unaligned):
            assert cand.id != ref.id
            if cand.id in aligned_idx:
                continue
            is_match = check_if_match_and_align(ref, cand)
            if is_match:
                aligned_idx.add(cand.id)
                cand.is_ref = True
                stack.append(cand)
                print(ref.id, cand.id)
    assert len(aligned_idx) == len(scanners)


def get_total_num_of_beacons(scanners: List[Scanner]) -> int:
    all_beacons = set()
    for scanner in scanners:
        all_beacons |= scanner.beacons_from_origin
    return len(all_beacons)


def get_max_manhattan(scanners: List[Scanner]) -> int:
    max_manh = 0
    for scanner_a in scanners:
        for scanner_b in scanners:
            if scanner_a.id == scanner_b.id:
                continue
            a_x, a_y, a_z = scanner_a.loc
            b_x, b_y, b_z = scanner_b.loc
            manh = abs(a_x - b_x) + abs(a_y - b_y) + abs(a_z - b_z)
            max_manh = max([manh, max_manh])
    print(f"max_manh: {max_manh}")
    return max_manh


def calibrate(scanners: List[Scanner]):
    align_all(scanners)
    n_beacons = get_total_num_of_beacons(scanners)
    max_manh = get_max_manhattan(scanners)
    return n_beacons, max_manh


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    scanners = parse(filename)
    answer_a, answer_b = calibrate(scanners)
    # answer_b = val
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 79
    sample_b_answer = 3621

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

    # # Test on your input and submit
    answer_a, answer_b = main(input)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    # try:
    #     submit_answer(answer_a, "a")
    # except AocdError:
    #     submit_answer(answer_b, "b")
