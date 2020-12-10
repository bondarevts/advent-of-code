# https://adventofcode.com/2020/day/10

import sys
from collections import Counter
from pathlib import Path
from typing import Iterable

from utils import read_numbers

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'


def all_jolts(path: Path) -> Iterable[int]:
    yield 0
    max_jolts = 0
    for value in read_numbers(path):
        yield value
        if value > max_jolts:
            max_jolts = value
    yield max_jolts + 3


def diff_1_and_3_counts(dataset):
    values = sorted(all_jolts(dataset))
    diffs = list(b - a for a, b in zip(values, values[1:]))
    diff_counts = Counter(diffs)
    return diff_counts[1], diff_counts[3]


def combinations_count(values):
    values = sorted(values)
    combinations = [1]
    for i, value in enumerate(values[1:], start=1):
        combinations.append(sum(
            combinations[j]
            for j in range(max(0, i - 3), i)
            if values[i] - values[j] <= 3
        ))
    return combinations


def part1(dataset: Path):
    diff1, diff3 = diff_1_and_3_counts(dataset)
    print(diff1 * diff3)


def part2(dataset: Path):
    combinations = combinations_count(all_jolts(dataset))
    print(combinations[-1])


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)
    else:
        test()


def test():
    assert diff_1_and_3_counts(ROOT / 'test-dataset-1.txt') == (7, 5)
    assert diff_1_and_3_counts(ROOT / 'test-dataset-2.txt') == (22, 10)
    assert combinations_count(all_jolts(ROOT / 'test-dataset-1.txt'))[-1] == 8
    assert combinations_count(all_jolts(ROOT / 'test-dataset-2.txt'))[-1] == 19208


if __name__ == '__main__':
    main()
