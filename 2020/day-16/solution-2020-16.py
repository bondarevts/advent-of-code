# https://adventofcode.com/2020/day/16
import heapq
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'


@dataclass
class Field:
    name: str
    range1: range
    range2: range

    def __contains__(self, item):
        return item in self.range1 or item in self.range2


def read_dataset(path: Path):
    field_pattern = re.compile(r'(.*): (\d+)-(\d+) or (\d+)-(\d+)')
    fields = []
    with open(path) as data_lines:
        for line in data_lines:
            if not line.strip():
                break
            name, start1, end1, start2, end2 = field_pattern.match(line).groups()
            fields.append(Field(name, range(int(start1), int(end1) + 1), range(int(start2), int(end2) + 1)))

        assert next(data_lines) == 'your ticket:\n'
        my_ticket = [int(v) for v in next(data_lines).split(',')]

        assert not next(data_lines).strip()
        assert next(data_lines) == 'nearby tickets:\n'
        tickets = [
            [int(v) for v in line.split(',')]
            for line in data_lines
        ]
    return fields, my_ticket, tickets


def valid_numbers(fields):
    valid = set()
    for field in fields:
        valid.update(field.range1)
        valid.update(field.range2)
    return valid


def part1(dataset: Path):
    fields, _, tickets = read_dataset(dataset)
    valid = valid_numbers(fields)
    print(sum(
        value
        for ticket in tickets
        for value in ticket
        if value not in valid
    ))


def part2(dataset: Path):
    fields, my_ticket, tickets = read_dataset(dataset)
    valid = valid_numbers(fields)
    valid_tickets = [
        ticket
        for ticket in tickets
        if all(value in valid for value in ticket)
    ]
    valid_tickets.append(my_ticket)

    field_values = list(zip(*valid_tickets))
    possible_fields = []
    for position, values in enumerate(field_values):
        matching_fields = set()
        for field in fields:
            if all(value in field for value in values):
                matching_fields.add(field.name)
        possible_fields.append((len(matching_fields), position, matching_fields))

    heapq.heapify(possible_fields)
    result = 1
    while possible_fields:
        _, position, name_set = heapq.heappop(possible_fields)
        assert len(name_set) == 1
        name = name_set.pop()
        if name.startswith('departure'):
            result *= my_ticket[position]
        for _, _, matching_fields in possible_fields:
            matching_fields.remove(name)
        heapq.heapify(possible_fields)
    print(result)


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)


if __name__ == '__main__':
    main()
