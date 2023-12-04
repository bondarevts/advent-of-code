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
  const result = findAllPartNumbers(lines)
    .reduce((acc, partNumber) => acc + Number(partNumber.value), 0)
  console.log(result)
}

export function solve2(data: string): void {
  const lines = data.trimEnd().split("\n")
  const potentialGears = findPotentialGears(lines)

  const partNumbers = findAllPartNumbers(lines)
  const result = 
    potentialGears
    .map(position => getBorderNumberPositions(position, lines))
    .map(gearNumberPositions => {
      const gearPartNumbers = gearNumberPositions.map(position => getPartByPosition(position, partNumbers))
      return [...new Set(gearPartNumbers)]
    })
    .filter(partNumbers => partNumbers.length == 2)
    .map(([part1, part2]) => Number(part1.value) * Number(part2.value))
    .reduce((acc, value) => acc + value, 0)
  console.log(result)
}

function findAllPartNumbers(lines: string[]): PartNumber[] {
  const potentialPartNumbers = findPotentialPartNumbers(lines)
  return potentialPartNumbers.filter((p) => isLegalPartNumber(p, lines))
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

function findPotentialGears(lines: string[]): Position[] {
  return lines.flatMap((line, index) => parseGearsFromLine(line, index))
}

function parseGearsFromLine(line: string, index: number): Position[] {
  const positions: Position[] = []
  for (const match of line.matchAll(/\*/g)) {
    positions.push({y: index, x: match.index!})
  }
  return positions
}

function getBorderNumberPositions(position: Position, lines: string[]): Position[] {
  const numbers: number[] = []
  return getValidBorderPositions(position, 1, lines)
  .map(position => {
    return {
    position: position,
    value: lines[position.y][position.x]
  }})
  .filter(({value}) => /\d/.test(value))
  .map(({position}) => position)
}

function getPartByPosition(position: Position, partNumbers: PartNumber[]): PartNumber {
  for (const partNumber of partNumbers) {
    if (position.y == partNumber.position.y && position.x >= partNumber.position.x && position.x < partNumber.position.x + partNumber.value.length) {
      return partNumber
    }
  }
  throw new Error(`Can't find a part number for ${position}`)
}
