#include "cpp.h"

#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <filesystem>
#include <unordered_map>
#include <algorithm>
#include <cassert>

namespace fs = std::filesystem;
using namespace std;

vector<int> readInput(const string& filename)
{
    auto absPath = fs::absolute(filename);

    cout << "Reading: " << absPath << '\n';

    if (!fs::exists(absPath)) {
        throw runtime_error("file does not exist: " + absPath.string());
    }

    ifstream file(absPath);

    vector<int> ret;
    string line;
    while (getline(file, line)) {
        if (line.empty()) 
            continue;

        if (line[0] == 'L')
			line[0] = '-';
        else
            line[0] = ' ';

        ret.push_back(stoi(line));
    }
    return ret;
}

void part1(const vector<int>& input)
{
    int curr = 50;
    int pwd = 0;

    for (auto rot : input) {
        curr += rot;

        curr %= 100;
        if (curr < 0) 
            curr += 100;

        if (curr == 0)
            pwd++;
    }

    assert(pwd == 1034);
    cout << "Part 1: " << pwd << '\n';
}

void part2(const vector<int>& input)
{
    int curr = 50;
    long long pwd = 0;

    for (auto steps : input) {
        if (steps == 0)
            throw runtime_error("steps cannot be zero");

        long long passing_zero_cnt = 0;

        if (steps > 0) {
            passing_zero_cnt = (curr + steps) / 100;
        }
        else { // steps < 0
            if ((curr + steps) <= 0) {
                if (curr == 0) {
                    passing_zero_cnt = abs(static_cast<long long>(curr + steps)) / 100;
                }
                else {
                    passing_zero_cnt = (abs(static_cast<long long>(curr + steps)) / 100) + 1;
                }
            }
        }

        curr += steps;
        curr %= 100;
        if (curr < 0) curr += 100;

        pwd += passing_zero_cnt;
    }

    assert(pwd == 6166);
    cout << "Part 2: " << pwd << '\n';
}

int main()
{
    //auto input = readInput("../../../../../day01/example");
    auto input = readInput("../../../../../day01/input");

    part1(input);
    part2(input);

	//cin.get();

    return 0;
}
