from pathlib import Path

INPUT_DIR= Path(__file__).parent.parent / "inputs"

def check_test(quiz_n, result, true_result):
    assert (
        result == true_result
    ), f"Quiz {quiz_n} solution {result} does not match correct solution {true_result}"




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