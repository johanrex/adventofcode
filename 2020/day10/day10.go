package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
)

func readFileLinesInts(filename string) []int {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatalf("failed to open file: %s", err)
	}
	defer file.Close()

	var ints []int
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		num, err := strconv.Atoi(line)
		if err != nil {
			log.Fatalf("failed to convert line to int: %s", err)
		}

		ints = append(ints, num)
	}

	if err := scanner.Err(); err != nil {
		log.Fatalf("failed to read lines: %s", err)
	}

	return ints
}

func part1(ints []int) int {
	ret := -1

	diff1 := 0
	diff3 := 0

	for i := 1; i < len(ints); i++ {
		diff := ints[i] - ints[i-1]
		if diff == 1 {
			diff1++
		} else if diff == 3 {
			diff3++
		}
	}

	ret = diff1 * diff3
	return ret

}

func part2(ints []int) int {
	// create a map of all possible arrangements. Map is used for fast lookup.
	arrangements := make(map[string]bool)

	var dfs func([]int)
	dfs = func(ints []int) {
		//create string representation of the arrangement
		str := fmt.Sprintf("%v", ints)

		// Check if the arrangement is already in the map of arrangements
		if arrangements[str] {
			return
		}

		arrangements[str] = true

		// fmt.Println(str)

		for i := 2; i < len(ints)-1; i++ {
			a := ints[i-2]
			// b := ints[i-1]
			c := ints[i]

			// can the middle adapter be removed?
			if c-a <= 3 {
				// remove the middle adapter
				mutatedInts := append([]int(nil), ints[:i-1]...)
				mutatedInts = append(mutatedInts, ints[i:]...)

				// fmt.Println(mutatedInts)
				dfs(mutatedInts)
			}

		}
	}

	dfs(ints)

	return len(arrangements)

}

func main() {
	cwd, err := os.Getwd()
	if err != nil {
		log.Fatalf("os.Getwd failed: %s", err)
	}

	fmt.Println("cwd:", cwd)

	var filename string

	if true {
		filename = "day10/input"
	} else {
		filename = "day10/example"
	}

	fmt.Println("filename:", filename)

	ints := readFileLinesInts(filename)

	sort.Ints(ints)

	//add the charging outlet
	ints = append([]int{0}, ints...)

	//add the device's built-in adapter
	ints = append(ints, ints[len(ints)-1]+3)

	part1 := part1(ints)
	fmt.Println("Part 1:", part1)

	// TODO wrong approach
	// part2 := part2(ints)
	// fmt.Println("Part 2:", part2)

	fmt.Println("Done.")
}
