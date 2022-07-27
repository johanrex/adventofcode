MODEL_NR = 13579246899999


def get_initial_state() -> dict:
    return {
        "w": 0,
        "x": 0,
        "y": 0,
        "z": 0,
    }


def evaluate_lines(lines: list[str], model_nr: int):
    state = get_initial_state()
    model_nr_str = str(model_nr)
    inp_offset = 0

    for line in lines:
        tokens = line.split()

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


if __name__ == "__main__":
    with open("d24_input.txt") as f:
        lines = f.readlines()

    model_nr = 99999999999999

    while True:
        # print(f"Evaluating {model_nr}.")

        state = evaluate_lines(lines, model_nr)
        if state["z"] == 1:
            print(f"{model_nr} is largest valid model nr.")
            break

        model_nr -= 1

        if model_nr % 10 == 0:
            model_nr -= 1

        assert model_nr > 0

    pass
# en dict som håller global state.
# sedan utvärdera rad för rad och stoppa in global state.
# stoppa in model_nr också så att man kan populera inp operationen.
# parsa strängen med split eller nåt.
