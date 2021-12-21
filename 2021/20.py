import numpy as np

def parse_input(filename):
    alg = None
    image = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if alg is None:
                alg = np.asarray(list(map(int, line.replace('.', '0').replace('#', '1'))))
                continue

            if len(line) == 0:
                continue
            else:
                line = line.replace('.', '0')
                line = line.replace('#', '1')
                image.append(list(map(int, list(line))))

    image = np.asarray(image)

    return alg, image


def pad_with_empty(unpadded_input, pad_nr):
    return np.pad(unpadded_input, pad_nr, mode='constant')


def get_neighbors(image, row, col):
    
    if not (
        1 <= row <= (len(image)-1) and
        1 <= col <= (len(image[0])-1)
        ):
        raise Exception('nah')

    neighbors = np.concatenate( (
        image[row-1, col-1:col+2],
        image[row, col-1:col+2],
        image[row+1, col-1:col+2]
    ))

    return neighbors

def apply_alg(input, alg):
    row_count = len(input)
    col_count = len(input[0])

    output = np.copy(input)

    for row in range(1, row_count-1):
        for col in range(1, col_count-1):
            neighbors = get_neighbors(input, row, col)

            #Convert bits to int. Could probably be done more effective. 
            val = int(''.join(map(str, list(neighbors))), 2)

            px = alg[val]
            
            output[row, col] = px

    return output

def enhance(input, alg, steps):

    #pad 2 lines
    padded = pad_with_empty(input, 2*steps + 2)

    for step in range(steps):
        padded = apply_alg(padded, alg)

    #strip away 1 extra padding
    output = padded[2:-2,2:-2]

    return output


def print_image(image):
    for row in range(image.shape[0]):
        print(''.join(map(str, list(image[row]))).replace('0', ' ').replace('1', chr(9608)))


def main():
    filename = '2021/20_input.txt'
    #filename = '2021/20_input_example.txt'
    alg, input = parse_input(filename)

    n = 2
    output = enhance(input, alg, n)
    print(f'Enhancements:{n} Sum: {output.sum()}')

    n = 50
    output = enhance(input, alg, n)
    print_image(output)
    print(f'Enhancements:{n} Sum: {output.sum()}')

main()

i = 0
