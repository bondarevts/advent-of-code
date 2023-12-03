type PartNumber = {
  value: string
  position: Position
}

type Position = {
  y: number
  x: number
}

export function solve1(data: string): void {
  const lines = data.trimEnd().split('\n')
  const potentialPartNumbers = findPotentialPartNumbers(lines)
  const result = potentialPartNumbers
    .filter((p) => isLegalPartNumber(p, lines))
    .reduce((acc, partNumber) => acc + Number(partNumber.value), 0)
  console.log(result)
}

function findPotentialPartNumbers(lines: string[]): PartNumber[] {
  return lines.flatMap((line, index) => parsePartNumbersFromLine(line, index))
}

function parsePartNumbersFromLine(line: string, index: number): PartNumber[] {
  const partNumbers: PartNumber[] = []
  for (const match of line.matchAll(/\d+/g)) {
    partNumbers.push({
      value: match[0],
      position: {
        y: index,
        x: match.index!,
      },
    })
  }
  return partNumbers
}

function getValidBorderPositions(
  position: Position,
  length: number,
  lines: string[],
): Position[] {
  const borderPositions: Position[] = [
    { y: position.y, x: position.x - 1 },
    { y: position.y, x: position.x + length },
  ]

  for (let start = position.x - 1; start <= position.x + length; start++) {
    borderPositions.push({ y: position.y - 1, x: start })
    borderPositions.push({ y: position.y + 1, x: start })
  }

  return borderPositions.filter(
    (position) =>
      position.y >= 0 &&
      position.y < lines.length &&
      position.x >= 0 &&
      position.x < lines[0].length,
  )
}

function isLegalPartNumber(partNumber: PartNumber, lines: string[]): boolean {
  return getValidBorderPositions(
    partNumber.position,
    partNumber.value.length,
    lines,
  ).some((position) => lines[position.y][position.x] != '.')
}
