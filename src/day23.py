"""Notes
Pseudorandom 

Each buyer's secret number evolves into the next secret number in the sequence via the following process:
- res= secret_number * 64
- res=int(secret_number/32) 
- secret_number * 2048

M= mix(res, secret number) : bitwise XOR (42 mix 15 = 37)
P= prune(M) number % 16777216 : prune(100000000)= 16113920


secret number is the seed

2000 new random numbers

16777216 = 0b1000000000000000000000000

 ((S*64) XOR S) % 16777216

Nice thing: we only start with unsigned numbers.
167... is 2*25, so "modulo it") means to take the first 24 bits
prune = number & 0x 0000000000111111

S*64 = S<<6 (shift of bits)
/ 32 is equal to >>5
* 2048 = <<11
so these are ALL bitwise operation so far.

Is there any repetition?

# PART 2
now, I only have 2098 stuff for 2000 steps, so the final matrix is
2K * 2K, and it is SORT OF manageable. YES I KNOW I could look at repetitions. Should I?


"""
# %%
import numpy as np
from common import INPUT_DIR, get_data, check_test,check_solution
from tqdm import tqdm
import matplotlib.pyplot as plt
def printd(*args):
    #print(*args)
    pass

# %%

def parse(text_data):
    return [line.split("-") for line in text_data.split("\n")]

def build_data(data):
    conn2=data["conn2"]
    pc_names=set()
    for conn in conn2:
        pc_names.add(conn[0])
        pc_names.add(conn[1])
    pc_names=list(pc_names)
    pc_names.sort()

    mat_conn=np.zeros((len(pc_names), len(pc_names)))
    for conn in conn2:
        c1 = pc_names.index(conn[0])
        c2 = pc_names.index(conn[1])
        mat_conn[c1,c2]=mat_conn[c2,c1]=1
    data["pc_names"]=pc_names
    data["mat_conn"]=mat_conn
    plt.figure()
    plt.imshow(mat_conn, aspect="auto")
    
    return data

 

    


def find_3(data):
    mat=data["mat_conn"]
    pc_names=data["pc_names"]
    all3 = []
    t3 = []
    for i, name_i in enumerate(pc_names):
        idxs=np.where(mat[i,:]>0)[0] # all PC connected to pc_name
        idxs=idxs[idxs>i]            # among those higher then pc_name (sorting)
        ni = name_i[0]
        for j in idxs:
            nj = pc_names[j][0]
            idxs=np.where(mat[i]*mat[j]>0)[0]  # all pc_s connected to i and j
            idxs = idxs[idxs>j] # only if k > j > i
            for k in idxs:
                nk=pc_names[k][0]
                to_add=[name_i, pc_names[j], pc_names[k]]
                all3.append(to_add)
                if "t" in [ni, nj, nk]:
                    t3.append(to_add)
    data["all3"]=all3
    data["t3"]= t3
    return data

def solve_quiz1(fn=None, test_data=None, start_with_t=True):
    text_data = get_data(fn, test_data)
    data = {"conn2":parse(text_data)}
    data = build_data(data)
    data=find_3(data)
    if start_with_t:
        return len(data["t3"])

    return len(data["all3"])

def find_psw(mat, check_idx=None, prev_idx=0):
    N = mat.shape[0]
    
    if check_idx is None: # first: check everything
        check_idx=np.ones((N,))
    
    idxs=np.where(check_idx==1)[0] 
    # only for the current stuff
    
    if idxs.size==0: # if I can't go forward, I skip this
        return []
    max_how_many=0 # maximum count
    which_ones=None
    for i in idxs:        
        # let's count what happens forward, only considering:
        # 1. the matrix starting from the index I just found 
        #     e.g., index 10, I'm looking from index 11 on
        # 2. # the connection I need to keep are: those kept so far (check_idxs) times the ones that I'll be exploring of myself mat[i]    
        which_ones_i=[prev_idx+i,]
        if mat[i, i+1:].shape!=check_idx[i+1:].shape:
            pass
        which_ones_i += find_psw(mat[i+1:,i+1:], mat[i, i+1:]*check_idx[i+1:], prev_idx+i+1)
        if len(which_ones_i) > max_how_many:
            which_ones = which_ones_i
            max_how_many=len(which_ones_i)

    return which_ones
    

def find_password(data):   
    idxs=find_psw(data["mat_conn"])
    pc_names= [data["pc_names"][i] for i in idxs]
    pc_names.sort()
    return ",".join(pc_names)

def solve_quiz2(fn=None, test_data=None):
    text_data = get_data(fn, test_data)
    data = {"conn2":parse(text_data)}
    data = build_data(data)
    return find_password(data)




if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day23.txt"

    test_data = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
    all3 = solve_quiz1(test_data=test_data, start_with_t=False)
    check_test(f"\t1.1 comparison", all3, true_result=12)
    t3 =  solve_quiz1(test_data=test_data, start_with_t=True)
    check_test(f"\t1.2 comparison", t3, true_result=7)
        
    
    solution=solve_quiz1(fn=quiz_fn, start_with_t=True)
    check_solution(1, solution, 1062)        
    
    solution=solve_quiz2(fn=quiz_fn)
    check_solution(2, solution, "bz,cs,fx,ms,oz,po,sy,uh,uv,vw,xu,zj,zm")        
    

