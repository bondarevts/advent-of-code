export function solve1(data: string): void {
  // only 12 red cubes, 13 green cubes, and 14 blue cubes
  const maxCubes = {
    red: 12,
    green: 13,
    blue: 14
  }

  const result = 
    data.trimEnd().split("\n").map((line, index) => {
      const gameNumber = index + 1
      const allDrawsSuccessful = line.split(": ")[1].split("; ").every(drawString => 
        drawString.split(", ").every(cubeColorString => {
          const [cubesString, color] = cubeColorString.split(" ")
          return Number(cubesString) <= maxCubes[color as "red" | "green" | "blue"]
        })
      )
      return allDrawsSuccessful ? gameNumber : 0
    }).reduce((acc, value) => acc + value, 0)
  console.log(result)
}