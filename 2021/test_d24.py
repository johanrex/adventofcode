from d24 import evaluate_lines, MODEL_NR


def prepare_lines(multiline_str: str):

    lines = multiline_str.splitlines()
    lines = [line.strip() for line in lines if line.strip() != ""]

    return lines


def test_evaluate_lines_1():
    lines = prepare_lines(
        """
    inp x
    mul x -1
    """
    )
    state = evaluate_lines(lines, MODEL_NR)

    assert state == {"w": 0, "x": -1, "y": 0, "z": 0}


def test_evaluate_lines_2():
    lines = prepare_lines(
        """
    inp z
    inp x
    mul z 3
    eql z x
    """
    )
    state = evaluate_lines(lines, MODEL_NR)

    assert state == {"w": 0, "x": 3, "y": 0, "z": 1}


def test_evaluate_lines_3():
    lines = prepare_lines(
        """
    inp w
    add z w
    mod z 2
    div w 2
    add y w
    mod y 2
    div w 2
    add x w
    mod x 2
    div w 2
    mod w 2
    """
    )
    state = evaluate_lines(lines, 9)

    assert state == {"w": 1, "x": 0, "y": 0, "z": 1}


# test_evaluate_lines_1()
# test_evaluate_lines_2()
# test_evaluate_lines_3()
