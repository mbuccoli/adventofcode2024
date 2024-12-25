# %%
import numpy as np
from common import (
    INPUT_DIR,
    check_solution,
    check_test,
    get_data,
    printd,
    dontprint,
    deltas_cross,
    print_mat,
)


printd = dontprint


def parse(text_data):

    lines = text_data.split("\n")
    coordinates = np.zeros((len(lines), 2), dtype=int)
    for l, line in enumerate(lines):
        coordinates[l, :] = np.array([int(l) for l in line.split(",")])

    return {"coordinates": coordinates}


def build_data(data, grid_size, after_ns):
    data["grid_size"] = grid_size + 1
    grid = np.zeros((grid_size + 1, grid_size + 1), dtype=int)
    corrupted_grid = grid.copy()
    c = data["coordinates"]
    corrupted_grid[c[:after_ns, 1], c[:after_ns, 0]] = -1
    data["grid"] = grid
    data["corrupted_grid"] = corrupted_grid
    return data


def valid_pos(pos, grid):
    if np.any(pos < 0) or np.any(pos >= grid.shape[0]):
        return False
    if grid[*pos] == -1:
        return False
    return True


def find_quickest_path(data, max_steps=None):
    grid_steps = data["corrupted_grid"].copy()
    if max_steps is None:
        MAX_STEPS = 2 * grid_steps.size  # all the grid twice
    else:
        MAX_STEPS = max_steps
    grid_steps[grid_steps == 0] = MAX_STEPS
    grid_steps[-1, -1] = 0
    min_steps = 0
    while np.any(grid_steps == MAX_STEPS):  # I still need to check some matrix
        idxs_i, idxs_j = np.where(grid_steps == min_steps)
        if idxs_i.size == 0:
            break  # can't increase anything
        for i, j in zip(idxs_i, idxs_j):
            pos = np.array([i, j])
            for delta in deltas_cross:
                pos_dest = pos + delta
                if valid_pos(
                    pos_dest, grid_steps
                ):  # if it's already been visited, I check the minimum
                    grid_steps[*pos_dest] = min(min_steps + 1, grid_steps[*pos_dest])

        min_steps += 1  # I increase it because I already visited everything
    data["grid_steps"] = grid_steps
    return grid_steps[0, 0]


def solve_quiz1(fn=None, test_data=None, grid_size=70, after_ns=1024):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    data = build_data(data, grid_size, after_ns)
    print_mat(data["corrupted_grid"], {0: ".", -1: "#"})
    quickest_path = find_quickest_path(data)
    return quickest_path


def binary_search_n(data, grid_size, after_ns):
    max_steps = grid_size**3

    Nhigh = len(data["coordinates"])
    Nlow = after_ns
    
    hash_paths = {}

    while Nlow + 1 != Nhigh:
        Nmid = (Nhigh+Nlow)//2

        Qmid=hash_paths[Nmid] = hash_paths.get(
            Nmid, find_quickest_path(build_data(data, grid_size, Nmid), max_steps)
        )

        if Qmid == max_steps:  # solution is too high!
            Nhigh=Nmid 
        else:   # solution is too low
            Nlow=Nmid 
    return Nhigh


def solve_quiz2(fn=None, test_data=None, grid_size=70, after_ns=1024):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    n = binary_search_n(data, grid_size, after_ns)
    C = data["coordinates"][n - 1]
    return f"{C[0]},{C[1]}"

    raise NameError("stop")


# %%
if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day18.txt"

    test_data = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
    quickest_path = solve_quiz1(test_data=test_data, grid_size=6, after_ns=12)
    check_test("1.1", quickest_path, 22)

    quickest_path = solve_quiz1(fn=quiz_fn)
    check_solution(1, quickest_path)

    block_c = solve_quiz2(test_data=test_data, grid_size=6, after_ns=12)
    check_test("1.1", block_c, "6,1")

    block_c = solve_quiz2(fn=quiz_fn)
    check_solution(2, block_c, "30,12")
