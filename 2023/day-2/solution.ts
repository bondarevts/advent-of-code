type Color = 'red' | 'green' | 'blue'
type Reveal = {
  count: number
  color: Color
}

type Game = {
  reveals: Reveal[]
  number: number
}

const MAX_CUBES = {
  red: 12,
  green: 13,
  blue: 14,
}

export function solve1(data: string): void {
  const games = parseGames(data.trimEnd())
  const result = games
    .filter(isLegalGame)
    .map((game) => game.number)
    .reduce((acc, value) => acc + value)
  console.log(result)
}

export function solve2(data: string): void {
  const games = parseGames(data.trimEnd())
  const result = games.map(solveGame).reduce((acc, value) => acc + value, 0)
  console.log(result)
}

function isLegalGame(game: Game): boolean {
  return game.reveals.every((reveal) => reveal.count <= MAX_CUBES[reveal.color])
}

function parseGames(data: string): Game[] {
  return data.split('\n').map(parseGame)
}

function parseGame(gameString: string): Game {
  const [gameDescription, gameRevealsSet] = gameString.split(': ')

  const gameNumber = Number(gameDescription.split(' ')[1])

  return {
    number: gameNumber,
    reveals: gameRevealsSet.replace(/;/g, ',').split(', ').map(parseReveal),
  }
}

function parseReveal(reveal: string): Reveal {
  const [count, cubeColor] = reveal.split(' ')
  return {
    count: Number(count),
    color: cubeColor as Color,
  }
}

function solveGame(game: Game): number {
  const maxPerColor = game.reveals.reduce(
    (maxCounts, reveal) => {
      maxCounts[reveal.color] = Math.max(maxCounts[reveal.color], reveal.count)
      return maxCounts
    },
    { red: 0, blue: 0, green: 0 },
  )

  return maxPerColor.red * maxPerColor.green * maxPerColor.blue
}
