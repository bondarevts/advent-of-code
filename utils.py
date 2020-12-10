from pathlib import Path
from typing import Iterable


def read_numbers(path: Path) -> Iterable[int]:
    with open(path) as input_file:
        for line in input_file:
            yield int(line)
