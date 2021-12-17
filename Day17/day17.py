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
import sys


class Trajectory:

    
    def __init__(self, points: List[int]):
        self.points = points
        self.min_x = points[0]
        self.max_x = points[1]
        self.min_y = points[2]
        self.max_y = points[3]

    def __contains__(self, point) -> bool:
        if self.min_x <= point[0] <= self.max_x and self.min_y <= point[1] <= self.max_y:
            return True
        return False


class Experiment:
    is_terminated: bool = False
    success: bool = False
    high_point: List[int] = [0, 0]
    
    def __init__(self, velocity: List[int], trajectory: Trajectory):
        self.v = list(velocity)
        self.traj = trajectory
        self.pos = [0, 0]
    
    def run(self) -> Tuple[bool, List[int], List[int], List[int]]:
        while True:
            self.step()
            if self.is_terminated:
                break
        return self.success, self.high_point, self.pos, self.v

    def step(self):
        if self.v[1] == 0:
            self.high_point = self.pos[:]
        self.pos = self.pos[0] + self.v[0], self.pos[1] + self.v[1]
        self.v[1] += -1
        if self.v[0] > 0:
            self.v[0] -= 1
        elif self.v[0] < 0:
            self.v[0] += 1
        self.check_terminate()

    def check_terminate(self) -> None:
        if self.pos in self.traj:
            self.is_terminated = True
            self.success = True
        elif self.pos[1] < self.traj.min_y:
            self.is_terminated = True
            self.success = False
        elif self.pos[0] > self.traj.max_x:
            self.is_terminated = True
            self.success = False


def parse(filename: str) -> Trajectory:
    with open(filename, "r") as f:
        lines = f.read().strip()
        points = list(map(int, re.findall("-?\d+", lines)))
    return Trajectory(points)


def run_experiment(trajectory: Trajectory) -> Tuple[int, int]:
    max_height = -sys.maxsize
    counts = 0

    for i in range(1, trajectory.max_x + 1):
        for j in range(trajectory.min_y, 1000):
            v = [i, j]
            exp = Experiment(v, trajectory)
            success, highpoint, end_pos, end_v = exp.run()
            if success:
                counts += 1
                if highpoint[1] > max_height:
                    max_height = highpoint[1]

    return max_height, counts


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    trajectory = parse(filename)
    answer_a, answer_b = run_experiment(trajectory)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 45
    sample_b_answer = 112

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
