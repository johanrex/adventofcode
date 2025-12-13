#include "file_utils.h"
#include "string_utils.h"
#include "union_find.h"
#include <algorithm>
#include <functional>
#include <iostream>
#include <string>
#include <unordered_map>

using namespace std;
using ll = long long;

struct Point
{
    ll x = 0;
    ll y = 0;
    ll z = 0;
    bool operator==(Point const &o) const noexcept = default; // TODO wtf is this.
};

template <>
struct hash<Point>
{
    size_t operator()(Point const &p) const noexcept
    {
        // combine hashes of components (boost::hash_combine style)
        size_t h1 = std::hash<size_t>{}(p.x);
        size_t h2 = std::hash<size_t>{}(p.y);
        size_t h3 = std::hash<size_t>{}(p.z);

        size_t seed = h1;
        seed ^= h2 + 0x9e3779b97f4a7c15ULL + (seed << 6) + (seed >> 2);
        seed ^= h3 + 0x9e3779b97f4a7c15ULL + (seed << 6) + (seed >> 2);
        return seed;
    }
};

struct DistInfo
{
    double dist;
    size_t i;
    size_t j;
};

vector<Point> parse(const string &filename)
{
    auto lines = read_as_strings(filename);

    vector<Point> points;
    for (auto &line : lines)
    {
        line = strip(line);
        auto nrs = split(line, ',');

        points.push_back(Point{
            stoul(nrs[0]),
            stoul(nrs[1]),
            stoul(nrs[2])});
    }
    return points;
};

void solve(vector<Point> &points)
{
    const size_t n = points.size();

    unordered_map<Point, size_t> point_to_idx;
    point_to_idx.reserve(n);
    for (size_t i = 0; i < n; ++i)
        point_to_idx[points[i]] = i;

    // Compute all pairwise squared distances
    vector<DistInfo> dists;
    dists.reserve(n * (n - 1));
    for (size_t i = 0; i < n; ++i)
    {
        Point p1 = points[i];

        for (size_t j = i + 1; j < n; ++j)
        {
            Point p2 = points[j];

            ll dist = (pow(p1.x - p2.x, 2) +
                       pow(p1.y - p2.y, 2) +
                       pow(p1.z - p2.z, 2));

            DistInfo info;
            info.dist = dist;
            info.i = i;
            info.j = j;
            dists.push_back(info);
        }
    }

    sort(
        dists.begin(),
        dists.end(),
        [](const DistInfo &a, const DistInfo &b)
        { return a.dist < b.dist; });

    const size_t connections_to_make = (n == 20) ? 10u : 1000u;

    ll p1_ans = 0;
    ll p2_ans = 0;

    UnionFind uf(n);

    for (size_t i = 0; i < dists.size(); ++i)
    {
        const auto &distinfo = dists[i];
        if (uf.merge(distinfo.i, distinfo.j))
            p2_ans = points[distinfo.i].x * points[distinfo.j].x;

        if (i + 1 == connections_to_make)
        {
            auto sizes = uf.component_sizes();
            sort(sizes.begin(), sizes.end(), greater<size_t>());
            p1_ans = sizes[0] * sizes[1] * sizes[2];
        }
    }

    if (p1_ans != 97384)
        throw runtime_error("Unexpected: did not reach expected number of components");
    if (p2_ans != 9003685096ll)
        throw runtime_error("Unexpected: Part 2 did not reach expected value");

    cout << "Part 1: " << p1_ans << "\n";
    cout << "Part 2: " << p2_ans << "\n";
}

int main()
{
    auto points = parse("../input");
    solve(points);

    return 0;
}
