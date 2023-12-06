import { prod } from '../utils'

type Score = {
  time: number
  distance: number
}

export function solve1(data: string): void {
  const [timeString, distanceString] = data.split('\n')
  const [_timeHeader, ...times] = timeString.split(/ +/).map(Number)
  const [_distanceHeader, ...distances] = distanceString.split(/ +/).map(Number)

  const result = prod(
    times
      .map((time, index) => ({ time, distance: distances[index] }))
      .map(solveForScore),
  )
  console.log(result)
}

export function solve2(data: string): void {
  const [timeString, distanceString] = data.split('\n')
  const [_timeHeader, ...times] = timeString.split(/ +/)
  const [_distanceHeader, ...distances] = distanceString.split(/ +/)

  const score: Score = {
    time: Number(times.join('')),
    distance: Number(distances.join('')),
  }
  console.log(solveForScore(score))
}

function solveForScore(score: Score): number {
  let lowerWinningTime: number | undefined = undefined
  let upperWinningTime: number | undefined = undefined

  for (let time = 1; time < score.time; time++) {
    const distance = time * (score.time - time)
    if (lowerWinningTime === undefined) {
      if (distance > score.distance) {
        lowerWinningTime = time
      }
    } else if (upperWinningTime === undefined) {
      if (distance <= score.distance) {
        upperWinningTime = time - 1
      }
    }
  }
  return upperWinningTime! - lowerWinningTime! + 1
}
