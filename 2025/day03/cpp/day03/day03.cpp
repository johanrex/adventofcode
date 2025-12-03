#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <cassert>

using namespace std;


using ll = long long;

vector<vector<int>> parse(string& filename)
{
    vector<vector<int>> data;
    ifstream f(filename);
    string line;

    while (getline(f, line))
    {
        vector<int> row;
        for (char c : line)
            row.emplace_back(c - '0');
        data.emplace_back(row);
    }

    return data;

}

ll findJoltage(const vector<vector<int>>& data, int size)
{
    ll ans = 0;

    for (const auto& row : data)
    {
        int tmp_size = size;
        vector<int> batteries;
        int max_battery_idx = -1;

        while (tmp_size > 0)
        {
            int max_battery = -1;
            int rowLength = (int)row.size();
            for (int i = max_battery_idx + 1; i <= rowLength - tmp_size; ++i)
            {
                if (row[i] > max_battery)
                {
                    max_battery = row[i];
                    max_battery_idx = i;
                }
            }

            batteries.emplace_back(max_battery);
            tmp_size--;
        }

        ll tmp = 0;
        for (int d : batteries)
            tmp = tmp * 10 + d;

        ans += tmp;
    }

    return ans;
}

int main()
{
    //string filename = "../../example";
    string filename = "../../input";

    auto data = parse(filename);

    auto p1 = findJoltage(data, 2);
    cout << "Part 1:" << p1 << endl;

    auto p2 = findJoltage(data, 12);
    cout << "Part 2:" << p2 << endl;
}
