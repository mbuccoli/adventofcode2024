# https://adventofcode.com/2024/day/7
# %% IMPORT
from typing import Union
from pathlib import Path
from common import INPUT_DIR, check_test, DayQuiz
from graphlib import TopologicalSorter
import numpy as np
from itertools import product

# %%


class Day7Quiz(DayQuiz):
    def __init__(self, quiz_fn):
        super(Day7Quiz, self).__init__(quiz_fn)
        self.data = None # {"equations": {}, "filtered_equations": {}}

    def parse(self, text):
        data = {}
        data["equations"] = []
        for row in text.split("\n"):
            res, vals = row.split(": ")
            data["equations"].append((int(res), [int(val) for val in vals.split(" ")]))
        return data
    def check_res(self, res, partial_res, vals):
        if partial_res > res:  # higher than results, so following won't match
            return 0
        if len(vals) == 1:  # last number, so we can check if the results are good
            return int(res == partial_res + vals[0]) + int(res == partial_res * vals[0])
        check_sum = self.check_res(res, partial_res + vals[0], vals[1:])
        check_prod = self.check_res(res, partial_res * vals[0], vals[1:])
        return check_sum + check_prod
    def check_res_concat(self, res, partial_res, vals):
        if partial_res > res:  # higher than results, so following won't match
            return 0
        if len(vals) == 1:  # last number, so we can check if the results are good
            return int(res == partial_res + vals[0]) + \
                   int(res == partial_res * vals[0]) + \
                   int(res == int(str(partial_res)+str(vals[0])))
        check_sum = self.check_res_concat(res, partial_res + vals[0], vals[1:])
        check_prod = self.check_res_concat(res, partial_res * vals[0], vals[1:])
        check_concat = self.check_res_concat(res, int(str(partial_res)+str(vals[0])), vals[1:])
        
        return check_sum + check_prod + check_concat

    def count_test_values(self, data: dict):
        num = 0
        for res, _, _ in data["filtered_equations"]:
            num += res
        return num

    def filter_equations(self, data: dict, check_func):
        data["filtered_equations"] = []
        data["wrong_equations"]=[]
        for i, (res, vals) in enumerate(data["equations"]):
            
            how_many = check_func(res, partial_res=vals[0], vals=vals[1:])
            if how_many>0:
                data["filtered_equations"].append((res, i, how_many))
            else:
                data["wrong_equations"].append((res, i, how_many))

    def solve_quiz1(self, test_data=None):
        data = self.get_data(test_data)
        self.filter_equations(data, check_func=self.check_res)
        return self.count_test_values(data)

    def solve_quiz2(self, test_data=None):
        data = self.get_data(test_data)
        # first thing: only look at the wrong equations
        self.filter_equations(data, check_func=self.check_res_concat)
        return self.count_test_values(data)


if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day7.txt"
    d7q = Day7Quiz(quiz_fn)

    test_data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

    result_test1 = d7q.solve_quiz1(test_data=test_data)
    check_test(1, result_test1, true_result=3749)
    print("Quiz1 result is", d7q.solve_quiz1())
    result_test2 = d7q.solve_quiz2(test_data=test_data)
    check_test(2, result_test2, true_result=11387)
    print("Quiz2 result is", d7q.solve_quiz2())

# %%
