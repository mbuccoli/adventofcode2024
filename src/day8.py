# https://adventofcode.com/2024/day/7
# %% IMPORT
from typing import Union
from common import INPUT_DIR, check_test, DayQuiz
import numpy as np
from itertools import product

# %%


class Day8Quiz(DayQuiz):
    def __init__(self, quiz_fn):
        super(Day8Quiz, self).__init__(quiz_fn)
        self.data = None # {"equations": {}, "filtered_equations": {}}

    def parse(self, text):
        data = {}
        freqs={}
        f=1
        map_=[]
        for line in text.split("\n"):
            row = []
            for char in line:
                if char==".":
                    row.append(0)
                    continue
                val = freqs.get(char, f)
                row.append(val)
                if val==f:
                    freqs[char]=f
                    f+=1
            map_.append(row)
        data["map"] = np.array(map_)
        data["freqs"] = freqs
        return data
    
    def find_antinodes_freq(self, data, freq):
        N, M = data["map"].shape
        
        def in_map(p):
            return np.all(p>=0) and p[0]<N and p[1]<M
        
        I, J = np.where(data["map"]==freq)
        idxs = np.concatenate([I[:,None], J[:,None]], axis=1)
        for k, p1 in enumerate(idxs[:-1]):
            for p2 in idxs[k+1:]:
                dist = p2-p1
                p_l = p1 - dist
                p_r = p2 + dist
                if in_map(p_l):
                    data["antinodes"][*p_l] += 1                 
                if in_map(p_r):
                    data["antinodes"][*p_r] += 1 
        return data
        
    def find_antinodes(self, data):
        # for each pair of antennas place an antinode, when possible         
        data["antinodes"] = np.zeros_like(data["map"])
        for freq in range(1,len(data["freqs"])+1):
            data = self.find_antinodes_freq(data, freq)

        return data
    def count_antinodes(self, data):
        return np.sum(np.sign(data["antinodes"]))

    def solve_quiz1(self, test_data=None):
        data = self.get_data(test_data)
        data = self.find_antinodes(data)
        return self.count_antinodes(data)

    def solve_quiz2(self, test_data=None):
        data = self.get_data(test_data)
        pass

if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day8.txt"
    d8q = Day8Quiz(quiz_fn)

    test_data = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

    result_test1 = d8q.solve_quiz1(test_data=test_data)
    check_test(1, result_test1, true_result=14)
    print("Quiz1 result is", d8q.solve_quiz1())
    # result_test2 = d8q.solve_quiz2(test_data=test_data)
    # check_test(2, result_test2, true_result=11387)
    # print("Quiz2 result is", d8q.solve_quiz2())

# %%
