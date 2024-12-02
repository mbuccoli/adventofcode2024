from pathlib import Path

INPUT_DIR= Path(__file__).parent.parent / "inputs"

def check_test(quiz_n, result, true_result):
    assert (
        result == true_result
    ), f"Quiz {quiz_n} solution {result} does not match correct solution {true_result}"