from numpy import true_divide
import pandas as pd

def get_input():

    all_diagnostics = []

    with(open("2021/3_input.txt", "r")) as f:
        for line in f:
    
            lst = list(line.strip())
            all_diagnostics.append(lst)

    header = [h for h in range(12)]

    df = pd.DataFrame(all_diagnostics, columns=header)
    df = df.astype(int)

    return df

df = get_input()

nr_of_columns = len(df.columns)

print('--------------')
print('Part 1')
print('--------------')

gamma = 0
epsilon = 0

for col_num in range(nr_of_columns):

    bit_pos = nr_of_columns - (col_num + 1)    
    bit_to_set = 1 << bit_pos

    s = df[col_num].sum()

    if s == 500:
        raise "real shit"
    elif s > 500:
        gamma += bit_to_set
    else:
        epsilon += bit_to_set

print(f'gamma: {gamma}')
print(f'epsilon: {epsilon}')
print(f'multiplied: {gamma*epsilon}')

print('--------------')
print('Part 2')
print('--------------')

o2_rating = 0
co2_rating = 0

def filter_rows(df, common: bool, col_num: int = 0):
    s = df[col_num].sum()

    if s >= len(df) / 2:
        most_common_value = 1
    else:
        most_common_value = 0

    if common:
        df_filtered = df[df[col_num] == most_common_value]
    else:
        df_filtered = df[df[col_num] != most_common_value]

    if len(df_filtered) == 1:
        lst = df_filtered.values[0].tolist()
        bin_str = ''.join(list(map(str, lst)))
        number = int(bin_str, 2)
        return number
    else:
        col_num += 1        
        return filter_rows(df_filtered, common, col_num)

o2_rating = filter_rows(df, common=True)
co2_rating = filter_rows(df, common=False)

print(f'o2_rating: {o2_rating}')
print(f'co2_rating: {co2_rating}')
print(f'multiplied: {o2_rating*co2_rating}')

