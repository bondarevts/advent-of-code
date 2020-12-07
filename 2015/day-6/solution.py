# https://adventofcode.com/2015/day/6

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'
FIELD_SIZE = 1000


@dataclass
class Command:
    name: str
    top: int
    bottom: int
    left: int
    right: int


def read_commands(path: Path) -> Iterable[Command]:
    pattern = re.compile(r'(turn off|turn on|toggle) (\d+),(\d+) through (\d+),(\d+)')
    with open(path) as dataset:
        for line in dataset:
            match = pattern.match(line)
            name, *coordinates = match.groups()
            top, left, bottom, right = map(int, coordinates)
            yield Command(name, top=top, bottom=bottom, left=left, right=right)


def total_sum_after_commands(commands_path, operations):
    field = [[0] * FIELD_SIZE for _ in range(FIELD_SIZE)]

    for command in read_commands(commands_path):
        operation = operations[command.name]
        for i in range(command.top, command.bottom + 1):
            for j in range(command.left, command.right + 1):
                field[i][j] = operation(field[i][j])

    return sum(sum(line) for line in field)


def part1():
    print(total_sum_after_commands(DATASET_PATH, operations={
        'turn on': lambda x: 1,
        'turn off': lambda x: 0,
        'toggle': lambda x: x ^ 1,
    }))


def part2():
    print(total_sum_after_commands(DATASET_PATH, operations={
        'turn on': lambda x: x + 1,
        'turn off': lambda x: max(x - 1, 0),
        'toggle': lambda x: x + 2,
    }))


def main():
    if sys.argv[1] == '1':
        part1()
    else:
        part2()


if __name__ == '__main__':
    main()
