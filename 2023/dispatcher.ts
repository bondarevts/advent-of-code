import * as fs from 'fs'

async function runSolution() {
  const day = process.argv[3]
  const level = (process.argv[4] ?? '1') as '1' | '2'
  const dayFolder = `day-${day}`

  console.log(`Running solution for day ${day}, level ${level}`)

  const solution = await import(`./${dayFolder}/solution.ts`)

  const datasetFolder = `${process.cwd()}/${dayFolder}`
  let dataset: string
  switch (process.argv[2]) {
    case 'solve':
      dataset = `${datasetFolder}/dataset.txt`
      break

    case 'test':
      if (process.argv[5]) {
        dataset = `${datasetFolder}/${process.argv[5]}.txt`
      } else {
        dataset = `${datasetFolder}/test${level}.txt`
      }
      break

    default:
      throw new Error('Wrong mode')
  }

  console.log(`Running on the dataset: ${dataset}`)
  const data = fs.readFileSync(dataset, 'utf8')
  solution[`solve${level}`](data.trimEnd())
}

runSolution()
