from typing import List

def read_file(filename: str) -> List[str]:

    with(open(filename, "r")) as f:
        s = f.read().splitlines()

    return s
