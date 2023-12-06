export function sum(array: number[]): number {
  return array.reduce((acc, value) => acc + value, 0)
}

export function prod(array: number[]): number {
  return array.reduce((acc, value) => acc * value, 1)
}
