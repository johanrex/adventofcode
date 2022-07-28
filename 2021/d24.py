MODEL_NR = 13579246899999


def get_initial_state() -> dict:
    return {
        "w": 0,
        "x": 0,
        "y": 0,
        "z": 0,
    }


def evaluate_inputs(tokenized_inputs: list[list[str]], model_nr: int):
    state = get_initial_state()
    model_nr_str = str(model_nr)
    inp_offset = 0

    for tokens in tokenized_inputs:

        if len(tokens) == 3:
            arg_2_value = int(tokens[2]) if tokens[2].lstrip("-").isnumeric() else state[tokens[2]]

        if tokens[0] == "inp":
            inp_value = int(model_nr_str[inp_offset])
            inp_offset += 1
            state[tokens[1]] = inp_value
        elif tokens[0] == "mul":
            state[tokens[1]] = state[tokens[1]] * arg_2_value
        elif tokens[0] == "add":
            state[tokens[1]] = state[tokens[1]] + arg_2_value
        elif tokens[0] == "div":
            assert arg_2_value != 0
            state[tokens[1]] = state[tokens[1]] // arg_2_value
        elif tokens[0] == "mod":
            assert state[tokens[1]] >= 0
            assert arg_2_value > 0
            state[tokens[1]] = state[tokens[1]] % arg_2_value
        elif tokens[0] == "eql":
            state[tokens[1]] = 1 if state[tokens[1]] == arg_2_value else 0

    return state


def optimize_and_tokenize_inputs(lines: list[str]):
    tokenized_inputs = []

    for line in lines:
        tokens = line.split()

        # Remove useless input
        if tokens[0] == "div" and tokens[2] == "1":
            continue
        else:
            tokenized_inputs.append(tokens)

    return tokenized_inputs


if __name__ == "__main__":
    with open("d24_input.txt") as f:
        lines = f.readlines()

    tokenized_inputs = optimize_and_tokenize_inputs(lines)
    test_count = 0
    model_nr = 99999999999999

    while model_nr >= 11111111111111:

        if "0" in str(model_nr):
            model_nr -= 1
            continue

        test_count += 1
        if test_count % 10000 == 0:
            print(f"Evaluating {model_nr}.")

        state = evaluate_inputs(tokenized_inputs, model_nr)
        if state["z"] == 1:
            print(f"{model_nr} is largest valid model nr.")
            break

        model_nr -= 1
        assert model_nr > 0

    pass
