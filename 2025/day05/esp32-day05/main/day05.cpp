#include <stdio.h>
#include <inttypes.h>
// #include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_chip_info.h"
#include "esp_flash.h"
#include "esp_system.h"

#include <fstream>
#include <iostream>
#include <string>
#include <filesystem>
#include <vector>
#include <algorithm>
#include "input.h"


using namespace std;

using ll = long long;
using range = pair<ll, ll>;

void parse(vector<range> &ranges, vector<ll> &ingredients)
{
    bool first_part = true;
    string line;

    for (auto line : INPUT_DATA)
    {
        if (line.empty())
        {
            first_part = false;
            continue;
        }

        if (first_part)
        {
            // ranges
            size_t dash_pos = line.find('-');
            ll start = stoll(line.substr(0, dash_pos));
            ll end = stoll(line.substr(dash_pos + 1));
            ranges.emplace_back(start, end);
        }
        else
        {
            // ingredients
            ingredients.emplace_back(stoll(line));
        }
    }
}

vector<range> merge_ranges(vector<range> &ranges)
{
    // sort input on start
    sort(ranges.begin(), ranges.end());

    vector<range> ans;

    for (const auto &range : ranges)
    {
        if (ans.empty())
        {
            ans.emplace_back(range);
        }
        else
        {
            ll prev_end = ans.back().second;
            ll curr_start = range.first;
            ll curr_end = range.second;

            // start new range
            if (curr_start > prev_end)
            {
                ans.emplace_back(range);
            }
            // extend prev range
            else
            {
                if (curr_end > prev_end)
                {
                    ll start = ans.back().first;
                    ans.back() = {start, curr_end};
                }
            }
        }
    }

    return ans;
}

void part1(const vector<range> &ranges, const vector<ll> &ingredients)
{
    ll fresh_cnt = 0;

    for (ll ingredient : ingredients)
    {
        for (const auto &[start, end] : ranges)
        {
            if (start <= ingredient && ingredient <= end)
            {
                fresh_cnt++;
                break;
            }
        }
    }

    cout << "Part 1: " << fresh_cnt << endl;
}

void part2(vector<range> &ranges)
{
    auto merged = merge_ranges(ranges);

    ll total_span = 0;
    for (const auto &[start, end] : merged)
    {
        total_span += end - start + 1;
    }

    cout << "Part 2: " << total_span << endl;
}

extern "C" void app_main(void)
{
    vector<range> ranges;
    vector<ll> ingredients;

    parse(ranges, ingredients);
    part1(ranges, ingredients);
    part2(ranges);

    for (int i = 10; i >= 0; i--)
    {
        printf("Restarting in %d seconds...\n", i);
        vTaskDelay(pdMS_TO_TICKS(1000)); // avoids CONFIG_FREERTOS_HZ/configTICK_RATE_HZ issues
    }
    // printf("Restarting now.\n");
    // fflush(stdout);
    esp_restart();
}
