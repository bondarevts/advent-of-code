import { sum } from "../utils"

export function solve1(data: string) {
  console.log(sum(parseDataset(data).map(predictNextInSequence)))
}

export function solve2(data: string) {
  const sequences = parseDataset(data)
  console.log(sum(sequences.map(predictPreviousInSequence)))
}

function parseDataset(data: string): number[][] {
  return data.split('\n').map(line => line.split(" ").map(Number))
}

function predictNextInSequence(sequence: number[]): number {
  const triangle = buildTriangle(sequence)
  return sum(triangle.map(row => row[row.length - 1]))
}

function predictPreviousInSequence(sequence: number[]): number {
  const triangle = buildTriangle(sequence)
  return triangle.reverse().reduce((acc, sequence) => sequence[0] - acc, 0)
}

function buildTriangle(sequence: number[]): number[][] {
  const triangle = [sequence]
  let lastSequence = sequence
  while (!lastSequence.every(value => value === 0)) {
    const newSequence: number[] = []
    for (let i = 0; i < lastSequence.length - 1; i++) {
      newSequence.push(lastSequence[i + 1] - lastSequence[i])
    }
    triangle.push(newSequence)
    lastSequence = newSequence
  }
  return triangle
}

