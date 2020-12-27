# https://adventofcode.com/{{ year }}/day/{{ day }}

import sys
from pathlib import Path

import pytest

from utils import read_numbers

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'


def part1(dataset: Path):
    numbers = list(read_numbers(dataset))
    loops = {}
    v = 1
    iteration = 0
    while numbers:
        iteration += 1
        v *= 7
        v %= 20201227
        if v in numbers:
            numbers.remove(v)
            loops[v] = iteration
    subject = loops.popitem()[0]
    additional_iterations = loops.popitem()[1]

    v = 1
    for _ in range(additional_iterations):
        v *= subject
        v %= 20201227
    print(v)


def part2(dataset: Path):
    pass


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)
    else:
        pytest.main([__file__])


if __name__ == '__main__':
    main()
