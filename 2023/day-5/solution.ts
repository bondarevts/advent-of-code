type Mapping = {
  sourceStart: number
  destinationStart: number
  length: number
}

type Range = {
  start: number
  end: number
}

type Transformation = {
  range: Range
  diff: number
}

export function solve1(data: string): void {
  const lines = data.split('\n')
  let currentIds = extractSeeds(lines)
  while (lines.length != 0) {
    const mappings = extractNextMappings(lines)
    currentIds = applyMappings(currentIds, mappings)
  }
  console.log(Math.min(...currentIds))
}

export function solve2(data: string): void {
  const lines = data.split('\n')
  let ranges = extractSeedRanges(lines)
  while (lines.length != 0) {
    const transformations = extractNextTransformations(lines)
    ranges = transformRanges(ranges, transformations)
  }
  console.log(Math.min(...ranges.map((r) => r.start)))
}

function extractSeeds(lines: string[]): number[] {
  const seedsLine = lines.shift()!
  lines.shift() // consume an empty line

  const [_, seedsBlock] = seedsLine.split(': ')
  return seedsBlock.split(' ').map(Number)
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
    const [destinationStartString, sourceStartString, lengthString] =
      mappingString.split(' ')
    mapping.push({
      sourceStart: Number(sourceStartString),
      destinationStart: Number(destinationStartString),
      length: Number(lengthString),
    })
    mappingString = lines.shift() ?? ''
  }
  return mapping
}

function applyMappings(ids: number[], mappings: Mapping[]): number[] {
  return ids.map((id) => {
    const mapping = findApplicableMapping(id, mappings)
    if (mapping === undefined) {
      return id
    }
    return applyMapping(id, mapping)
  })
}

function findApplicableMapping(
  id: number,
  mappings: Mapping[],
): Mapping | undefined {
  for (const mapping of mappings) {
    if (
      mapping.sourceStart <= id &&
      id < mapping.sourceStart + mapping.length
    ) {
      return mapping
    }
  }
  return undefined
}

function applyMapping(id: number, mapping: Mapping): number {
  return mapping.destinationStart + (id - mapping.sourceStart)
}

function extractSeedRanges(lines: string[]): Range[] {
  const seedsLine = lines.shift()!
  lines.shift() // consume an empty line

  const [_, seedsBlock] = seedsLine.split(': ')
  const rawRanges = seedsBlock.split(' ').map(Number)
  const ranges: Range[] = []
  while (rawRanges.length != 0) {
    const start = rawRanges.shift()!
    const length = rawRanges.shift()!
    ranges.push({
      start: start,
      end: start + length - 1,
    })
  }
  return ranges
}

function extractNextTransformations(lines: string[]): Transformation[] {
  if (lines.length == 0) {
    return []
  }

  // remove header
  lines.shift()

  const transformations: Transformation[] = []
  let transformationString = lines.shift() ?? ''
  while (transformationString !== '') {
    const [destinationStart, sourceStart, length] = transformationString
      .split(' ')
      .map(Number)
    transformations.push({
      range: {
        start: sourceStart,
        end: sourceStart + length - 1,
      },
      diff: destinationStart - sourceStart,
    })
    transformationString = lines.shift() ?? ''
  }
  transformations.sort((t1, t2) => t1.range.start - t2.range.start)

  const finalTransformations: Transformation[] = []
  let lowerBoundary = -Infinity
  for (const transformation of transformations) {
    if (lowerBoundary + 1 < transformation.range.start) {
      finalTransformations.push({
        range: {
          start: lowerBoundary,
          end: transformation.range.start - 1,
        },
        diff: 0,
      })
    }
    finalTransformations.push(transformation)
    lowerBoundary = transformation.range.end + 1
  }
  finalTransformations.push({
    range: {
      start: lowerBoundary,
      end: Infinity,
    },
    diff: 0,
  })
  return finalTransformations
}

function transformRanges(
  ranges: Range[],
  transformations: Transformation[],
): Range[] {
  return ranges.flatMap((r) => transformRange(r, transformations))
}

function transformRange(
  range: Range,
  transformations: Transformation[],
): Range[] {
  let id = range.start
  const ranges: Range[] = []
  for (const transformation of transformations) {
    if (transformation.range.end < id) {
      continue
    }
    if (id > range.end) {
      break
    }
    ranges.push({
      start: id + transformation.diff,
      end: Math.min(transformation.range.end, range.end) + transformation.diff,
    })
    id = Math.min(transformation.range.end, range.end) + 1
  }
  return ranges
}

function findApplicableTransformation(
  id: number,
  transformations: Transformation[],
): Transformation | undefined {
  let finalTransformation: Transformation | undefined = undefined
  for (const transformation of transformations) {
    if (id < transformation.range.start) {
      break
    }
    finalTransformation = transformation
  }
  return finalTransformation
}
