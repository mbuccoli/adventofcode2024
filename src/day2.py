# https://adventofcode.com/2024/day/2
4# %% IMPORT
from typing import Union
from pathlib import Path
from common import INPUT_DIR, check_test
import numpy as np

# %%


class Day2Quiz:
    def __init__(self, quiz_fn):
        assert quiz_fn.exists(), f"{quiz_fn} does not exist"
        self.quiz_fn = quiz_fn
        self.parsed_data = None
        self.data = None

    def parse(self, text):
        reports = text.split("\n")
        for r, rep in enumerate(reports):
            line = np.array([float(rep_j) for rep_j in rep.split(" ")])
            reports[r]=line
        return reports

    def get_data(self, test_data):
        if test_data is not None:
            return self.parse(test_data)
        if self.parsed_data is None:
            with open(self.quiz_fn, "r") as fp:
                self.parsed_data = self.parse(fp.read())
        return self.parsed_data

    def is_safe(self, report):
        min_dist = 1
        max_dist = 3
        levels_diff = report[1:] - report[:-1]
        signs = np.sign(levels_diff)
        if np.unique(signs).size != 1:
            # not increasing or decreasing
            return False
        if np.any(np.abs(levels_diff)< min_dist) :
            return False
        if np.any(np.abs(levels_diff)> max_dist) :
            return False
        return True

    def is_safe_with_dampener(self, report):
        for i in range(report.size):
            if self.is_safe(np.delete(report, i)):
                return True
        return False


    def solve_quiz1(self, test_data=None):
        data = self.get_data(test_data)
        safe_vals = 0
        for report in data:
            safe_vals += self.is_safe(report)
        return safe_vals

    def solve_quiz2(self, test_data=None):
        data = self.get_data(test_data)
        safe_vals = 0
        for report in data:
            is_safe= self.is_safe(report)
            safe_vals += is_safe
            if is_safe:
                continue
            safe_vals+=self.is_safe_with_dampener(report)

        return safe_vals


if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day2.txt"
    d2q = Day2Quiz(quiz_fn)
    test_data = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
    
    result_test1=d2q.solve_quiz1(test_data=test_data)
    check_test(1, result_test1, true_result=2)
    print("Quiz1 result is", d2q.solve_quiz1())

    result_test2=d2q.solve_quiz2(test_data=test_data) 
    check_test(2, result_test2, true_result=4)
    
    print("Quiz2 result is", d2q.solve_quiz2())

# %%
