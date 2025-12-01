#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <filesystem>
#include <unordered_map>
#include <algorithm>

namespace fs = std::filesystem;
using namespace std;

vector<int> readInts(const string& filename)
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
        if (line.empty()) continue;
        ret.push_back(stoi(line));
    }
    return ret;
}

void part1(const vector<int>& input)
{
    unordered_map<int, int> diffs;
    int prev = 0;
    int diff = 0;
    for (auto i: input)
    {
        diff = i - prev;
        diffs[diff]++;
        prev = i;
    }

    int ans = diffs[1] * diffs[3];
    cout << "Part 1: " << ans << endl;
}

unordered_map<int, int64_t> memo;
int64_t stepCounter(const vector<int>& input, int i)
{
    if (i == input.size()-1)
        return 1;

    if (memo.contains(i))
        return memo[i]; 

    int64_t ans = 0;
    for (int j = i+1; j < input.size() ; j++)
    {
        if (input[j] - input[i] <= 3)
            ans += stepCounter(input, j);
    }

    memo[i] = ans;

    return ans;
}

void part2(const vector<int>& input)
{
    auto ans = stepCounter(input, 0);
    cout << "Part 2: " << ans << endl;
}

int main()
{
    auto input = readInts("day10/example");

    sort(input.begin(), input.end());
    input.insert(input.begin(), 0); // add the charging outlet
    input.emplace_back(input.back() + 3); // add the device built-in adapter

    part1(input);
    part2(input);

    cout << "Done." << endl;
    return 0;
}
