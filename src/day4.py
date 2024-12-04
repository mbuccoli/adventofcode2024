# https://adventofcode.com/2024/day/3
# %% IMPORT
from typing import Union
from pathlib import Path
from common import INPUT_DIR, check_test
import numpy as np

# %%


class Day4Quiz:
    def __init__(self, quiz_fn):
        assert quiz_fn.exists(), f"{quiz_fn} does not exist"
        self.quiz_fn = quiz_fn
        self.data = None

    def parse(self, text):
        # from string to matrix
        mat = [np.array([char for char in line]) for line in text.split("\n")]
        return np.array(mat)
    def r2s(self, row):
        #row2string
        return "".join(row)
    def get_data(self, test_data):
        if test_data is not None:
            return self.parse(test_data)
        if self.data is None:
            with open(self.quiz_fn, "r") as fp:
                self.data = self.parse(fp.read())
        return self.data
    def get_diag(self, data):
        rows=[]
        col_idxs = np.arange(data.shape[1])            
        row_idxs=np.arange(data.shape[0])        
        for i in range(data.shape[0]): # loop diagonally on rows
            row_idxs_i = row_idxs[i:]
            minN=min(row_idxs_i.size, col_idxs.size)
            row_idxs_i=row_idxs_i[:minN]
            col_idxs_i=col_idxs[:minN]
            row = data[row_idxs_i, col_idxs_i]
            rows.extend([self.r2s(row), self.r2s(row[::-1])])
        for j in range(1,data.shape[1]): # loop diagonally on cols
            col_idxs_j = col_idxs[j:]
            minN=min(row_idxs.size, col_idxs_j.size)
            row_idxs_j=row_idxs[:minN]
            col_idxs_j=col_idxs_j[:minN]
            row = data[row_idxs_j, col_idxs_j]
            rows.extend([self.r2s(row), self.r2s(row[::-1])])
        return rows
    def get_rows(self, data):
        # given the matrix, return all the way it can be read (vert, hor, diag)
        rows = [self.r2s(row) for row in data] # rows
        rows.extend([self.r2s(row[::-1]) for row in data]) # rows upside down
        rows.extend([self.r2s(row) for row in data.T]) # cols
        rows.extend([self.r2s(row[::-1]) for row in data.T]) # cols upside down
        rows.extend(self.get_diag(data))
        rows.extend(self.get_diag(np.rot90(data)))
        return rows            
    def find_xmas_row(self, row):
        i = row.find("XMAS")
        if i==-1:
            return 0
        return 1+self.find_xmas_row(row[i+1:])
         
    def find_xmas(self, rows):
        # return number of xmas in rows, possibly recursively/iteratively?
        total_num=0
        for row in rows:
            total_num+=self.find_xmas_row(row)
        return total_num
    
    def is_mas(self, val1, val2):
        good_set=["MS", "SM"]
        return int(val1 in good_set and val2 in good_set)
        
    def find_plus(self, data, i, j):
        val_up=data[i-1, j]
        val_down=data[i+1, j]
        val_left=data[i, j-1]        
        val_right=data[i, j+1]
        return self.is_mas(val_up+val_down, val_left+val_right)
        
    def find_cross(self, data, i, j):
        val_ul=data[i-1, j-1]
        val_dr=data[i+1, j+1]
        val_ur=data[i-1, j+1]        
        val_dl=data[i+1, j-1]
        return self.is_mas(val_ul+val_dr, val_ur+val_dl)
    
    def find_x_mas(self, data):
        # Now, this is a little bit more complex, but just a little bit. What I would do if I was a human?
        # 
        # 1. find all As
        
        As_idxs_i, As_idxs_j = np.where(data=="A")

        # 2. refine removing all the As on the edge
        N, M= data.shape
        def clean_idxs(idxs_i, idxs_j, val_i=-1, val_j=-1):
            good_i=idxs_i!=val_i
            idxs_i=idxs_i[good_i]
            idxs_j=idxs_j[good_i]
            good_j=idxs_j!=val_j
            idxs_i=idxs_i[good_j]
            idxs_j=idxs_j[good_j]
            return idxs_i, idxs_j
        
        As_idxs_i, As_idxs_j = clean_idxs(As_idxs_i, As_idxs_j, 0, 0)
        As_idxs_i, As_idxs_j = clean_idxs(As_idxs_i, As_idxs_j, N-1, M-1)
 
        # 3. explore for each cross dimension (horizontally-vertically or diagonally) if we can find an M and a S
        num = 0
        for i, j in zip(As_idxs_i, As_idxs_j):
          #  num+=self.find_plus(data, i, j)   # OOPS, I believed plus'es counted as crosses
            num+=self.find_cross(data, i, j)
        return num

    def solve_quiz1(self, test_data=None):
        data = self.get_data(test_data)
        rows = self.get_rows(data)
        number= self.find_xmas(rows)

        return number

    def solve_quiz2(self, test_data=None):
        data = self.get_data(test_data)
        number= self.find_x_mas(data)
        return number
    


if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day4.txt"
    d4q = Day4Quiz(quiz_fn)
    test_data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

#     test_data="""123456
# abcdef
# ghijkl"""
    
    
#    test_data="""123456
#                 abcdef
#                 ghijkl"""
    
    result_test1=d4q.solve_quiz1(test_data=test_data)
    check_test(1, result_test1, true_result=18)
    print("Quiz1 result is", d4q.solve_quiz1())
    result_test2=d4q.solve_quiz2(test_data=test_data) 
    check_test(2, result_test2, true_result=9)    
    print("Quiz2 result is", d4q.solve_quiz2())

# %%
