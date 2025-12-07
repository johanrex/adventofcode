#pragma once

#include <utility>  // for std::pair
#include <cstddef>  // for size_t

static_assert(sizeof(int) == 4, "we need to pack two ints in one size_t for PairHash to work.");
static_assert(sizeof(size_t) == 8, "we need to pack two ints in one size_t for PairHash to work.");

//Collision free mapping of two 32 bit ins to one 64 bit int
struct IntPairPackerFunctor
{
	size_t operator()(const std::pair<int, int>& p) const
	{
		size_t h1 = p.first; //implicit cast from int to size_t with sign extension in case of negative value
		size_t h2 = p.second; //implicit cast from int to size_t with sign extension in case of negative value
		h2 &= 0x00000000FFFFFFFF; // in case we get negative second value, we need to zero the upper bits so we can add them safely OR then without sign extension messing things up. 
		return (h1 << 32) | h2;
	}
};
