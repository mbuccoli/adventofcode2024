# %%
import numpy as np
from common import INPUT_DIR, check_solution, check_test, get_data, printd, dontprint, deltas_cross, print_mat


printd=dontprint
def parse(text_data):
    data={}
    lines=text_data.split("\n")
    coordinates = np.zeros((len(lines),2), dtype=int)
    for l, line in enumerate(lines):
        coordinates[l, :] = np.array([int(l) for l in line.split(",")])
    
    return {"coordinates": coordinates}

def build_data(data, grid_size, after_ns):
    data["grid_size"]= grid_size+1
    grid = np.zeros((grid_size+1, grid_size+1), dtype=int)
    corrupted_grid=grid.copy()
    c=data["coordinates"]
    corrupted_grid[c[:after_ns,1],c[:after_ns,0]]=-1
    data["grid"]=grid
    data["corrupted_grid"]=corrupted_grid
    return data
def valid_pos(pos, grid):
    if np.any(pos<0) or np.any(pos>=grid.shape[0]):
        return False
    if grid[*pos]==-1:
        return False
    return True
        

# def find_quickest_path(data):
#     hash_pos={}
#     gs = data["grid_size"]
#     def find_rec(grid, pos, prev_pos=[]):
#         tpos=tuple([int(p) for p in pos])
#         printd(pos)
#         if tpos in hash_pos:
#             printd("  already visited")
#             return hash_pos[tpos]
#         elif np.all(pos==gs-1):
#             printd("  end!")
#             return 0, [tpos,] # we found the corner
#         min_steps=(gs**3)
#         path=[tpos,]
#         min_path = None
#         deltas_cross=np.array([[1,0], [0, 1],[-1,0],[0,-1]])
#         for delta in deltas_cross:
#             pos_dest=pos+delta
#             if not valid_pos(pos_dest, grid):
#                 continue
#             if tuple(pos_dest) in prev_pos:                
#                 continue # skip to avoid looping
#             Nsteps, subpath = find_rec(grid, pos_dest, prev_pos=prev_pos+path)
#             if Nsteps < min_steps:
#                 min_path = subpath
#                 min_steps = Nsteps
#             if min_steps==0: # I was one step from the solution, let's skip everything else
#                 break
#         printd(min_steps, min_path)
#         if min_steps>=gs**3: # dead end from here:
#             hash_pos[tpos]=[1+min_steps, [None,]]
#         else:    
#             hash_pos[tpos]=[1+min_steps, [tpos,]+min_path]
#         return hash_pos[tpos]
    
#     idxs0_i, idxs0_j = np.where(data["corrupted_grid"]==0)
#     idxs0_i= idxs0_i[::-1][1:]
#     idxs0_j= idxs0_j[::-1][1:]
#     for i, j in zip(idxs0_i, idxs0_j):
#         min_steps, min_path = find_rec(data["corrupted_grid"], np.array([i,j])) 
#     min_steps, min_path = find_rec(data["corrupted_grid"], np.array([0,0])) 
#     data["min_steps"]= min_steps
#     data["min_paht"] = min_path
#     print(hash_pos)
#     return min_steps 
        
def find_quickest_path(data):
    grid_steps=data["corrupted_grid"].copy()
    MAX_STEPS=2*grid_steps.size # all the grid twice
    grid_steps[grid_steps==0]=MAX_STEPS
    grid_steps[-1,-1]=0
    min_steps=0
    while np.any(grid_steps==MAX_STEPS): # I still need to check some matrix
        idxs_i, idxs_j = np.where(grid_steps== min_steps)
        if idxs_i.size==0:
            break # can't increase anything
        for i, j in zip(idxs_i, idxs_j):
            pos = np.array([i,j])
            for delta in deltas_cross:
                pos_dest = pos+delta
                if valid_pos(pos_dest, grid_steps): # if it's already been visited, I check the minimum
                    grid_steps[*pos_dest]=min(min_steps+1, grid_steps[*pos_dest])
        
        min_steps+=1 # I increase it because I already visited everything
    data["grid_steps"]=grid_steps
    return grid_steps[0,0]



def solve_quiz1(fn=None, test_data=None, grid_size=70, after_ns=1024):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    data= build_data(data, grid_size, after_ns)
    print_mat(data["corrupted_grid"], {0:".",-1:"#"})
    quickest_path = find_quickest_path(data)
    return quickest_path





# %%
if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day18.txt"

    test_data="""5,4
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