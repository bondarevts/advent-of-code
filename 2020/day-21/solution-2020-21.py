# https://adventofcode.com/{{ year }}/day/{{ day }}

import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import List
from typing import Set

import pytest

ROOT = Path(__file__).parent
DATASET_PATH = ROOT / 'dataset.txt'


@dataclass
class Food:
    ingredients: Set[str]
    allergens: Set[str]


def read_dataset(path: Path):
    for line in path.read_text().splitlines():
        ingredients, allergens = line.split(' (contains ')
        yield Food(set(ingredients.split()), set(allergens.rstrip(')').split(', ')))


def solve_allergens(possible_allergens):
    solved_allergens = {}
    while possible_allergens:
        for allergen, ingredients in possible_allergens.items():
            if len(ingredients) == 1:
                break
        else:
            assert False
        ingredient = ingredients.pop()
        solved_allergens[allergen] = ingredient
        possible_allergens.pop(allergen)

        for ingredients in possible_allergens.values():
            ingredients.discard(ingredient)
    return solved_allergens


def localize_allergens(foods):
    possible_allergens = {}
    for food in foods:
        for allergen in food.allergens:
            if allergen in possible_allergens:
                possible_allergens[allergen].intersection_update(food.ingredients)
            else:
                possible_allergens[allergen] = set(food.ingredients)
    return solve_allergens(possible_allergens)


def part1(dataset: Path):
    foods = list(read_dataset(dataset))
    all_allergens = set(localize_allergens(foods).values())
    print(sum(
        ingredient not in all_allergens
        for food in foods
        for ingredient in food.ingredients
    ))


def part2(dataset: Path):
    foods = read_dataset(dataset)
    allergen_to_ingredient = sorted(localize_allergens(foods).items())
    print(','.join(ingredient for _, ingredient in allergen_to_ingredient))


def main():
    if sys.argv[1] == '1':
        part1(DATASET_PATH)
    elif sys.argv[1] == '2':
        part2(DATASET_PATH)
    else:
        pytest.main([__file__])


if __name__ == '__main__':
    main()
