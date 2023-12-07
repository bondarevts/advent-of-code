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

type Hand = {
  value: Label[]
  strength: number
}

type Game = {
  hand: Hand
  bid: number
}

export function solve1(data: string): void {
  const games = data
    .split('\n')
    .map(parseGame)
    .sort((game1, game2) => handComparator(game1.hand, game2.hand))
  const result = sum(games.map((game, index) => game.bid * (index + 1)))
  console.log(result)
}

function handComparator(hand1: Hand, hand2: Hand): number {
  if (hand1.strength !== hand2.strength) {
    return hand1.strength - hand2.strength
  }
  for (let i = 0; i < 5; i++) {
    const label1 = hand1.value[i]
    const label2 = hand2.value[i]
    if (label1 !== label2) {
      return power.get(label1)! - power.get(label2)!
    }
  }
  return 0
}

function parseGame(line: string): Game {
  const handAndBid = line.split(' ')
  const handLabels = handAndBid[0] as unknown as Label[]
  return {
    hand: {
      value: handLabels,
      strength: calculateHandStrength(handLabels),
    },
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
