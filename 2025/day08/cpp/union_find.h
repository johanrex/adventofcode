#pragma once

#include <cstddef>
#include <stdexcept>
#include <vector>

// Implements the canonical Union-Find (Disjoint Set Union) data structure
// with path compression (path halving) and union by size.
// Uses 0-based indexing for elements.
class UnionFind
{
  public:
    // Construct with n elements: 0..n-1
    explicit UnionFind(size_t n) : parent_(n), size_(n, 1), components_(n)
    {
        if (n <= 0)
        {
            throw std::invalid_argument("n must be positive");
        }
        for (size_t i = 0; i < n; ++i)
            parent_[i] = i;
    }

    // Returns the representative root of the set containing x
    size_t find(size_t x)
    {
        // Path compression via path halving
        while (x != parent_[x])
        {
            parent_[x] = parent_[parent_[x]];
            x = parent_[x];
        }
        return x;
    }

    // Merge the sets containing a and b. Returns true if merged; false if already in same set.
    bool merge(size_t a, size_t b)
    {
        size_t ra = find(a);
        size_t rb = find(b);
        if (ra == rb)
            return false;

        // Union by size: attach smaller under larger
        if (size_[ra] < size_[rb])
            std::swap(ra, rb);
        parent_[rb] = ra;
        size_[ra] += size_[rb];
        --components_;
        return true;
    }

    // Check if a and b are in the same set
    bool connected(size_t a, size_t b)
    {
        return find(a) == find(b);
    }

    // Size of the component containing x
    size_t component_size(size_t x)
    {
        return size_[find(x)];
    }

    // Sizes of all components (indexed by root)
    std::vector<size_t> component_sizes()
    {
        return size_;
    }

    // Number of disjoint components
    size_t components() const
    {
        return components_;
    }

  private:
    std::vector<size_t> parent_;
    std::vector<size_t> size_;
    size_t components_;
};
