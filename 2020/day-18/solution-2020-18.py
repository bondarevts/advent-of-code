# https://adventofcode.com/2020/day/18
import ast
import operator
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'


def read_exercises(path: Path):
    return path.read_text().splitlines()


# (7 * (6 * 5 + 2 * 6 * 2)) + 9 + 6 + ((8 + 4) * 5 * 3 + 5 * 8) * ((5 * 5) + (8 + 4 * 5) * 8 + 4 + 2)

valid_symbols = set('()+*')
number_pattern = re.compile(r'\d+')
operations = {
    '+': operator.add,
    '*': operator.mul,
}


def read_number_string_at(expression, pos):
    return number_pattern.match(expression, pos).group()


def tokenize(expression):
    position = 0
    while position < len(expression):
        value = expression[position]
        if value == ' ':
            position += 1
            continue
        if value in valid_symbols:
            yield value
            position += 1
            continue
        number = read_number_string_at(expression, position)
        yield int(number)
        position += len(number)


def apply_value_to(stack, value):
    if stack and stack[-1] in operations:
        operation = stack.pop()
        current_result = stack.pop()
        stack.append(operations[operation](current_result, value))
    else:
        stack.append(value)


def evaluate(expression):
    stack = []
    for token in tokenize(expression):
        if isinstance(token, int):
            apply_value_to(stack, token)
        elif token == ')':
            value = stack.pop()
            assert stack.pop() == '('
            apply_value_to(stack, value)
        else:
            assert token in '(+*'
            stack.append(token)
    assert len(stack) == 1
    return stack.pop()


def part1(dataset: Path):
    print(sum(evaluate(expression) for expression in read_exercises(dataset)))


def put_plus_back(node):
    if isinstance(node, ast.BinOp):
        node.op = ast.Add() if isinstance(node.op, ast.Pow) else node.op
        node.left = put_plus_back(node.left)
        node.right = put_plus_back(node.right)

    return node


def evaluate_plus_first(expression):
    tree = ast.parse(expression.replace('+', '**'), mode='eval')
    tree.body = put_plus_back(tree.body)
    return eval(compile(tree, '', 'eval'))


def part2(dataset: Path):
    print(sum(evaluate_plus_first(expression) for expression in read_exercises(dataset)))


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)
    else:
        pytest.main([__file__])


@pytest.mark.parametrize('expected, expression', [
    (71, '1 + 2 * 3 + 4 * 5 + 6'),
    (51, '1 + (2 * 3) + (4 * (5 + 6))'),
    (26, '2 * 3 + (4 * 5)'),
    (437, '5 + (8 * 3 + 9 + 3 * 4 * 3)'),
    (12240, '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'),
    (13632, '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')
])
def test_evaluate(expected, expression):
    assert expected == evaluate(expression)


@pytest.mark.parametrize('expected, expression', [
    (231, '1 + 2 * 3 + 4 * 5 + 6'),
    (51, '1 + (2 * 3) + (4 * (5 + 6))'),
    (46, '2 * 3 + (4 * 5)'),
    (1445, '5 + (8 * 3 + 9 + 3 * 4 * 3)'),
    (669060, '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'),
    (23340, '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')
])
def test_evaluate_plus_first(expected, expression):
    assert expected == evaluate_plus_first(expression)


if __name__ == '__main__':
    main()
