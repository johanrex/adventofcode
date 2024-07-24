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

func getAllAdjacent(grid Grid, row, col int) []rune {
	adj := []rune{}
	for _, dir := range dirs {
		newCol, newRow := col+dir.dcol, row+dir.drow
		if newRow >= 0 && newRow < len(grid) && newCol >= 0 && newCol < len(grid[row]) {
			adj = append(adj, grid[newRow][newCol])
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

func isEqual(grid1 Grid, grid2 Grid) bool {
	if len(grid1) != len(grid2) {
		log.Fatalf("grids have different number of rows")
	}
	for y := range grid1 {
		if len(grid1[y]) != len(grid2[y]) {
			log.Fatalf("grids have different number of columns")
		}
		for x := range grid1[y] {
			if grid1[y][x] != grid2[y][x] {
				return false // Different elements
			}
		}
	}
	return true
}

func rule1ShouldChangeState(grid Grid, row, col int) bool {
	// If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied (change state)
	if grid[row][col] == 'L' && !any(getAllAdjacent(grid, row, col), '#') {
		return true
	}
	return false
}

func rule2ShouldChangeState(grid Grid, row, col int) bool {
	// If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
	if grid[row][col] == '#' && arrCount(getAllAdjacent(grid, row, col), '#') >= 4 {
		return true
	}
	return false
}

func copyGrid(grid Grid) Grid {
	newGrid := make(Grid, len(grid))
	for rowIdx, row := range grid {
		newGrid[rowIdx] = make([]rune, len(row))
		for colIdx, cellVal := range row {
			newGrid[rowIdx][colIdx] = cellVal
		}
	}

	return newGrid
}

func evalRound(grid *Grid) bool {
	var changes []GridChange

	//check if we should change anything
	for rowIdx := 0; rowIdx < len(*grid); rowIdx++ {
		row := (*grid)[rowIdx]
		for colIdx := 0; colIdx < len(row); colIdx++ {
			if rule1ShouldChangeState(*grid, rowIdx, colIdx) {
				change := GridChange{
					row:    rowIdx,
					col:    colIdx,
					newVal: '#',
				}
				changes = append(changes, change)
			} else if rule2ShouldChangeState(*grid, rowIdx, colIdx) {
				change := GridChange{
					row:    rowIdx,
					col:    colIdx,
					newVal: 'L',
				}
				changes = append(changes, change)
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

func main() {
	filename := "day11/example"
	// filename := "day11/input"
	grid := readFile2dSlice(filename)

	fmt.Println("Grid size is:")
	fmt.Println(len(grid), "rows")
	fmt.Println(len(grid[0]), "columns")

	fmt.Println("Starting grid:")
	printGrid(grid)

	for i := 0; true; i++ {
		changed := evalRound(&grid)

		fmt.Println("")
		fmt.Println("Round", i+1)
		printGrid(grid)

		if !changed {
			fmt.Println("No change in grid after round", i+1)
			break
		}
	}

	cnt := gridCount(grid, '#')
	fmt.Println("Part 1:", cnt)

	// (L) empty
	// (#) occupied
	// (.) floor

	fmt.Println("Done.")
}
