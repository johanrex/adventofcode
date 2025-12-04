#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <filesystem>

using namespace std;


struct PairHash
{
    size_t operator()(const pair<int, int>& p) const noexcept
    {
        // combine two 32-bit ints into a 64-bit value, then hash
        return std::hash<unsigned long long>()(
            (static_cast<unsigned long long>(static_cast<unsigned int>(p.first)) << 32) ^ static_cast<unsigned int>(p.second));
    }
};


class Grid
{
    private:
        unordered_map<pair<int, int>, char, PairHash> map;
		char defaultValue;

    public:
        int RowCnt;
        int ColCnt;

        Grid(char defaultValue)
        {
			this->defaultValue = defaultValue;
        }

        void Set(int row, int col, char value)
        {
            map[{row, col}] = value;
		}

        char GetOrDefault(int row, int col, char defaultValue)
        {
            auto it = map.find({row, col});
            if (it != map.end())
            {
                return it->second;
            }
            return defaultValue;
        }
};


static Grid parse(const string& filename)
{
    string fileInfo;
    fileInfo += "This is the current working directory: " + filesystem::current_path().string() + ".\n";
	fileInfo += "Filename supplied: " + filename + ".\n";
	fileInfo += "Resolves to absolute path: " + filesystem::absolute(filename).string() + ".\n";

    if (!filesystem::exists(filename))
    {
        cerr << fileInfo << endl;
        cerr << "Error: file does not exist: " << filesystem::absolute(filename) << endl;
		throw runtime_error("file does not exist");
    }

    ifstream f(filename);

    Grid grid('@');

    int row = 0;
    int col = 0;

    string line;

    while (getline(f, line))
    {
        col = 0;
        for (char c : line)
        {
            grid.Set(row, col, c);
            col++;
        }
        row++;
    }

	grid.RowCnt = row;
	grid.ColCnt = col;

    return grid;
}



vector<pair<int, int>> find_removable(Grid& grid)
{
    vector<pair<int, int>> removable;

    for (int r = 0; r < grid.RowCnt; r++)
    {
        for (int c = 0; c < grid.ColCnt; c++)
        {
            char curr_val = grid.GetOrDefault(r, c, ' ');
            if (curr_val == '@')
            {
                // get neighbors in all 8 directions
                vector<char> neighbor_vals = {
                    grid.GetOrDefault(r - 1, c - 1, ' '),
                    grid.GetOrDefault(r - 1, c, ' '),
                    grid.GetOrDefault(r - 1, c + 1, ' '),
                    grid.GetOrDefault(r, c - 1, ' '),
                    grid.GetOrDefault(r, c + 1, ' '),
                    grid.GetOrDefault(r + 1, c - 1, ' '),
                    grid.GetOrDefault(r + 1, c, ' '),
                    grid.GetOrDefault(r + 1, c + 1, ' ')
                };
                auto cnt = count(neighbor_vals.begin(), neighbor_vals.end(), '@');
                if (cnt < 4)
                {
                    removable.push_back({r, c});
                }
            }
        }
    }
    return removable;
}


void part1(Grid& grid)
{
    auto removable = find_removable(grid);
    cout << "Part 1:" << removable.size() << endl;
}

void part2(Grid& grid)
{
    size_t total_removed = 0;
    while (true)
    {
        auto removable = find_removable(grid);
        if (removable.size() == 0)
        {
            break;
        }
        for (const auto& pos : removable)
        {
            grid.Set(pos.first, pos.second, ' ');
        }
        total_removed += removable.size();
    }
    cout << "Part 2: " << total_removed << endl;
}

int main()
{
    //string filename = "../../../../example";
    string filename = "../../../../input";

    auto grid = parse(filename);
	part1(grid);
    part2(grid);

	return 0;
}
