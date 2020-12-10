# https://adventofcode.com/2020/day/9

import sys
from pathlib import Path

from utils import read_numbers

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'


def is_correct_value(value, buffer):
    for i, v1 in enumerate(buffer):
        for j, v2 in enumerate(buffer):
            if i != j and v1 + v2 == value:
                return True
    return False


def find_first_invalid_value(numbers):
    buffer = numbers[:25]
    for value in numbers[25:]:
        if not is_correct_value(value, buffer):
            return value
        buffer.pop(0)
        buffer.append(value)
    assert False, 'at least one value must be invalid'


def part1(dataset: Path):
    numbers = list(read_numbers(dataset))
    print(find_first_invalid_value(numbers))


def part2(dataset: Path):
    numbers = list(read_numbers(dataset))
    invalid = find_first_invalid_value(numbers)
    for i in range(len(numbers) - 1):
        sequence = []
        while sum(sequence, 0) < invalid:
            sequence.append(numbers[i])
            i += 1
        if sum(sequence) == invalid:
            print(min(sequence) + max(sequence))
            return


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)


if __name__ == '__main__':
    main()
