# https://adventofcode.com/2020/day/7
import re
import sys
from pathlib import Path
from typing import Dict
from typing import Tuple

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'

INNER_BAG_PATTERN = re.compile(r'(\d+) (\w+ \w+) bag')


def parse_rule(line: str) -> Tuple[str, Dict[str, int]]:
    name, should_contain = line.split(' bags contain ')
    if should_contain == 'no other bags.\n':
        return name, {}

    bag_content = {}
    for inner_bag in should_contain.split(', '):
        count, inner_name = INNER_BAG_PATTERN.match(inner_bag).groups()
        bag_content[inner_name] = int(count)
    return name, bag_content


def read_rules(path: Path) -> Dict[str, Dict[str, int]]:
    with open(path) as dataset:
        return dict(parse_rule(line) for line in dataset)


def outer_bags(dataset: Path):
    parents = {}
    for bag_color, contains in read_rules(dataset).items():
        for inner_color, _ in contains.items():
            parents.setdefault(inner_color, []).append(bag_color)
    return parents


def count_ancestors(dataset: Path, start: str) -> int:
    parents = outer_bags(dataset)
    stack = [start]
    visited = set()
    while stack:
        child = stack.pop()
        if child in visited:
            continue
        visited.add(child)
        stack.extend(parents.get(child, []))
    return len(visited) - 1


def count_children(dataset: Path, start: str) -> int:
    rules = read_rules(dataset)
    total_inside = 0
    to_visit = [(start, 1)]
    while to_visit:
        node, multiplier = to_visit.pop()
        for child, n in rules[node].items():
            node_multiplier = multiplier * n
            total_inside += node_multiplier
            to_visit.append((child, node_multiplier))
    return total_inside


def part1(dataset: Path):
    print(count_ancestors(dataset, 'shiny gold'))


def part2(dataset: Path):
    print(count_children(dataset, 'shiny gold'))


def main():
    parameter = sys.argv[1]
    if parameter == '1':
        part1(DATASET_PATH)
    elif parameter == '2':
        part2(DATASET_PATH)


if __name__ == '__main__':
    main()
