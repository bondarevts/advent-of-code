# https://adventofcode.com/2020/day/8

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from typing import List

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'


@dataclass
class Statement:
    name: str
    argument: int


@dataclass
class RunResult:
    finished: bool
    accumulator: int


def read_source_code(path: Path) -> Iterable[Statement]:
    with open(path) as source_file:
        for line in source_file:
            name, argument = line.split()
            yield Statement(name, int(argument))


def run_program(statements: List[Statement]) -> RunResult:
    visited = [False] * len(statements)
    current_line = 0
    accumulator = 0
    while not visited[current_line]:
        visited[current_line] = True
        statement = statements[current_line]
        if statement.name == 'jmp':
            current_line += statement.argument
        else:
            current_line += 1
            if statement.name == 'acc':
                accumulator += statement.argument
        if current_line >= len(statements):
            return RunResult(finished=True, accumulator=accumulator)
    return RunResult(finished=False, accumulator=accumulator)


def toggle_statement(statement: Statement):
    assert statement.name != 'acc'
    statement.name = 'jmp' if statement.name == 'nop' else 'nop'


def part1(dataset: Path):
    statements = list(read_source_code(dataset))
    print(run_program(statements).accumulator)


def part2(dataset: Path):
    statements = list(read_source_code(dataset))
    for statement in statements:
        if statement.name == 'acc':
            continue
        toggle_statement(statement)
        result = run_program(statements)
        if result.finished:
            print(result.accumulator)
            return
        toggle_statement(statement)


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)


if __name__ == '__main__':
    main()
