# %%
from common import INPUT_DIR, check_test, parse_mat, get_data, in_mat
import numpy as np

# %%


def find_trail(mat, val, idx, idxs9, count):
    if not in_mat(idx, mat.shape):
        return
    if mat[*idx] != val:
        return
    mat[*idx] = -1 # this allows the path not to be considered anymore; it was covered by someone else

    if val == 9:
        idx9 = np.argmin(np.sum(np.abs(idxs9 - idx), axis=1))
        count[idx9] = 1
        return
    deltas=np.array([[1,0], [-1,0],[0, 1],[0,-1]])
    for delta in deltas: # moving up, down, left, right to check the next one
        find_trail(mat, val+1, idx+delta, idxs9, count[:])
                    

def find_trails(mat):
    idxs0 = np.array(np.where(mat == 0)).T
    idxs9 = np.array(np.where(mat == 9)).T
    count_trails = np.zeros((idxs0.shape[0], idxs9.shape[0]), dtype=int)
    for i, idx0 in enumerate(idxs0):
        find_trail(mat.copy(), 0, idx0, idxs9, count_trails[i,:])
    return count_trails

def solve_quiz1(fn=None, test_data=None):
    text_data = get_data(fn, test_data)
    mat = parse_mat(text_data, lambda x: int(x))
    count_trails= find_trails(mat)
    return np.sum(np.abs(count_trails))


# def solve_quiz2(fn=None, test_data=None):
#     text_data = get_data(fn, test_data)
#     array, _ = parse(text_data)
#     ext_array = move_array_defrag(array)
#     return compute_checksum(ext_array)


if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day10.txt"

    test_data = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

    result_test1 = solve_quiz1(test_data=test_data)
    check_test(1, result_test1, true_result=36)
    print("Quiz1 result is", solve_quiz1(fn=quiz_fn))
    # result_test2 = solve_quiz2(test_data=test_data)
    # check_test(2, result_test2, true_result=2858)
    # print("Quiz2 result is", solve_quiz2(fn=quiz_fn))
