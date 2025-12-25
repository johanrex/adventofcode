#include "file_utils.h"
#include "string_utils.h"
#include <algorithm>
#include <iostream>
#include <string>

using namespace std;
using ll = long long;

struct Point
{
    ll row = 0;
    ll col = 0;
};

vector<Point> parse(const string &filename)
{
    auto lines = read_as_strings(filename);

    vector<Point> polygon;
    for (auto &line : lines)
    {
        line = strip(line);
        auto nrs = split(line, ',');

        Point p;
        p.row = stoul(nrs[0]);
        p.col = stoul(nrs[1]);

        polygon.emplace_back(p);
    }
    return polygon;
};

bool is_point_inside_polygon(const Point &p, const vector<pair<Point, Point>> &vertical_lines)
{
    // Determines if the point is inside the polygon by using ray-casting.
    // Cast a ray from the starting point to the right and count how many times it crosses vertical polygon edges.
    // This is slightly different than a normal grid based approach.

    ll row = p.row;
    ll col = p.col;
    size_t crosses_cnt = 0;
    for (const auto &[p1, p2] : vertical_lines)
    {
        ll s_col = p1.col;
        ll s_min_row = min(p1.row, p2.row);
        ll s_max_row = max(p1.row, p2.row);

        if (s_min_row < row && row < s_max_row && col <= s_col)
            crosses_cnt++;
    }
    return (crosses_cnt % 2) == 1;
}

void part1(const vector<Point> &polygon)
{
    ll max_area = -1;
    for (size_t i = 0; i < polygon.size(); i++)
    {
        auto &p1 = polygon[i];
        for (size_t j = i + 1; j < polygon.size(); j++)
        {
            auto &p2 = polygon[j];

            ll area = (abs(p1.row - p2.row) + 1) * (abs(p1.col - p2.col) + 1);
            max_area = max(area, max_area);
        }
    }

    cout << "Part 1: " << max_area << "\n";
}

void part2(const vector<Point> &polygon)
{
    // visual inspection of input data to find two inner points
    Point a = {94808, 48629};
    Point b = {94808, 50147};

    ll max_area = -1;

    // vertical line segments for ray casting
    vector<pair<Point, Point>> vertical_line_segments;
    {
        for (size_t i = 0; i < polygon.size(); i++)
        {
            auto &p1 = polygon[i];
            auto &p2 = polygon[(i + 1) % polygon.size()];

            if (p1.col == p2.col)
            {
                pair<Point, Point> p{p1, p2};
                vertical_line_segments.emplace_back(p);
            }
        }
    }

    for (auto &far_corner : polygon)
    {
        Point inner_corner;
        if (far_corner.col < a.col)
            inner_corner = a;
        else if (far_corner.col > b.col)
            inner_corner = b;
        else
            continue;

        ll area = (abs(far_corner.row - inner_corner.row) + 1) * (abs(far_corner.col - inner_corner.col) + 1);

        if (area > max_area)
        {
            if (!is_point_inside_polygon({inner_corner.row, far_corner.col}, vertical_line_segments))
                continue;
            if (!is_point_inside_polygon({far_corner.row, inner_corner.col}, vertical_line_segments))
                continue;

            max_area = area;
        }
    }
    cout << "Part 2: " << max_area << "\n";
}

int main()
{
    auto polygon = parse("../input");
    part1(polygon);
    part2(polygon);

    return 0;
}
