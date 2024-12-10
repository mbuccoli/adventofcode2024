from pathlib import Path
import numpy as np
INPUT_DIR= Path(__file__).parent.parent / "inputs"

def check_test(quiz_n, result, true_result):
    assert (
        result == true_result
    ), f"Quiz {quiz_n} solution {result} does not match correct solution {true_result}"


def parse_mat(text, map_func=lambda x: x):
    mat = [np.array([map_func(char) for char in line]) for line in text.split("\n")]
    return np.array(mat)

def in_mat(idxs, shape):
    return np.all(idxs>=0) and np.all((shape-idxs)>0)

def get_data(fn, test_data):
    if fn is not  None:
        with open(fn, "r") as fp:
            text_data = fp.read()
    elif test_data is not None:
        text_data = test_data
    else:
        raise NameError("Either test_data or fn must be not None")
    return text_data

class DayQuiz:
    def __init__(self, quiz_fn):
        assert quiz_fn.exists(), f"{quiz_fn} does not exist"
        self.quiz_fn = quiz_fn
        self.data = None
        
    def get_data(self, test_data):
        if test_data is not None:
            return self.parse(test_data)
        if self.data is None:
            with open(self.quiz_fn, "r") as fp:
                self.data = self.parse(fp.read())
        return self.data

    def solve_quiz1(self, test_data=None):
        pass
    def solve_quiz2(self, test_data=None):
        pass