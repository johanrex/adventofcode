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
    
    #pad with one row outside for easy extraction of empty pixels. 
    padded = pad_with_empty(image, 1)
    col += 1
    row += 1

    neighbors = np.concatenate( (
        padded[row-1, col-1:col+2],
        padded[row, col-1:col+2],
        padded[row+1, col-1:col+2]
    ))

    return neighbors

def enhance(input, alg):
    row_count = len(input)
    col_count = len(input[0])

    output = np.copy(input)

    for row in range(row_count):
        for col in range(col_count):
            neighbors = get_neighbors(input, row, col)

            #Convert bits to int. Could proabbly be made more effective. 
            val = int(''.join(map(str, list(neighbors))), 2)

            px = alg[val]
            
            output[row, col] = px

    return output

def print_image(image):
    for row in range(image.shape[0]):
        print(''.join(map(str, list(image[row]))).replace('0', ' ').replace('1', '\u25A0'))


def main():
    #filename = '2021/20_input_example.txt'
    filename = '2021/20_input.txt'
    alg, input = parse_input(filename)

    output = None

    for i in range(2):
        #make bigger
        extended = pad_with_empty(input, 2)

        print('enhance!')
        output = enhance(extended, alg)
        print_image(output)

        print('Sum:', output.sum())
        
        input = output


    # 5682 < x < 5702

main()

i = 0
