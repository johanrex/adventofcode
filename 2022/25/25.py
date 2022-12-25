def snafu_to_int(s):
    val = 0
    for i in range(len(s)):
        curr = s[i]

        if curr == "-":
            curr = -1
        elif curr == "=":
            curr = -2
        else:
            curr = int(curr)
        pos = len(s) - (i + 1)
        val += pow(5, pos) * curr
    return val


def int_to_snafu(n):
    alphabet = ["0", "1", "2", "=", "-"]

    lst = []
    tmp = n
    while tmp > 0:
        m = tmp % 5
        if m >= 3:
            m -= 5

        lst.append(alphabet[m])
        tmp -= m
        tmp //= 5

    return "".join(reversed(lst))


def test():

    mapper = {
        1: "1",
        2: "2",
        3: "1=",
        4: "1-",
        5: "10",
        6: "11",
        7: "12",
        8: "2=",
        9: "2-",
        10: "20",
        15: "1=0",
        20: "1-0",
        2022: "1=11-2",
        12345: "1-0---0",
        314159265: "1121-1110-1=0",
    }

    for k, v in mapper.items():
        assert int_to_snafu(k) == v
        assert k == snafu_to_int(v)


# filename = "25/example"
filename = "25/input"
with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]


# test()

sum = 0
for snafu in lines:
    sum += snafu_to_int(snafu)

print("p1:", int_to_snafu(sum))
