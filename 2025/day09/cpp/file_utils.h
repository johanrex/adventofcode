#pragma once
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

// TODO put in namespace?

inline std::vector<std::string> read_as_strings(const std::string &filename)
{
    if (!std::filesystem::exists(filename))
    {
        std::string fileInfo;
        fileInfo += "This is the current working directory: " + std::filesystem::current_path().string() + ".\n";
        fileInfo += "Filename supplied: " + filename + ".\n";
        fileInfo += "It resolves to absolute path: " + std::filesystem::absolute(filename).string() + ".\n";

        std::cerr << fileInfo << std::endl;
        throw std::runtime_error("file does not exist");
    }

    std::ifstream f(filename);
    if (!f.is_open())
    {
        std::cerr << "Error opening file: " << filename << std::endl;
        throw std::runtime_error("error opening file");
    }

    std::vector<std::string> lines;
    std::string line;
    while (std::getline(f, line))
        lines.push_back(line);

    return lines;
}
