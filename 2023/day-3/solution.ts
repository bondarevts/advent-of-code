type PartNumber = {
  value: string
  lineNumber: number
  position: number
}

export function solve1(data: string):void {
  const lines = data.trimEnd().split("\n")
  const potentialPartNumbers = findPotentialPartNumbers(lines)
  const result = 
    potentialPartNumbers
    .filter(p => isLegalPartNumber(p, lines))
    .reduce((acc, partNumber) => acc + Number(partNumber.value), 0)
  console.log(result)
}

function findPotentialPartNumbers(lines: string[]): PartNumber[] {
  return lines.flatMap((line, index) => parseLine(line, index))
}

function parseLine(line: string, index: number): PartNumber[] {
  const partNumbers = []
  for (const match of line.matchAll(/\d+/g)) {
    partNumbers.push({
      value: match[0],
      lineNumber: index,
      position: match.index!
    })
  }
  return partNumbers
}

function isLegalPartNumber(partNumber: PartNumber, lines: string[]): boolean {
  let positionsToCheck: [number, number][] = [
    [partNumber.lineNumber, partNumber.position - 1],
    [partNumber.lineNumber, partNumber.position + partNumber.value.length]
  ]

  for (let start = partNumber.position - 1; start <= partNumber.position + partNumber.value.length; start++) {
    positionsToCheck.push([partNumber.lineNumber - 1, start])
    positionsToCheck.push([partNumber.lineNumber + 1, start])
  }

  console.log(partNumber)
  console.log(positionsToCheck)
  positionsToCheck = positionsToCheck.filter(([line, position]) => 
    line >= 0 && line < lines.length && position >= 0 && position < lines[0].length
  )
  console.log(positionsToCheck)

  return positionsToCheck.some(([line, position]) => lines[line][position] != '.')
}