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

    # def filter_equations(self, data: dict):
    #     data["filtered_equations"] = []
    #     for i, (res, vals) in enumerate(data["equations"]):
    #         # check how many combiantions we can have (one is enough, but let's keep everything)
    #         # WE CAN USE A BINARY
            
    #         how_many = self.check_res(res, partial_res=0, vals=vals)
    #         if how_many>0:
    #             data["filtered_equations"].append((res, i, how_many))

    def count_test_values(self, data: dict):
        num = 0
        for res, _, _ in data["filtered_equations"]:
            num += res
        return num

    def solve_quiz1(self, test_data=None):
        data = self.get_data(test_data)
        self.filter_equations(data, check_func=self.check_res)
        return self.count_test_values(data)

    def filter_equations(self, data: dict, check_func):
        data["filtered_equations"] = []
        data["wrong_equations"]=[]
        for i, (res, vals) in enumerate(data["equations"]):
            
            how_many = check_func(res, partial_res=vals[0], vals=vals[1:])
            if how_many>0:
                data["filtered_equations"].append((res, i, how_many))
            else:
                data["wrong_equations"].append((res, i, how_many))

    def compute_res(self, vals):
        if len(vals)==1:
            return vals
        results=[]
        possible_comb = 2**(len(vals)-1) # if I have 4 values, I have 2*2*2 = 8 possible combinations of operators
        for comb in range(possible_comb):   # let's scroll that
            partial_res=vals[0]    # first I use compute
            for i in range(1,len(vals)):   # than for all the possible values in the following 
                if ((1<<(i-1)) & comb):   # I place a 1 and check if the bit in the i-th position is 0 or 1, and I multiply or sum accordingly
                    partial_res *= vals[i]
                else:  
                    partial_res += vals[i]
            results.append(partial_res)
        return results    

        
    def apply_concatenation(self, data):
        # first, we only want wrong ones

        # Now, is there only ONE concatenation possible or more concatenations are possible?        
        # let's stay safe and assume 1, than I'll check with many

        # For an equation with N vals, N-1 possible positions of operator exist. So I need to make that possible
        
        for res, i, _ in data["wrong_equations"]:
            res2, vals=data["equations"][i]
            assert res==res2, f"Some problem here at index {i}"
            found=False
            for op_j  in range(1,len(vals)):
                # I need to have a list of results for left side and right side and then
                res_left= self.compute_res(vals[:op_j])
                res_right = self.compute_res(vals[op_j:])
                
                for left, right in product(res_left, res_right):
                    if int(str(left)+str(right)) == res:
                        found=True
                        break
                if found:
                    break
            if found:
                data["filtered_equations"].append((res, i, 1))
                        



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
