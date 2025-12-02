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

using ll = long long;
using Interval = std::pair<ll, ll>;
using Intervals = std::vector<Interval>;


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

vector<Interval> parse(const string& filename)
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

    vector<Interval> intervals;

    for(auto part: tmp)
    {
		auto toks = split(part, '-');
        ll a = stoll(toks[0]);
        ll b = stoll(toks[1]);
        intervals.emplace_back(a, b);
    }

    return intervals;
}

static bool is_repeated_twice(ll num)
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

static bool is_repeated_at_least_twice(ll num)
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

static void part1(const vector<Interval>& intervals)
{
    unordered_set<ll> invalids;
    for (const auto& interval : intervals)
    {
        ll start = interval.first;
        ll end = interval.second;
        for (ll i = start; i <= end; ++i)
        {
            if (is_repeated_twice(i))
                invalids.insert(i);
        }

        //cout << interval << " -> " << invalids << endl;
    }

    ll ans = 0;
    for (ll v : invalids) 
        ans += v;

    cout << "Part 1: " << ans << endl;
}

static void part2(const vector<Interval>& intervals)
{
    unordered_set<ll> invalids;
    for (const auto& interval : intervals)
    {
        ll start = interval.first;
        ll end = interval.second;
        for (ll i = start; i <= end; ++i)
        {
            if (is_repeated_at_least_twice(i))
                invalids.insert(i);
        }

        // cout << interval << " -> " << invalids << endl;
    }

    ll ans = 0;
    for (ll v : invalids) 
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
