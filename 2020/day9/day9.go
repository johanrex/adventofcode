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

func part1(ints []int, preambleLength int) int {
	isValid := func(preamble []int, target int) bool {
		for i := 0; i < len(preamble); i++ {
			for j := i + 1; j < len(preamble); j++ {
				if preamble[i]+preamble[j] == target {
					return true
				}
			}
		}
		return false
	}

	ret := -1

	for i := preambleLength; i < len(ints); i++ {
		preamble := ints[i-preambleLength : i]

		current := ints[i]

		if !isValid(preamble, current) {
			ret = current
			break
		}

	}

	return ret
}

func part2(ints []int, target int) int {
	windowStartIdx := 0
	windowEndIdx := 1
	windowSum := ints[windowStartIdx] + ints[windowEndIdx]

	for windowSum != target {
		if windowSum == target {
			break
		} else if windowSum < target {
			windowEndIdx++
			windowSum += ints[windowEndIdx]
		} else {
			windowSum -= ints[windowStartIdx]
			windowStartIdx++
		}
	}
	windowSlice := ints[windowStartIdx:windowEndIdx]
	sort.Ints(windowSlice)
	encryptionWeakness := windowSlice[0] + windowSlice[len(windowSlice)-1]

	return encryptionWeakness
}

func main() {
	cwd, err := os.Getwd()
	if err != nil {
		log.Fatalf("os.Getwd failed: %s", err)
	}

	fmt.Println("cwd:", cwd)

	var filename string
	var preambleLength int

	if true {
		filename = "day9/input"
		preambleLength = 25
	} else {
		filename = "day9/example"
		preambleLength = 5
	}

	fmt.Println("filename:", filename)
	fmt.Println("preamble:", preambleLength)

	ints := readFileLinesInts(filename)

	part1 := part1(ints, preambleLength)
	fmt.Println("Part 1:", part1)

	part2 := part2(ints, part1)
	fmt.Println("Part 2:", part2)

	fmt.Println("Done.")
}
