# %%
from common import INPUT_DIR, check_test, get_data, parse_mat
from day14 import print_mat
import numpy as np
import matplotlib.pyplot as plt
# %%

ROBOT_SYMBOL= 42
EMPTY_SYMBOL=0
PACK_SYMBOL=3
WALL_SYMBOL=-1
def parse(text_data):
    data={}
    
    text_mat, text_commands=text_data.split("\n\n")
    text_commands=text_commands.replace("\n", "")
    sym_dict = {"#":WALL_SYMBOL, "O": PACK_SYMBOL, "@": ROBOT_SYMBOL, ".":EMPTY_SYMBOL}
    text_commands="\n".join(text_commands)
    cmd_dict = {"^":np.array([-1,0]), "v": np.array([1,0]) , ">": np.array([0,1]), "<":np.array([0,-1])}


    data["mat"] = parse_mat(text_mat, lambda x: sym_dict[x]).astype(int)
    data["commands"] = np.squeeze(parse_mat(text_commands, lambda x: cmd_dict[x]).astype(int))
    return data

def find_robot(data):
    data["robot"] = np.array([i[0] for i in np.where(data["mat"] ==ROBOT_SYMBOL)])
    return data

def execute_move_down(mat, robot):
    i, j=robot
    idxs_empty = np.where(mat[i+1:, j]==EMPTY_SYMBOL)[0]
    idxs_wall = np.where(mat[i+1:, j]==WALL_SYMBOL)[0][0] # first wall

    if idxs_empty.size==0:         # if no zero is found, the command can't be executed
        return mat, robot 
    idx_firstempty = idxs_empty[0]+i+1
    idxs_wall += i+1
    if idxs_wall < idx_firstempty: # there is a wall and the space is behind a wall; I can't move a wall
        return mat, robot
    mat[i+1:idx_firstempty+1,j]=mat[i:idx_firstempty,j]
    mat[i, j]=EMPTY_SYMBOL
    robot[0] += 1
    return mat, robot

def find_pack_tree(mat, robot):
    i, j = robot    
    J={j}
    pairs=[]
    k=i
    found_pack=True
    block=False

    while found_pack:
        found_pack=False
        for j in list(J):
            if np.abs(mat[k+1, j])==PACK_SYMBOL:
                j2 = j + np.sign(mat[k+1,j]) # if its "-3", then I want to add to the right, otherwise I want to add to the right
                J.add(j2)
                if (k+1, j) not in pairs:
                    pairs.append((k+1, j))
                if (k+1, j2) not in pairs:                
                    pairs.append((k+1, j2))

                found_pack=True
            elif mat[k+1, j] == WALL_SYMBOL:
                block = True
        k+=1
    J=list(J)
    J.sort()
    return J, block, pairs

    


def execute_move_down2(mat, robot):
    i, j=robot
    if mat[i+1, j]==EMPTY_SYMBOL: # this is easy
        mat[i+1, j] = ROBOT_SYMBOL
        mat[i, j] = EMPTY_SYMBOL
        robot[0]+=1
        return mat, robot
    if mat[i+1, j]==WALL_SYMBOL: # this was also easy
        return mat, robot
    J, block, idxs = find_pack_tree(mat, robot)
    # now I know that a tree above me spans until J units.
    # however, if block is True, it means that above a package there is a wall, so I cannot raise it 
    if block:
        return mat, robot
    for i_, j_ in idxs[::-1]:
        mat[i_+1, j_] = mat[i_, j_]
        mat[i_, j_] = EMPTY_SYMBOL
    mat[i+1, j] = ROBOT_SYMBOL
    mat[i, j] = EMPTY_SYMBOL
    robot[0]+=1 
    return mat, robot


def up_to_down(mat, robot, back_forth="forth"):
    if back_forth=="forth":
        mat = mat.copy()[::-1]
        robot = robot.copy() 
        robot[0] = mat.shape[0]-robot[0]-1
    elif back_forth=="back":
        mat = mat[::-1]
        robot[0] = mat.shape[0]-robot[0]-1    
    return mat, robot

def right_to_down(mat, robot, back_forth = "forth"):
    if back_forth=="forth":
        mat = mat.copy().T
        robot = robot.copy()[::-1]         
    elif back_forth=="back":
        mat = mat.T
        robot = robot[::-1]     
    return mat, robot


def execute_moves(data):
    for cmd in data["commands"]:
        # print(cmd)
        # print(data["robot"])
        # print_mat(data["mat"])
        # let's manipulate the matrix and then always return the same stuff
        if cmd[0]==-1: # check upwards            
            mat, robot = up_to_down(data["mat"], data["robot"], "forth")
            mat, robot = execute_move_down(mat, robot)
            data["mat"], data["robot"] = up_to_down(mat, robot, "back")            
        elif cmd[0]==1: # check upwards
            data["mat"], data["robot"] = execute_move_down(data["mat"], data["robot"])                    
        elif cmd[1]==-1: # check left
            mat, robot = up_to_down(*right_to_down(data["mat"], data["robot"], "forth"), "forth") 
            mat, robot = execute_move_down(mat, robot)
            data["mat"], data["robot"] = right_to_down(*up_to_down(mat, robot, "back"), "back") 
            
        elif cmd[1]==1: # check right
            mat, robot = right_to_down(data["mat"], data["robot"], "forth") 
            mat, robot = execute_move_down(mat, robot)
            data["mat"], data["robot"] = right_to_down(mat, robot, "back")
        # print_mat(data["mat"])
        # print(data["robot"])    
    return data

def count_gps(data):
    idxs_x, idxs_y = np.where(data["mat"]==PACK_SYMBOL)

    return 100*np.sum(idxs_x) + np.sum(idxs_y)

def expand_data(data):
    N, M=data["mat"].shape
    mat = np.tile(data["mat"].flatten()[:,None],(1,2))
    idxs = mat[:,0]==PACK_SYMBOL
    mat[idxs,1]=-PACK_SYMBOL
    idxs = mat[:,0] == ROBOT_SYMBOL
    mat[idxs,1] = EMPTY_SYMBOL
    data["mat"]=np.reshape(mat, (N, 2*M))
    return data


def solve_quiz1(fn=None, test_data=None):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    data = find_robot(data)        
    data = execute_moves(data)
    return count_gps(data)

sym_dict={EMPTY_SYMBOL:".",WALL_SYMBOL:"#", ROBOT_SYMBOL:"@", PACK_SYMBOL:"[", -PACK_SYMBOL:"]"}
    

def execute_moves2(data):    
    # same as before for left-right, it changes for up-down
    for c, cmd in enumerate(data["commands"]):
        print()
        print(c, cmd)
        print_mat(data["mat"], sym_dict)
        #input("\n")
        if c==21:
            pass
        if cmd[0]==-1: # check upwards            
            mat, robot = up_to_down(data["mat"], data["robot"], "forth")
            mat, robot = execute_move_down2(mat, robot)
            data["mat"], data["robot"] = up_to_down(mat, robot, "back")            
        elif cmd[0]==1: # check downwards
            data["mat"], data["robot"] = execute_move_down2(data["mat"], data["robot"])                    
        elif cmd[1]==-1: # check left
            mat, robot = up_to_down(*right_to_down(data["mat"], data["robot"], "forth"), "forth") 
            mat, robot = execute_move_down(mat, robot)
            data["mat"], data["robot"] = right_to_down(*up_to_down(mat, robot, "back"), "back") 
            
        elif cmd[1]==1: # check right
            mat, robot = right_to_down(data["mat"], data["robot"], "forth") 
            mat, robot = execute_move_down(mat, robot)
            data["mat"], data["robot"] = right_to_down(mat, robot, "back")
    return data

def solve_quiz2(fn=None, test_data=None):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    data = expand_data(data)
    
    data = find_robot(data)        
    data = execute_moves2(data)
    
    return count_gps(data)

if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day15.txt"

    small_test_data = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

    large_test_data = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
    
    small_test_data2="""#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

    result_test_small = solve_quiz1(test_data=small_test_data)
    check_test(1, result_test_small, true_result=2028)
    
    result_test_large = solve_quiz1(test_data=large_test_data)
    check_test(1, result_test_large, true_result=10092)

    print("🎄 🎄 🎄 Quiz1 result is", solve_quiz1(fn=quiz_fn))
    result_test_small2 = solve_quiz2(test_data=small_test_data2)
    check_test(2, result_test_small2, true_result=105+207+306)


    result_test_large = solve_quiz2(test_data=large_test_data)
    check_test(2, result_test_large, true_result=9021)

    print("🎄 🎄 🎄 Quiz2 result is", solve_quiz2(fn=quiz_fn))

