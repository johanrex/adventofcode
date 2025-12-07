#pragma once

#include <unordered_map>
#include <utility>
#include <functional>
#include <algorithm>
#include "utils.h"

using namespace std;

template<typename T, T default_value>
class DefaultGrid
{
private:
	unordered_map<pair<int, int>, T, IntPairPackerFunctor> nodes;
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
