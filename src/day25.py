"""Notes

"""
# %%
import numpy as np
from common import INPUT_DIR, get_data, check_test,check_solution, parse_mat
from tqdm import tqdm
import matplotlib.pyplot as plt
def printd(*args):
    #print(*args)
    pass

# %%



def parse(text_data):
    locks_keys = text_data.split("\n\n")
    map_func = lambda x: 1 if x=="#" else 0
    lk_mats=[]
    lock_mats=[]
    key_mats=[]
    for lock_key in locks_keys:
        lk_mat = parse_mat(lock_key, map_func).astype(int)
        lk_mats.append(lk_mat)
        if lk_mat[0,0] == 0:
            key_mats.append(lk_mat)
        else:
            lock_mats.append(lk_mat)

    
    
    return {"lock_mats":lock_mats, "key_mats":key_mats}    

def check_fit(data):
    
    compute_signature=lambda mat: np.sum(mat, axis=0)    
    lock_signs=[compute_signature(lm) for lm in data["lock_mats"]]
    key_signs=[compute_signature(lm) for lm in data["key_mats"]]

    combination = np.zeros((len(lock_signs), len(key_signs)), dtype=int)
    M = data["lock_mats"][0].shape[0]    
    for l, lock_sign in enumerate(lock_signs):
        for k, key_sign in enumerate(key_signs):
            combination[l,k] = int(np.all(lock_sign+key_sign<=M))
    
    data["combination"]=combination
    data["key_sign"]=key_sign
    data["lock_sign"]=lock_sign
    return data


def solve_quiz1(fn=None, test_data=None):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    data = check_fit(data)
    
    return np.sum(data["combination"])



if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day25.txt"

    test_data = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""
    sol = solve_quiz1(test_data=test_data)
    check_test(f"\t1.1 comparison", sol, true_result=3)

    sol = solve_quiz1(fn=quiz_fn)
    check_solution(1, sol)
