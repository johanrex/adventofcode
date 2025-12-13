#pragma once
#include <regex>
#include <string>
#include <vector>

// TODO put in namespace?

inline std::string strip(const std::string &s)
{
    // Remove leading and trailing whitespaces.
    // The regex is static so it's compiled once.
    static const std::regex re(R"(^\s+|\s+$)");
    return std::regex_replace(s, re, std::string());
}

inline std::vector<std::string> split(const std::string &s, char delim)
{
    std::vector<std::string> ret;
    size_t start = 0;
    while (true)
    {
        size_t pos = s.find(delim, start);
        ret.emplace_back(s.substr(start, pos == std::string::npos ? std::string::npos : pos - start));
        if (pos == std::string::npos)
            break;
        start = pos + 1;
    }
    return ret;
}