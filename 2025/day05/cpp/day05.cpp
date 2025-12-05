#include <fstream>
#include <iostream>
#include <string>
#include <filesystem>
#include <vector>
#include <algorithm>

using namespace std;

using ll = long long;
using range = pair<ll, ll>;


void parse(const string& filename, vector<range>& ranges, vector<ll>& ingredients)
{
	if (!filesystem::exists(filename))
	{
		string fileInfo;
		fileInfo += "This is the current working directory: " + filesystem::current_path().string() + ".\n";
		fileInfo += "Filename supplied: " + filename + ".\n";
		fileInfo += "Resolves to absolute path: " + filesystem::absolute(filename).string() + ".\n";

		cerr << fileInfo << endl;
		cerr << "Error: file does not exist: " << filesystem::absolute(filename) << endl;
		throw runtime_error("file does not exist");
	}

	ifstream f(filename);
	if (!f.is_open())
	{
		cerr << "Error opening file: " << filename << endl;
		throw runtime_error("error opening file");
	}

	bool first_part = true;
	string line;

	while (getline(f, line))
	{
		if (line.empty())
		{
			first_part = false;
			continue;
		}

		if (first_part)
		{
			// ranges
			size_t dash_pos = line.find('-');
			ll start = stoll(line.substr(0, dash_pos));
			ll end = stoll(line.substr(dash_pos + 1));
			ranges.emplace_back(start, end);
		}
		else
		{
			// ingredients
			ingredients.emplace_back(stoll(line));
		}
	}

	f.close();
}

vector<range> merge_ranges(vector<range>& ranges)
{
	// sort input on start
	sort(ranges.begin(), ranges.end());

	vector<range> ans;

	for (const auto& range : ranges)
	{
		if (ans.empty())
		{
			ans.emplace_back(range);
		}
		else
		{
			ll prev_end = ans.back().second;
			ll curr_start = range.first;
			ll curr_end = range.second;

			// start new range
			if (curr_start > prev_end)
			{
				ans.emplace_back(range);
			}
			// extend prev range
			else
			{
				if (curr_end > prev_end)
				{
					ll start = ans.back().first;
					ans.back() = {start, curr_end};
				}
			}
		}
	}

	return ans;
}

void part1(const vector<range>& ranges, const vector<ll>& ingredients)
{
	ll fresh_cnt = 0;

	for (ll ingredient : ingredients)
	{
		for (const auto& [start, end] : ranges)
		{
			if (start <= ingredient && ingredient <= end)
			{
				fresh_cnt++;
				break;
			}
		}
	}

	cout << "Part 1: " << fresh_cnt << endl;
}

void part2(vector<range>& ranges)
{
	auto merged = merge_ranges(ranges);

	ll total_span = 0;
	for (const auto& [start, end] : merged)
	{
		total_span += end - start + 1;
	}

	cout << "Part 2: " << total_span << endl;
}

int main()
{
	//string filename = "../../../../example";
	string filename = "../../../../input";

	vector<range> ranges;
	vector<ll> ingredients;

	parse(filename, ranges, ingredients);
	part1(ranges, ingredients);
	part2(ranges);

	return 0;
}
