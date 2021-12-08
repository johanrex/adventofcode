

def read_input(filename):
    targets = 0

    input = []
    with(open(filename, "r")) as f:
        for line in f:
            first, second = line.split('|')
            l1 = first.strip().split()
            l2 = second.strip().split()

            targets += len([item for item in l2 if len(item) == 2])
            targets += len([item for item in l2 if len(item) == 4])
            targets += len([item for item in l2 if len(item) == 3])
            targets += len([item for item in l2 if len(item) == 7])


    return targets 

targets = read_input('2021/8_input_example.txt')
print(f'Part 1. Sum: {targets}')



i = 0