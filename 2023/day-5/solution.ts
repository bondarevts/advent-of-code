type Mapping = {
  sourceStart: number
  destinationStart: number
  length: number
}

export function solve1(data: string): void {
  const lines = data.split("\n")
  let currentIds = extractSeeds(lines)
  while (lines.length != 0) {
    const mappings = extractNextMappings(lines)
    currentIds = applyMappings(currentIds, mappings)
  }
  console.log(Math.min(...currentIds))
}

function extractSeeds(lines: string[]): number[] {
  const seedsLine = lines.shift()!
  lines.shift()  // consume an empty line

  const [_, seedsBlock] = seedsLine.split(": ")
  return seedsBlock.split(" ").map(Number)
}

function extractNextMappings(lines: string[]): Mapping[] {
  if (lines.length == 0) {
    return []
  }

  // remove header
  lines.shift()

  const mapping: Mapping[] = []
  let mappingString = lines.shift() ?? ''
  while (mappingString !== '') {
    const [destinationStartString, sourceStartString, lengthString] = mappingString.split(" ")
    mapping.push({
      sourceStart: Number(sourceStartString),
      destinationStart: Number(destinationStartString),
      length: Number(lengthString)
    })
    mappingString = lines.shift() ?? ''
  }
  return mapping
}

function applyMappings(ids: number[], mappings: Mapping[]): number[] {
  return ids.map(id => {
    const mapping = findApplicableMapping(id, mappings)
    if (mapping === undefined) {
      return id
    }
    return applyMapping(id, mapping)
  })
}

function findApplicableMapping(id: number, mappings: Mapping[]): Mapping | undefined {
  for (const mapping of mappings) {
    if (mapping.sourceStart <= id && id < mapping.sourceStart + mapping.length) {
      return mapping
    }
  }
  return undefined
}

function applyMapping(id: number, mapping: Mapping): number {
  return mapping.destinationStart + (id - mapping.sourceStart)
}
