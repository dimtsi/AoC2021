from typing import List, Tuple


def parse(filename: str) -> List[str]:

    with open(filename, "r") as f:
        lines = f.read().split("\n")

        return lines


def count_zeros_ones(l: List[str]) -> Tuple[List[int], List[int]]:
    size = len(l[0])
    ones = [0] * size
    zeros = ones[:]

    for line in l:
        for i in range(size):
            if int(line[i]) == 0:
                zeros[i] += 1
            else:
                ones[i] += 1
    return zeros, ones


def calculate_gamma_epsilon(
    zero_totals: List[int], one_totals: List[int]
) -> int:
    gamma = ""
    epsilon = ""
    for zero_cnt, one_cnt in zip(zero_totals, one_totals):
        if zero_cnt > one_cnt:
            gamma += "0"
            epsilon += "1"
        else:
            gamma += "1"
            epsilon += "0"
    gamma_dec = int(gamma, 2)
    epsilon_dec = int(epsilon, 2)
    return gamma_dec * epsilon_dec


# p2
def count_zeros_ones_at_k(
    l: List[str], idx: int
) -> Tuple[int, int, List[str], List[str]]:
    ones = 0
    zeros = 0
    ones_l = []
    zeros_l = []
    for line in l:
        if int(line[idx]) == 0:
            zeros += 1
            zeros_l.append(line)
        else:
            ones += 1
            ones_l.append(line)
    return zeros, ones, zeros_l, ones_l


def get_oxygen(l: List[str], idx: int) -> List[str]:
    zeros, ones, zeros_l, ones_l = count_zeros_ones_at_k(l, idx)
    if zeros > ones:
        candidates_ox = zeros_l
    else:
        candidates_ox = ones_l
    while len(candidates_ox) > 1:
        candidates_ox = get_oxygen(candidates_ox, idx + 1)
    return candidates_ox


def get_co2(l: List[str], idx: int) -> List[str]:
    zeros, ones, zeros_l, ones_l = count_zeros_ones_at_k(l, idx)
    if ones >= zeros:
        candidates_co2 = zeros_l
    else:
        candidates_co2 = ones_l
    while len(candidates_co2) > 1:
        candidates_co2 = get_co2(candidates_co2, idx + 1)
    return candidates_co2


def calc_life_support(ox, co2):
    ox = int(ox, 2)
    co2 = int(co2, 2)
    return ox * co2


if __name__ == "__main__":

    sample = "sample.txt"
    input = "input.txt"
    bits: List[str] = parse(input)
    zeros, ones = count_zeros_ones(bits)
    power = calculate_gamma_epsilon(zeros, ones)
    print(f"p1: {power}")
    bits: List[str] = parse(input)
    ox = get_oxygen(bits, 0)
    co2 = get_co2(bits, 0)
    life_support = calc_life_support(ox[0], co2[0])
    print(f"p2: {life_support}")
