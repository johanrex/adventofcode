package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

type Grid [][]rune

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

func getAllAdjacent(grid Grid, x, y int) []rune {

	adj := []rune{}
	if y > 0 { //up
		adj = append(adj, grid[y-1][x])
	}
	if y < len(grid)-1 { //down
		adj = append(adj, grid[y+1][x])
	}
	if x > 0 { //left
		adj = append(adj, grid[y][x-1])
	}
	if x < len(grid[y])-1 { //right
		adj = append(adj, grid[y][x+1])
	}
	if y > 0 && x > 0 { //up left
		adj = append(adj, grid[y-1][x-1])
	}
	if y > 0 && x < len(grid[y])-1 { //up right
		adj = append(adj, grid[y-1][x+1])
	}
	if y < len(grid)-1 && x > 0 { //down left
		adj = append(adj, grid[y+1][x-1])
	}
	if y < len(grid)-1 && x < len(grid[y])-1 { //down right
		adj = append(adj, grid[y+1][x+1])
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

func rule1ShouldChangeState(grid Grid, x, y int) bool {
	// If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied (change state)
	if grid[y][x] == 'L' && !any(getAllAdjacent(grid, x, y), '#') {
		return true
	}
	return false
}

func rule2ShouldChangeState(grid Grid, x, y int) bool {
	// If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
	if grid[y][x] == '#' && arrCount(getAllAdjacent(grid, x, y), '#') >= 4 {
		return true
	}
	return false
}

func evalRound(grid Grid) Grid {
	newGrid := make(Grid, len(grid))
	for y, row := range grid {
		newGrid[y] = make([]rune, len(row))
		for x, cell := range row {
			if rule1ShouldChangeState(grid, x, y) {
				newGrid[y][x] = '#'
			} else if rule2ShouldChangeState(grid, x, y) {
				newGrid[y][x] = 'L'
			} else {
				newGrid[y][x] = cell
			}
		}
	}

	return newGrid
}

func main() {
	// filename := "day11/example"
	filename := "day11/input"
	grid := readFile2dSlice(filename)

	// fmt.Println("Starting grid:")
	// printGrid(grid)

	for i := 0; true; i++ {
		newGrid := evalRound(grid)

		// fmt.Println("")
		// fmt.Println("Round", i+1)
		// printGrid(newGrid)

		if isEqual(grid, newGrid) {
			fmt.Println("No change in grid after round", i+1)
			break
		}

		grid = newGrid
	}

	cnt := gridCount(grid, '#')
	fmt.Println("Part 1:", cnt)

	// (L) empty
	// (#) occupied
	// (.) floor

	fmt.Println("Done.")
}
