def parse(filename) -> list[int]:
    data = []
    with open(filename) as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            ints = [int(c) for c in line]
            data.append(ints)
    return data


def find_joltage(data, size):
    ans = 0

    for row in data:
        tmp_size = size
        batteries = []
        max_battery_idx = -1
        while tmp_size > 0:
            max_battery = -1

            for i in range(max_battery_idx + 1, len(row) - tmp_size + 1):
                if row[i] > max_battery:
                    max_battery = row[i]
                    max_battery_idx = i

            batteries.append(max_battery)

            tmp_size -= 1

        tmp = [str(n) for n in batteries]
        tmp = "".join(tmp)
        tmp = int(tmp)
        # print(f"Found {str(tmp)} joltage in bank.")
        ans += tmp

    return ans


filename = "day03/example"
filename = "day03/input"

data = parse(filename)
# ans = part1(data)

p1 = find_joltage(data, 2)
print("Part 1:", p1)

p2 = find_joltage(data, 12)
print("Part 2:", p2)
