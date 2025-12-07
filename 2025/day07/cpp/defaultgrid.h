#pragma once

#include <unordered_map>
#include <utility>
#include <functional>
#include <algorithm>

using namespace std;

static_assert(sizeof(size_t) == 2 * sizeof(int), "we need to pack two ints in one size_t for PairHash to work.");

template<typename T, T default_value>
class DefaultGrid
{
private:
	struct PairHash
	{
		size_t operator()(const pair<int, int>& p) const
		{
			size_t h1 = p.first;
			size_t h2 = p.second;
			return (h1 << 32) + h2;
		}
	};

	unordered_map<pair<int, int>, T, PairHash> nodes;
	int max_row = -1;
	int max_col = -1;

public:
	T get_at(int row, int col) const
	{
		auto it = nodes.find({row, col});
		if (it != nodes.end())
		{
			return it->second;
		}
		return default_value;
	}

	void set_at(int row, int col, T value)
	{
		nodes[{row, col}] = value;
		max_row = max(max_row, row);
		max_col = max(max_col, col);
	}

	int rows() const
	{
		return max_row + 1;
	}

	int cols() const
	{
		return max_col + 1;
	}
};
