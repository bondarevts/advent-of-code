export function solve1(data: string): void {
  const result = data
    .split('\n')
    .map((line) => firstDigit(line) * 10 + firstDigit(line.split('').reverse()))
    .reduce((value, acc) => value + acc, 0)
  console.log(result)
}

function firstDigit(s: string | string[]): number {
  for (const char of s) {
    if (isDigit(char)) {
      return Number(char)
    }
  }
  return 0
}

function isDigit(char: string): boolean {
  return char >= '0' && char <= '9'
}

export function solve2(data: string): void {
  const result = data
    .split('\n')
    .map((line) => advancedFirstDigit(line) * 10 + advancedLastDigit(line))
    .reduce((value, acc) => value + acc, 0)
  console.log(result)
}

function advancedFirstDigit(s: string): number {
  const regex = /(one|two|three|four|five|six|seven|eight|nine|zero|[0-9])/
  return advancedFindDigit(regex, s)
}

function advancedLastDigit(s: string): number {
  const regex = /.*(one|two|three|four|five|six|seven|eight|nine|zero|[0-9])/
  return advancedFindDigit(regex, s)
}

function advancedFindDigit(regex: RegExp, s: string): number {
  const match = s.match(regex)
  const digit = match ? match[1] : '0'
  switch (digit) {
    case 'zero':
      return 0
    case 'one':
      return 1
    case 'two':
      return 2
    case 'three':
      return 3
    case 'four':
      return 4
    case 'five':
      return 5
    case 'six':
      return 6
    case 'seven':
      return 7
    case 'eight':
      return 8
    case 'nine':
      return 9
    default:
      return Number(digit)
  }
}
