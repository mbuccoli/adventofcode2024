# %%
from common import INPUT_DIR, check_test, get_data, parse_mat, print_mat, deltas
import numpy as np
from numpy.linalg import norm
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

def solve_maze(data, steps, next_attempt):
    pass    

    # Check the delta at which I can continue
    # if the current delta is included, go on
    #   BUT FIRST put the other deltas in next attempt as index, new delta
    # if the current delta is not included, but another delta is, follow it
    # if there is no other delta, pop the last attempt from the next one
    
    # once solved the maze, compute the score
    
    # follow the other directions  
    
    # if I can, add it to the steps and continue
    # if I can
    

def solve_mazes(data):
    start_delta=np.array([0, 1])
    d = np.argmin(norm(deltas-start_delta[None], axis=1))
    paths=[]
    next_attemps=[]
    start_idx=data["start_idx"]
    end_idx=data["start_idx"]
    
    
        
    

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
    
# %%
# Some notes here

# I want to score the maze, i.e., finding the path with minimum cost.
# in that sense, I can see a maze as a graph where nodes are the point with 
# choice and edges are the path to connect them, related with the cost.

# E.g. if this is the maze, the actual nodes will be marked as @.
###############
#..@....#....E#
#.#.###.#.###.#
#@.@..#.#...#.#
#.###.#####.#.#
#.#.#....@..#.#
#.#.#####.###.#
#..@.@...@..#.#
###.#.#####.#.#
#..@#.....#.#.#
#.#.#.###.#.#.#
#@.@..#..@#.#.#
#.###.#.#.#.#.#
#S..#..@..#...#
###############

# So nodes are points that empty space that are surrounded by 3 or 4 spaces:
#   #.###
#   .@.@.
#   #.#.#
#
# Interesting part here: I can use a filter to understand empty spaces:
#  010
#  151
#  010
#  And check whenever the filtering is 8 (center + 3 spaces) or 9 (center + 4 spaces) 
# I weight the center as 5 so if the center is a wall (0), the filter will be at maximum 4<5
#
# Now, the interesting thing is that I can already identify dead ends, and remove them.
# A dead end is whatever is surrounded by only 1 space. I will mark that as §
# and remove all the path that leads to it, i.e., from the edge to the dead end

###############
#..@§§§§#....E#
#.#.###§#.###.#
#@.@..#§#...#.#
#.###.#####.#.#
#.#§#....@..#.#
#.#§#####.###.#
#..@.@...@..#.#
###.#.#####.#.#
#..@#.....#.#.#
#.#.#.###.#.#.#
#@.@..#..@#.#.#
#.###.#.#.#.#.#
#S§§#..@..#...#
###############

# Now the interesting part is that after I remove dead ends, some nodes are not nodes
# anymore, because they only used to lead to a dead end. Let's clean them as well

###############
#...#####....E#
#.#.#####.###.#
#@.@..###...#.#
#.###.#####.#.#
#.###....@..#.#
#.#######.###.#
#..@.@...@..#.#
###.#.#####.#.#
#..@#.....#.#.#
#.#.#.###.#.#.#
#@.@..#..@#.#.#
#.###.#.#.#.#.#
#S###..@..#...#
###############

# Now, the problem is: how to score an edge? the edge depends on the previous direction.
# for example, the edge marked with |

#..@.@
###|#.
#.>@#.
#.#^#.
#@.@

# costs 1002 points is coming from ">" and it costs 2 if coming from "^"
# so FOR NOW let's just give it a score of 2. 
# Now I should be able to have a graph as a matrix:
#     S @1 @2 @3 .......   E
#   S 0 3  5  0            0
#  @1 3 0  2
#  @2 2 ....
#  ...
#   E
# Now, how can I find the least path?
# I'll start with S and attempt to reach all the other nodes, summing it with the score
# e.g. (I putA1 for @1 etc.)

#..C#.....#.#.#
#.#.#.###.#.#.#
#A.B..#..@#.#.#
#.###.#.#.#.#.#
#S###..D..#...#
###############

# S->A is 1002 points, and I can't reach anywhere else. So what can I reach from A?
# from A I can reach B and C. 
# Reaching B from S is another 1002; while reaching C is another 1004 score.
# So S->A-> B = 2004 and S->A->C = 2006
# My hash is building: {
# A = [((S,A),1002)],
# B = [((S,A,B),2004)],
# C = [((S,A,C), 2006)]   
# From B, I can reach C. or D!
# so I'll go and see  that B, i.e., S A B C, cost me + 1002
# therefore it is S A B C = 3006, which is more than the actual solution to reach C, so I disregard it
# then I can go on, keep finding position I can reach with the new
# A = SA 1002
# B = SAB 2004
# C = SAC 2006
# D = SABD 4010
# until I will find E (hopefully I won't use letter at this point)
# not only I have found E, but I will find which nodes that allow me to reach E and which allows me to find it with the minimum score

