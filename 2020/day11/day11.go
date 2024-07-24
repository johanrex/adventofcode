package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

type Grid [][]rune

type GridChange struct {
	row    int
	col    int
	newVal rune
}

var dirs = []struct{ dcol, drow int }{
	{-1, 0},  // up
	{1, 0},   // down
	{0, -1},  // left
	{0, 1},   // right
	{-1, -1}, // up-left
	{-1, 1},  // up-right
	{1, -1},  // down-left
	{1, 1},   // down-right
}

func readFile2dSlice(filename string) Grid {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatalf("failed to open file: %s", err)
	}
	defer file.Close()

	var grid [][]rune
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		grid = append(grid, []rune(line))
	}

	if err := scanner.Err(); err != nil {
		log.Fatalf("failed to read lines: %s", err)
	}

	return grid
}

func printGrid(grid Grid) {
	for _, row := range grid {
		fmt.Println(string(row))
	}
}

func getAdjacents(grid Grid, row, col int) []rune {
	adj := []rune{}
	for _, dir := range dirs {
		newCol, newRow := col+dir.dcol, row+dir.drow
		if newRow >= 0 && newRow < len(grid) && newCol >= 0 && newCol < len(grid[row]) {
			adj = append(adj, grid[newRow][newCol])
		}
	}

	return adj
}

func getFirstVisibles(grid Grid, row, col int) []rune {
	adj := []rune{}

	rows := len(grid)
	cols := len(grid[0])

	for _, dir := range dirs {
		newRow := row
		newCol := col

		for {
			newRow = newRow + dir.drow
			newCol = newCol + dir.dcol

			isValidPos := newRow >= 0 && newRow < rows && newCol >= 0 && newCol < cols

			if !isValidPos {
				break
			}

			// if we find a seat, add it to the list and break
			if grid[newRow][newCol] == 'L' || grid[newRow][newCol] == '#' {
				adj = append(adj, grid[newRow][newCol])
				break
			}
		}
	}

	return adj
}

func any(arr []rune, val rune) bool {
	for _, v := range arr {
		if v == val {
			return true
		}
	}
	return false

}

func arrCount(arr []rune, val rune) int {
	count := 0
	for _, v := range arr {
		if v == val {
			count++
		}
	}
	return count
}

func gridCount(grid Grid, val rune) int {
	count := 0
	for y := range grid {
		for x := range grid[y] {
			if grid[y][x] == val {
				count++
			}
		}
	}
	return count
}

func rule1ChangesState(grid Grid, row, col int, seats []rune) bool {
	// If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied (change state)
	if grid[row][col] == 'L' && !any(seats, '#') {
		return true
	}
	return false
}

func rule2ChangesState(grid Grid, row, col int, seats []rune, threshold int) bool {
	// If a seat is occupied (#) and [threshold] or more seats adjacent to it are also occupied, the seat becomes empty.
	if grid[row][col] == '#' && arrCount(seats, '#') >= threshold {
		return true
	}
	return false
}

func evalRound(grid *Grid, part int) bool {
	var changes []GridChange

	type rule1SeatFuncType func(Grid, int, int) []rune
	var rule1SeatFunc rule1SeatFuncType

	var rule2Threshold int
	if part == 1 {
		rule1SeatFunc = getAdjacents
		rule2Threshold = 4
	} else {
		rule1SeatFunc = getFirstVisibles
		rule2Threshold = 5
	}

	//check if we should change anything
	for rowIdx := 0; rowIdx < len(*grid); rowIdx++ {
		row := (*grid)[rowIdx]
		for colIdx := 0; colIdx < len(row); colIdx++ {
			var seats []rune

			seats = rule1SeatFunc(*grid, rowIdx, colIdx)

			if rule1ChangesState(*grid, rowIdx, colIdx, seats) {
				change := GridChange{
					row:    rowIdx,
					col:    colIdx,
					newVal: '#',
				}
				changes = append(changes, change)
			} else {
				if rule2ChangesState(*grid, rowIdx, colIdx, seats, rule2Threshold) {
					change := GridChange{
						row:    rowIdx,
						col:    colIdx,
						newVal: 'L',
					}
					changes = append(changes, change)
				}
			}
		}
	}

	//apply changes
	for _, change := range changes {
		(*grid)[change.row][change.col] = change.newVal

	}

	//return if we changed anything
	return len(changes) > 0
}

func evaluate(grid Grid, part int) {

	for i := 0; true; i++ {
		changed := evalRound(&grid, part)

		if !changed {
			fmt.Println("No change in grid after round", i+1)
			break
		}
	}

	cnt := gridCount(grid, '#')
	fmt.Println("Part", part, ":", cnt)
}
func deepCopyGrid(grid [][]rune) [][]rune {
	gridCopy := make([][]rune, len(grid))

	for i, row := range grid {
		newRow := make([]rune, len(row))
		copy(newRow, row)
		gridCopy[i] = newRow
	}

	return gridCopy
}

func main() {
	// filename := "day11/example"
	filename := "day11/input"

	grid := readFile2dSlice(filename)

	fmt.Println("Grid size is:")
	fmt.Println(len(grid), "rows")
	fmt.Println(len(grid[0]), "columns")

	evaluate(deepCopyGrid(grid), 1)
	evaluate(deepCopyGrid(grid), 2)

	// (L) empty
	// (#) occupied
	// (.) floor

	fmt.Println("Done.")
}
