import datetime
import day6


def test_p1():

    lines = """abc

a
b
c

ab
ac

a
a
a
a

b

""".split(
        "\n"
    )

    groups = day6.parse_groups(lines)
    s = day6.p1_sum_groups(groups)
    assert s == 11
    pass


def test_p2():
    lines = """
abc

a
b
c

ab
ac

a
a
a
a

b    
    
""".split(
        "\n"
    )

    groups = day6.parse_groups(lines)
    s = day6.p2_sum_groups(groups)
    assert s == 6


if __name__ == "__main__":
    test_p1()
    test_p2()
    print(datetime.datetime.now())
