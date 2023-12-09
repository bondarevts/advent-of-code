type Turn = 'L' | 'R'

type Directions = {
  turns: Turn[]
  links: Map<string, Record<Turn, string>>
}

export function solve1(data: string): void {
  const directions = parseDirections(data)
  console.log(stepsToTheEnd(directions))
}

export function solve2(data: string): void {
  const directions = parseDirections(data)
  console.log(calcTotalGhostSteps(directions))
}

function parseDirections(data: string): Directions {
  const [turns, _, ...rawLinks] = data.split('\n')
  return {
    turns: turns as unknown as Turn[],
    links: new Map(rawLinks.map(line => {
      const [node, left, right] = [...line.matchAll(/\w+/g)].map(String)
      return [node, {'L': left, 'R': right}]
    }))
  }
}

function stepsToTheEnd(directions: Directions): number {
  let currentNode = 'AAA'
  let steps = 0
  let currentTurnIndex = 0
  while (currentNode != 'ZZZ') {
    const turn = directions.turns[currentTurnIndex]
    currentNode = directions.links.get(currentNode)![turn]
    currentTurnIndex = (currentTurnIndex + 1) % directions.turns.length
    steps += 1
  }
  return steps
}

function calcTotalGhostSteps(directions: Directions): number {
  return Array.from(directions.links.keys()).filter(node => node.endsWith('A')).map(node => getLoopLength(node, directions)).reduce((acc, loop) => lcm(acc, loop), 1)
}

function getLoopLength(node: string, directions: Directions) {
  let currentNode = node
  let steps = 0
  let currentTurnIndex = 0
  while (!currentNode.endsWith('Z')) {
    const turn = directions.turns[currentTurnIndex]
    currentNode = directions.links.get(currentNode)![turn]
    currentTurnIndex = (currentTurnIndex + 1) % directions.turns.length
    steps += 1
  }
  return steps
}

function gcd(a: number, b: number): number {
  while (b != 0) {
      let t = b;
      b = a % b;
      a = t;
  }
  return a;
}

function lcm(a: number, b: number): number {
  return (a * b) / gcd(a, b);
}
