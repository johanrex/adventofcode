// day02.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <filesystem>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <utility>
#include <algorithm>
#include <regex>
#include <unordered_set>

using namespace std;

static string strip(const string& s)
{
    // Remove leading and trailing whitespaces.
    // The regex is static so it's compiled once.
    static const regex re(R"(^\s+|\s+$)");
    return regex_replace(s, re, string());
}

static vector<string> split(const string& s, char delim)
{
    vector<string> ret;
    size_t start = 0;
    while (true)
    {
        size_t pos = s.find(delim, start);
        ret.emplace_back(s.substr(start, pos == string::npos ? string::npos : pos - start));
        if (pos == string::npos) 
            break;
        start = pos + 1;
    }
    return ret;
}

// Pretty-printing helper
template<typename T, typename U>
std::ostream& operator<<(std::ostream& os, const std::pair<T, U>& p)
{
    return os << '(' << p.first << ", " << p.second << ')';
}

// Pretty-printing helper
template<typename T>
std::ostream& operator<<(std::ostream& os, const std::unordered_set<T>& s)
{
    os << '{';
    bool first = true;
    for (const auto& v : s)
    {
        if (!first) os << ", ";
        first = false;
        os << v;
    }
    return os << '}';
}

vector<pair<long long, long long>> parse(const string& filename)
{
    auto absPath = filesystem::absolute(filename);

    cout << "Reading: " << absPath << '\n';

    ifstream ifs(absPath);
    if (!ifs) 
		throw new runtime_error("Could not open file: " + absPath.string());

    string content((std::istreambuf_iterator<char>(ifs)), std::istreambuf_iterator<char>());

    content = strip(content);
    
    // remove newlines in the example input
    content.erase(remove(content.begin(), content.end(), '\n'), content.end());
    content.erase(remove(content.begin(), content.end(), '\r'), content.end());

	auto tmp = split(content, ',');

    vector<pair<long long, long long>> intervals;

    for(auto part: tmp)
    {
		auto toks = split(part, '-');
        long long a = stoll(toks[0]);
        long long b = stoll(toks[1]);
        intervals.emplace_back(a, b);
    }

    return intervals;
}


static bool is_repeated_twice(long long num)
{
    if (num < 10)
        return false;

    string s = to_string(num);
    if (s.length() % 2 == 1)
        return false;

    size_t half = s.length() / 2;
    string repeated = s.substr(0, half) + s.substr(0, half);
    return repeated == s;
}

static bool is_repeated_at_least_twice(long long num)
{
    if (num < 10)
        return false;

    string s = to_string(num);
    size_t L = s.length();

    for (size_t i = 0; i < L / 2; ++i)
    {
        size_t partLen = i + 1;
        if (L % partLen != 0)
            continue;

        string part = s.substr(0, partLen);
        size_t times = L / partLen;

        string repeated;
        repeated.reserve(partLen * times);
        for (size_t t = 0; t < times; ++t)
            repeated += part;

        if (repeated == s)
            return true;
    }

    return false;
}

static void part1(const vector<pair<long long, long long>>& intervals)
{
    unordered_set<long long> invalids;
    for (const auto& interval : intervals)
    {
        long long start = interval.first;
        long long end = interval.second;
        for (long long i = start; i <= end; ++i)
        {
            if (is_repeated_twice(i))
                invalids.insert(i);
        }

        //cout << interval << " -> " << invalids << endl;
    }

    long long ans = 0;
    for (long long v : invalids) 
        ans += v;

    cout << "Part 1: " << ans << endl;
}

static void part2(const vector<pair<long long, long long>>& intervals)
{
    unordered_set<long long> invalids;
    for (const auto& interval : intervals)
    {
        long long start = interval.first;
        long long end = interval.second;
        for (long long i = start; i <= end; ++i)
        {
            if (is_repeated_at_least_twice(i))
                invalids.insert(i);
        }

        // cout << interval << " -> " << invalids << endl;
    }

    long long ans = 0;
    for (long long v : invalids) 
        ans += v;

    cout << "Part 2: " << ans << endl;
}

int main()
{
    //print current working directory
    cout << filesystem::current_path() << '\n';

    //string filename = "../../example";
    string filename = "../../input";

    auto intervals = parse(filename);

    part1(intervals);
    part2(intervals);

    int i = 0;

}
