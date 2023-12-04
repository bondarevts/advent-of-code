import { sum } from '../utils'

type CardInfo = {
  winningNumbers: string[]
  myNumbers: string[]
}

export function solve1(data: string) {
  const result = sum(
    data.split('\n').map(parseCardInfo).map(calculateCardScore),
  )
  console.log(result)
}

function parseCardInfo(line: string): CardInfo {
  const [_, allNumbers] = line.split(': ')
  const [winningNumbersString, numbersString] = allNumbers.split(' | ')
  return {
    winningNumbers: winningNumbersString.match(/\d+/g) ?? [],
    myNumbers: numbersString.match(/\d+/g) ?? [],
  }
}

function calculateCardScore(card: CardInfo): number {
  const matchesInCard = matchesCount(card)
  return matchesInCard == 0 ? 0 : 2 ** (matchesInCard - 1)
}

function matchesCount(card: CardInfo): number {
  const myNumbersSet = new Set(card.myNumbers)
  return card.winningNumbers.filter((value) => myNumbersSet.has(value)).length
}
