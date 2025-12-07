#include <fstream>
#include <iostream>
#include <string>
#include <filesystem>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include "default_grid.h"
#include "utils.h"

using namespace std;

using ll = long long;
using range = pair<ll, ll>;
using Grid = DefaultGrid<char, '.'>;

unordered_set<pair<int, int>, IntPairPackerFunctor> splitters_reached;
unordered_map<pair<int, int>, ll, IntPairPackerFunctor> memo;

void parse(const string& filename, Grid& grid, pair<int, int>& s_pos)
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

	string line;
	int row_idx = 0;
	int col_idx = 0;
	while (getline(f, line))
	{
		col_idx = 0;
		for (char c : line)
		{
			grid.set_at(row_idx, col_idx, c);

			if (c == 'S')
			{
				s_pos = {row_idx, col_idx};
			}
			col_idx++;
		}

		row_idx++;
	}
}

void beam_from_point_p1(Grid& grid, int start_row, int start_col)
{
	if (start_row >= grid.rows() || start_col < 0 || start_col >= grid.cols())
		return;

	char curr_val = grid.get_at(start_row, start_col);

	if (curr_val == '.')
	{
		grid.set_at(start_row, start_col, '|');
		beam_from_point_p1(grid, start_row + 1, start_col);
	}
	else if (curr_val == '^')
	{
		splitters_reached.insert({start_row, start_col});
		beam_from_point_p1(grid, start_row, start_col - 1);
		beam_from_point_p1(grid, start_row, start_col + 1);
	}
}

ll beam_from_point_p2(Grid& grid, int start_row, int start_col)
{
	if (start_row >= grid.rows() || start_col < 0 || start_col >= grid.cols())
		return 1;

	if (memo.contains({start_row, start_col}))
		return memo[{start_row, start_col}];

	char curr_val = grid.get_at(start_row, start_col);

	ll timelines = 0;
	if (curr_val == '.')
	{
		timelines += beam_from_point_p2(grid, start_row + 1, start_col);
	}
	else if (curr_val == '^')
	{
		timelines += beam_from_point_p2(grid, start_row, start_col - 1);
		timelines += beam_from_point_p2(grid, start_row, start_col + 1);
	}

	memo[{start_row, start_col}] = timelines;
	return timelines;
}

void part1(Grid grid, const pair<int, int>& s_pos)
{
	splitters_reached.clear();
	
	int s_col = s_pos.second;
	beam_from_point_p1(grid, 1, s_col);

	auto ans = splitters_reached.size();
	cout << "Part 1: " << ans << endl;
}

void part2(Grid grid, const pair<int, int>& s_pos)
{
	memo.clear();
	
	int s_col = s_pos.second;
	auto timelines = beam_from_point_p2(grid, 1, s_col);

	cout << "Part 2: " << timelines << endl;
}

int main()
{
	//string filename = "../../../../example";
	string filename = "../../../../input";

	Grid grid;
	pair<int, int> s_pos;
	parse(filename, grid, s_pos);

	part1(Grid(grid), s_pos); // copy constructor so we don't modify original grid
	part2(grid, s_pos);

	return 0;
}
