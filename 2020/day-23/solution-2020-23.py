# https://adventofcode.com/{{ year }}/day/{{ day }}

import sys
from collections import deque
from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pytest

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'

MOVE_PER_ROUND = 3


def get_numbers(numbers_string):
    return [v - 1 for v in map(int, numbers_string)]  # 0 based


def run_rounds(numbers, total_rounds):
    circle = CupsCircle(numbers)
    current_value = numbers[0]
    for _ in range(total_rounds):
        current_value = circle.round(current_value)
    return circle


def test_known_case():
    assert result_to_part1_answer(run_rounds(get_numbers('389125467'), 100)) == '67384529'


def result_to_part1_answer(circle):
    start = circle.values[0]
    current = start.next
    values = []
    while current != start:
        values.append(str(current.value + 1))
        current = current.next
    return ''.join(values)


def part1(dataset: Path):
    numbers = get_numbers(dataset.read_text().strip())
    result_numbers = run_rounds(numbers, 100)
    print(result_to_part1_answer(result_numbers))


def test_part2():
    numbers = get_numbers('389125467')
    numbers.extend(range(9, 1_000_000))
    assert len(numbers) == 1_000_000
    assert result_to_part2_answer(run_rounds(numbers, total_rounds=10_000_000)) == 149245887792


def result_to_part2_answer(circle):
    start = circle.values[0]
    n1 = start.next.value + 1
    n2 = start.next.next.value + 1
    return n1 * n2


class Node:
    __slots__ = ('value', 'prev', 'next')

    def __init__(self, value, prev, next):
        self.value = value
        self.prev = prev
        self.next = next


class CupsCircle:
    def __init__(self, initial_values):
        self.values = {}
        for value in initial_values:
            self.values[value] = Node(value, None, None)
        for i, value in enumerate(initial_values):
            self.values[value].prev = self.values[initial_values[i - 1]]
            self.values[value].next = self.values[initial_values[(i + 1) % len(initial_values)]]

    def round(self, current):
        current_node = self.values[current]
        to_move_last = current_node.next.next.next
        destination_node = self._find_destination(current_node)
        first_move_node = current_node.next
        current_node.next = to_move_last.next
        to_move_last.next = destination_node.next
        destination_node.next = first_move_node
        return current_node.next.value

    def _find_destination(self, current_node) -> Node:
        to_move_values = (
            current_node.next.value,
            current_node.next.next.value,
            current_node.next.next.next.value
        )
        destination = (current_node.value - 1) % len(self.values)
        while destination in to_move_values:
            destination = (destination - 1) % len(self.values)
        return self.values[destination]

    def __len__(self):
        return len(self.values)


def part2(dataset: Path):
    numbers = get_numbers(dataset.read_text().strip())
    numbers.extend(range(9, 1_000_000))
    assert len(numbers) == 1_000_000
    circle = run_rounds(numbers, total_rounds=10_000_000)
    print(result_to_part2_answer(circle))


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)
    else:
        pytest.main([__file__])


if __name__ == '__main__':
    main()
