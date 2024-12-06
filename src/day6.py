# https://adventofcode.com/2024/day/4
# %% IMPORT
from typing import Union
from pathlib import Path
from common import INPUT_DIR, check_test, DayQuiz
from graphlib import TopologicalSorter
import numpy as np

# %%


class Day6Quiz(DayQuiz):
    def __init__(self, quiz_fn):
        super(Day6Quiz, self).__init__(quiz_fn)
        self.guard_move=[(0,1), # going right
                             (1,0), # going down
                             (0, -1), #  going left
                            (-1, 0)] # going up
        self.guard_looks={"v":1, ">":0, "^": 3, "<": 2}

    def parse(self, text):
        # parse from text to map
        
        # map is a numpy array filled with 0s where nothing append, obstacle is -1 and path is 1 
        # let's also look for directions and return as an index guard with an index of position
        chars_to_num={".":0, "#":-1}
        chars_to_num.update({v: 1 for v in self.guard_looks})
        guard_pos=[]
        guard_look=""
        map_=[]
        for l, line in enumerate(text.split("\n")):
            row=[]
            for c, char in enumerate(line):
                row.append(chars_to_num[char])
                if char in self.guard_looks:
                    guard_look=self.guard_looks[char]
                    guard_pos=[l, c]
            map_.append(row)
        return {"map":np.array(map_), "guard_look":guard_look, "guard_pos": np.array(guard_pos)}
    
    def walk(self, data):
        # make a step, turn it into one, go on
        R, C = data["map"].shape
        start_pos = data["guard_pos"]
        # compute next pos
        next_pos= start_pos+self.guard_move[data["guard_look"]]

        # if next pos is outside the array, exit
        if np.any(next_pos<0) or next_pos[0]==R or next_pos[1]==C:
            return False

        # if next pos is a block, change direction
        if data["map"][*next_pos]==-1:
            data["guard_look"] = (data["guard_look"] +1)%4
            return True
        # else make a step and return
        data["map"][*next_pos]=1
        data["guard_pos"]=next_pos
        return True

    def compute_number(self, data):
        map_changed= data["map"]
        map_changed[map_changed==-1]=0
        return np.sum(map_changed)


    def solve_quiz1(self, test_data=None):
        data = self.get_data(test_data)
        while self.walk(data):
            pass
        
        return self.compute_number(data)
    
    # def solve_quiz2(self, test_data=None):
    #     rules, updates = self.get_data(test_data)
    #     rules, updates = self.refine_data(rules, updates)
    #     _, wrong_updates = self.filter_updates(rules, updates)
    #     fixed_updates = self.fix_updates(rules, wrong_updates)
    #     return self.sum_middle_number(fixed_updates)


if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day6.txt"
    d6q = Day6Quiz(quiz_fn)

    test_data="""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
    
    
    result_test1=d6q.solve_quiz1(test_data=test_data)
    check_test(1, result_test1, true_result=41)
    print("Quiz1 result is", d6q.solve_quiz1())
    # result_test2=d5q.solve_quiz2(test_data=test_data) 
    # check_test(2, result_test2, true_result=123)    
    # print("Quiz2 result is", d5q.solve_quiz2())

# %%