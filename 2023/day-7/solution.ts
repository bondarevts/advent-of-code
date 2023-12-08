import { sum } from '../utils'

type Label =
  | 'A'
  | 'K'
  | 'Q'
  | 'J'
  | 'T'
  | '9'
  | '8'
  | '7'
  | '6'
  | '5'
  | '4'
  | '3'
  | '2'
  | '1' // as a Joker for the second part of the task

type HandType =
  | 'Five of a kind'
  | 'Four of a kind'
  | 'Full house'
  | 'Three of a kind'
  | 'Two pair'
  | 'One pair'
  | 'High card'

const typeToStrength: Map<HandType, number> = new Map([
  ['Five of a kind', 6],
  ['Four of a kind', 5],
  ['Full house', 4],
  ['Three of a kind', 3],
  ['Two pair', 2],
  ['One pair', 1],
  ['High card', 0],
])

const power: Map<Label, number> = new Map([
  ['A', 14],
  ['K', 13],
  ['Q', 12],
  ['J', 11],
  ['T', 10],
  ['9', 9],
  ['8', 8],
  ['7', 7],
  ['6', 6],
  ['5', 5],
  ['4', 4],
  ['3', 3],
  ['2', 2],
])

const power2: Map<Label, number> = new Map([
  ['A', 14],
  ['K', 13],
  ['Q', 12],
  ['T', 10],
  ['9', 9],
  ['8', 8],
  ['7', 7],
  ['6', 6],
  ['5', 5],
  ['4', 4],
  ['3', 3],
  ['2', 2],
  ['J', 1],
])

type Hand = Label[]

type Game = {
  hand: Hand
  bid: number
}

export function solve1(data: string): void {
  const games = data
    .split('\n')
    .map((line) => parseGame(line))
    .sort((game1, game2) =>
      handComparator(game1.hand, game2.hand, calculateHandStrength, power),
    )
  const result = sum(games.map((game, index) => game.bid * (index + 1)))
  console.log(result)
}

export function solve2(data: string): void {
  const games = data
    .split('\n')
    .map((line) => parseGame(line))
    .sort((game1, game2) =>
      handComparator(game1.hand, game2.hand, calculateHandStrength2, power2),
    )
  const result = sum(games.map((game, index) => game.bid * (index + 1)))
  console.log(result)
}

function handComparator(
  hand1: Hand,
  hand2: Hand,
  strengthCalculator: (hand: Hand) => number,
  labelPower: Map<Label, number>,
): number {
  const strength1 = strengthCalculator(hand1)
  const strength2 = strengthCalculator(hand2)
  if (strength1 !== strength2) {
    return strength1 - strength2
  }
  for (let i = 0; i < 5; i++) {
    const label1 = hand1[i]
    const label2 = hand2[i]
    if (label1 !== label2) {
      return labelPower.get(label1)! - labelPower.get(label2)!
    }
  }
  return 0
}

function parseGame(line: string): Game {
  const handAndBid = line.split(' ')
  return {
    hand: Array.from(handAndBid[0]) as unknown as Hand,
    bid: Number(handAndBid[1]),
  }
}

function calculateHandStrength(labels: Label[]): number {
  return typeToStrength.get(getHandType(labels))!
}

function getHandType(labels: Label[]): HandType {
  const counts = countCards(labels)
  if (counts.size === 1) {
    return 'Five of a kind'
  }
  const maxLabelCount = Math.max(...counts.values())
  if (maxLabelCount === 4) {
    return 'Four of a kind'
  }
  if (maxLabelCount === 3 && counts.size === 2) {
    return 'Full house'
  }
  if (maxLabelCount === 3) {
    return 'Three of a kind'
  }
  if (maxLabelCount === 2 && counts.size === 3) {
    return 'Two pair'
  }
  if (maxLabelCount === 2) {
    return 'One pair'
  }
  return 'High card'
}

function countCards(labels: Label[]): Map<Label, number> {
  const counts = new Map<Label, number>()
  for (const label of labels) {
    counts.set(label, (counts.get(label) ?? 0) + 1)
  }
  return counts
}

function calculateHandStrength2(labels: Label[]): number {
  return typeToStrength.get(getHandType2(labels))!
}

function getHandType2(hand: Hand): HandType {
  return getHandType(transformToMostValuableHand(hand))
}

function transformToMostValuableHand(hand: Hand): Hand {
  const counts = countCards(hand)

  counts.delete('J')
  counts.set('1', -1) // to serve as the current maximum for counts
  const maxNonJokerLabel = Array.from(counts).reduce(
    (currentMax, [key, value]) =>
      value > counts.get(currentMax)! ? key : currentMax,
    '1' as Label,
  )

  return hand.map((value) => (value !== 'J' ? value : maxNonJokerLabel))
}
