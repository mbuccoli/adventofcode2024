# %%
from common import INPUT_DIR, check_test, get_data, parse_mat, print_mat
from common import deltas_cross as deltas
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from day16 import EMPTY_SYMBOL, START_SYMBOL, END_SYMBOL, WALL_SYMBOL, sym2int, int2sym, parse
# %%


def find_path(data):
    idxs=[data["start_idx"],data["start_idx"]]
    idx=idxs[-1]        
    while norm(idx-data["end_idx"])!=0:
        for delta in deltas:
            idx_dest=idx+delta

            if data["maze"][*idx_dest]==WALL_SYMBOL:        
                continue
            elif norm(idx_dest-idxs[-2])==0:
                continue
            idxs.append(idx_dest)
            idx=idx_dest
            break
        
    data["path"]=np.array(idxs[1:])
    return data

def find_cheats(data, max_ps):
    deltas_cheat =deltas*max_ps # I can move TWO positions
    possible_cheats=[]    
    for i, idx_i in enumerate(data["path"][:-2]):
        idxs_idxs_j = np.where(norm(idx_i[None]-data["path"][i+2:], axis=1)<=max_ps)[0]
        for j in idxs_idxs_j:
            idx_j = data["path"][i+2+j]             
            for delta, delta_cheat in zip(deltas,deltas_cheat):
                if norm(idx_i+delta_cheat - idx_j) == 0 and data["maze"][*(idx_i+delta)]==WALL_SYMBOL:
                    possible_cheats.append(j)
    data["cheats"] = np.array(possible_cheats)
    return data                    




def solve_quiz1(fn=None, test_data=None):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    data = find_path(data)
    data = find_cheats(data,2)
    print(data["cheats"])
    return data["cheats"]

if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day20.txt"

    test_data = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

    cheats = solve_quiz1(test_data=test_data)
    true_cheats= [ [14, 2], [14, 4], [2, 6], [4, 8], [2, 10], [3, 12], [1, 20], [1, 36], [1, 38], [1, 40], [1, 64]]
    result_ps, result_count = np.unique(cheats, return_counts=True)
    print(result_ps, result_count)
    check_test(f"1. Comparing lengths", len(result_ps), true_result=len(true_cheats))    
    for i in range(len(result_ps)):
        picoseconds, count = result_ps[i], result_count[i]
        true_count, true_ps = true_cheats[i] 
        check_test(f"\t1.{i} Comparing ps", picoseconds, true_result=true_ps)
        check_test(f"\t1.{i} Comparing count", count, true_result=true_count)

    
    print("🎄 🎄 🎄 Quiz1 result is", np.sum(solve_quiz1(fn=quiz_fn)>=100))
    
