#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <filesystem>

using namespace std;

class Grid
{
    private:
        vector<char> vect;

    public:
        size_t row_cnt = -1;
        size_t col_cnt = -1;

        Grid(size_t row_cnt, size_t col_cnt, char default_value)
        {
			this->row_cnt = row_cnt;
			this->col_cnt = col_cnt;

            vect.resize(row_cnt * col_cnt, default_value);
        }   

        void set_at(int row, int col, char value)
        {
			vect[row * col_cnt + col] = value;
		}

        inline bool is_roll_at(int row, int col) const
        {
            if (row < 0 || row >= row_cnt || col < 0 || col >= col_cnt)
            {
                return false;
            }
            return vect[row * col_cnt + col] == '@';
        }
};


static Grid parse(const string& filename)
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

	vector<string> lines;
    string line;

    while (getline(f, line))
    {
        lines.emplace_back(line);
    }

	size_t rowCnt = lines.size();
	size_t colCnt = lines[0].size();

    Grid grid(rowCnt, colCnt, '.');

    int row = 0;
    int col = 0;

    for (const auto& line : lines)
    {
        col = 0;
        for (char c : line)
        {
            grid.set_at(row, col, c);
            col++;
        }
        row++;
    }

    return grid;
}


vector<pair<int, int>> find_removable(Grid& grid)
{
    vector<pair<int, int>> removable;

    for (int r = 0; r < grid.row_cnt; r++)
    {
        for (int c = 0; c < grid.col_cnt; c++)
        {
            if (grid.is_roll_at(r, c))
            {
				int neighboring_rolls = 0;
                if (grid.is_roll_at(r - 1, c - 1)) neighboring_rolls++;
                if (grid.is_roll_at(r - 1, c)) neighboring_rolls++;
                if (grid.is_roll_at(r - 1, c + 1)) neighboring_rolls++;
                if (grid.is_roll_at(r, c - 1)) neighboring_rolls++;
                if (grid.is_roll_at(r, c + 1)) neighboring_rolls++;
                if (grid.is_roll_at(r + 1, c - 1)) neighboring_rolls++;
                if (grid.is_roll_at(r + 1, c)) neighboring_rolls++;
                if (grid.is_roll_at(r + 1, c + 1)) neighboring_rolls++;

                if (neighboring_rolls < 4)
                {
					removable.emplace_back(r, c);
                }
            }
        }
    }
    return removable;
}


void part1(Grid& grid)
{
    auto removable = find_removable(grid);
    cout << "Part 1: " << removable.size() << endl;
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
            grid.set_at(pos.first, pos.second, '.');
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