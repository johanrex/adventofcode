from dataclasses import dataclass, field
import re
from typing import Self
import sys


@dataclass
class FsItem:
    name: str


@dataclass
class FsFile(FsItem):
    size: int


@dataclass
class FsDir(FsItem):
    dirs: list[Self] = field(default_factory=list)
    files: list[FsFile] = field(default_factory=list)


def parse_input(lines) -> FsDir:
    with open(filename) as f:
        lines = [line.strip() for line in f]

    cwd: list[FsDir] = []
    root = None
    for line in lines:

        if line.startswith("$ cd /"):
            assert len(cwd) == 0
            root = FsDir("/")
            cwd.append(root)
        elif line.startswith("$ cd .."):
            cwd.pop()
        elif line.startswith("$ cd "):
            dirname = line[len("$ cd ") :]

            directory = next((child for child in cwd[-1].dirs if child.name == dirname), None)
            if directory is None:
                directory = FsDir(dirname)
                cwd[-1].dirs.append(directory)

            cwd.append(directory)
        elif line.startswith("$ ls"):
            pass
        else:
            # is output of ls
            x, name = line.split(" ")
            if x.isnumeric():
                size = int(x)

                file = next((child for child in cwd[-1].files if child.name == name), None)
                if file is None:
                    cwd[-1].files.append(FsFile(filename, size))
    return root


def dfs(fs_dir: FsDir):
    global dirsizes
    dirsize = 0

    for child_dir in fs_dir.dirs:
        dirsize += dfs(child_dir)

    dirsize += sum(fs_file.size for fs_file in fs_dir.files)
    dirsizes.append(dirsize)

    # print(f"Size of '{fs_dir.name}': {dirsize}")
    return dirsize


filename = "7/input"
# filename = "7/example"
root = parse_input(filename)

part1_size = 0
dirsizes = []
dfs(root)

part1_size = sum([dirsize for dirsize in dirsizes if dirsize <= 100000])
assert part1_size == 1908462
print("Part1:", part1_size)

total_dirsize = max(dirsizes)
part2_size = min([dirsize for dirsize in dirsizes if (70000000 - total_dirsize + dirsize) >= 30000000])
assert part2_size == 3979145
print("Part2:", part2_size)
