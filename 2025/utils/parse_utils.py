import re


def parse_ints(filename: str):
    ints = []
    with open(filename) as f:
        for line in f:
            ints.append(list(map(int, re.findall(r"\d+", line))))
    return ints


def parse_strs(filename: str):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
    return lines


def parse_str(filename: str):
    with open(filename) as f:
        text = f.read()

    return text
