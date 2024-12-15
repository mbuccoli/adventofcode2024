# %%
from common import INPUT_DIR, check_test, get_data
import numpy as np
import matplotlib.pyplot as plt
# %%

SHAPE_X=101
SHAPE_Y=103
def parse(text_data):
    data=[]
    for line in text_data.split("\n"):
        robot_data={
            "p": np.array(line.split("p=")[1].split(" ")[0].split(","), dtype=int),
            "v": np.array(line.split("v=")[1].split(","), dtype=int)}
        data.append(robot_data)
    return data

def move_robots(robots, num_steps, shape):
    for robot in robots:
        robot["p"] = robot["p"] + num_steps*robot["v"]
        robot["p"][0] = robot["p"][0]%shape[0]
        robot["p"][1] = robot["p"][1]%shape[1]
        
    return robots

def count_quadrants(robots, shape, return_mat=False):
    mat = np.zeros(shape, dtype=int)
    for robot in robots:
        mat[*robot["p"]]+=1
    I2 = shape[0]//2
    J2 = shape[1]//2
    tl_count = np.sum(mat[:I2,:J2])
    tr_count = np.sum(mat[:I2,J2+1:])
    bl_count = np.sum(mat[I2+1:,:J2])
    br_count = np.sum(mat[I2+1:,J2+1:])
    if not return_mat:
        return [tl_count,tr_count,bl_count,br_count]
    return [tl_count,tr_count,bl_count,br_count], mat

def solve_quiz1(fn=None, test_data=None, shape=(SHAPE_X, SHAPE_Y)):
    text_data = get_data(fn, test_data)
    robots = parse(text_data)
    robots = move_robots(robots, num_steps=100, shape=shape)
    count = count_quadrants(robots, shape)

    return np.prod(count)
            
def print_mat(mat):
    for row in mat:
        row_text=""
        for elem in row:
            if elem == 0:
                row_text+=" "
            else:
                row_text+=str(elem%10)

        print(row_text)       


def solve_quiz2(fn=None, test_data=None, shape=(SHAPE_X, SHAPE_Y)):
    
    text_data = get_data(fn, test_data)
    robots = parse(text_data)
    positions = np.concatenate([robot["p"][None,:] for robot in robots], axis=0)
    velocities = np.concatenate([robot["v"][None,:] for robot in robots], axis=0)
    steps=np.arange(10000)[None, None,:]
    positions_steps = positions[...,None] + steps*velocities[...,None]
    positions_steps[:,0,:]=np.mod(positions_steps[:,0,:], shape[0])        
    positions_steps[:,1,:]=np.mod(positions_steps[:,1,:], shape[1])
    mean=np.mean(positions_steps, axis=0)
    std=np.std(positions_steps, axis=0)
    idx=np.where((std[0]<20) & (std[1]<20))[0]
    robots = move_robots(robots, num_steps=idx, shape=shape)
    _, mat = count_quadrants(robots, shape,return_mat=True)

    print_mat(mat.T)
    plt.figure()
    plt.imshow(mat.T, aspect="auto")
    # DEBUG
    # plt.figure()
    # for i, label in enumerate("XY"):
    #     plt.scatter(steps.flatten(),mean[i], label=f"Mean {label}")
    #     plt.scatter(steps.flatten(),std[i], label=f"std {label}")
    # plt.legend()
    plt.show()    
    return idx      
    

if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day14.txt"

    test_data = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
    
    result_test1 = solve_quiz1(test_data=test_data, shape=(11, 7))
    check_test(1, result_test1, true_result=12)
    
    print("🎄 🎄 🎄 Quiz1 result is", solve_quiz1(fn=quiz_fn))

    print("🎄 🎄 🎄 Quiz2 result is", solve_quiz2(fn=quiz_fn))

# %%
