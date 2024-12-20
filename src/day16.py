# %%
from common import INPUT_DIR, check_test, get_data, parse_mat, print_mat
import numpy as np
import matplotlib.pyplot as plt
# %%

EMPTY_SYMBOL=0
START_SYMBOL=100
END_SYMBOL=200
WALL_SYMBOL=-1
sym2int = {"#":WALL_SYMBOL, "S": START_SYMBOL, "E": END_SYMBOL, ".":EMPTY_SYMBOL}
int2sym={v: k for k, v in sym2int.items()}
dir2sym = lambda direction: {-2:"^",2:"v", -1:"<",1:">"}[direction[0]*2+direction[1]]

def parse(text_data):    
    mat = parse_mat(text_data, lambda x: sym2int[x]).astype(int)
    start_idx=np.where(mat==START_SYMBOL)
    end_idx=np.where(mat==END_SYMBOL)
    data={"maze":mat,
    "start_idx" : np.array([si[0] for si in start_idx]),
    "end_idx" : np.array([ei[0] for ei in end_idx])
    }
    return data

def solve_quiz1(fn=None, test_data=None):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    return -1

if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day16.txt"

    test_data_1 = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

    test_data_2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
    for i, (test_data, true_result) in enumerate(zip((test_data_1, test_data_2),(7036, 11048))):
        result_test = solve_quiz1(test_data=test_data)
        check_test(f"1.{i}", result_test, true_result=true_result)
    
    print("🎄 🎄 🎄 Quiz1 result is", solve_quiz1(fn=quiz_fn))
    
