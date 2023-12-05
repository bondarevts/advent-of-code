import { sum } from '../utils'

type CardInfo = {
  winningNumbers: string[]
  myNumbers: string[]
}

export function solve1(data: string): void {
  const result = sum(
    data.split('\n').map(parseCardInfo).map(calculateCardScore),
  )
  console.log(result)
}

export function solve2(data: string): void {
  const matchesPerCard = data.split('\n').map(parseCardInfo).map(matchesCount)
  const cardCounts = Array(matchesPerCard.length).fill(1)
  matchesPerCard.forEach((matches, index) => {
    const currentCardsCount = cardCounts[index]
    for (let i = index + 1; i < index + 1 + matches; i++) {
      cardCounts[i] += currentCardsCount
    }
  })
  console.log(sum(cardCounts))
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
