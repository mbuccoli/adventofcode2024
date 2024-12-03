# https://adventofcode.com/2024/day/3
# %% IMPORT
from typing import Union
from pathlib import Path
from common import INPUT_DIR, check_test
import numpy as np

# %%


class Day3Quiz:
    def __init__(self, quiz_fn):
        assert quiz_fn.exists(), f"{quiz_fn} does not exist"
        self.quiz_fn = quiz_fn
        self.data = None

    def check_num(self, num_str):
        try:
            return int(num_str)
        except:
            return None
    def parse_quiz1(self, text):
        # this is a good thing for regex, however we want to get
        # mul(int,int) with no spaces (is it int? I guess so)

        i=0
        muls=[]
        while i < len(text)-4:
            # check mul(
            if text[i:i+4]!="mul(":
                i+=1
                continue            
            i+=4
            if i>len(text):
                break
            # check number from ( to ,            
            index_comma=text[i:].find(",")
            if index_comma==-1:
                break
            num0 = self.check_num(text[i:i+index_comma])
            if num0 is None:
                i+=1
                continue
            # negative numbers are accepted?
            i+=index_comma
            i+=1
            if i>len(text):
                break
            # check number between , and )
            index_par=text[i:].find(")")
            if index_par==-1:
                break
            num1 = self.check_num(text[i:i+index_par])
            if num1 is None:
                i+=1
                continue
            muls.append([num0, num1])
            i+=index_par+1
            # continue
        return np.array(muls)
    def parse_quiz2(self, text):
        # this is a good thing for regex, however we want to get
        # mul(int,int) with no spaces (is it int? I guess so)

        i=0
        muls=[]
        LEN_DONT=len("don't()")
        while i < len(text)-LEN_DONT:
            if text[i:i+LEN_DONT]=="don't()":
                i+=LEN_DONT+1
                index_do = text[i:].find("do()")
                if index_do==-1:
                    break
                i+=index_do + len("do()")
                continue
            # check mul(
            if text[i:i+4]!="mul(":
                i+=1
                continue            
            i+=4
            if i>len(text):
                break
            # check number from ( to ,            
            index_comma=text[i:].find(",")
            num0 = self.check_num(text[i:i+index_comma])
            if num0 is None:
                i+=1
                continue
            # negative numbers are accepted?
            i+=index_comma
            i+=1
            if i>len(text):
                break
            # check number between , and )
            index_par=text[i:].index(")")
            num1 = self.check_num(text[i:i+index_par])
            if num1 is None:
                i+=1
                continue
            muls.append([num0, num1])
            i+=index_par+1
            # continue
        return np.array(muls)

    def get_data(self, test_data):
        if test_data is not None:
            return test_data
        if self.data is None:
            with open(self.quiz_fn, "r") as fp:
                self.data = fp.read()
        return self.data


    def solve_quiz1(self, test_data=None):
        data = self.parse_quiz1(self.get_data(test_data))
        if data.size==0:
            return 0
        return np.sum(np.prod(data, axis=1))

    def solve_quiz2(self, test_data=None):
        data = self.parse_quiz2(self.get_data(test_data))
        if data.size==0:
            return 0
        return np.sum(np.prod(data, axis=1))



if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day3.txt"
    d3q = Day3Quiz(quiz_fn)
    test_data = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
    
    result_test1=d3q.solve_quiz1(test_data=test_data)
    check_test(1, result_test1, true_result=161)
    print("Quiz1 result is", d3q.solve_quiz1())
    test_data="xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    result_test2=d3q.solve_quiz2(test_data=test_data) 
    check_test(2, result_test2, true_result=48)
    
    print("Quiz2 result is", d3q.solve_quiz2())

# %%
