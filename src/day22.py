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

def printd(*args):
    #print(*args)
    pass
# %%

def go_on(S, N=2000, store_results=False):
    R1=np.zeros_like(S)
    R2=np.zeros_like(S)
    R3=np.zeros_like(S)
    MASK=np.uint64(16777216)-1
    mix_prune= lambda X, Y: np.bitwise_and(np.bitwise_xor(X, Y, out=Y), MASK, out=Y)
    if store_results:
        mat_results = np.zeros((N,S.size), dtype=S.dtype)
    for n in range(N): # three steps at the time
        if store_results:
            mat_results[n]=S
        np.bitwise_left_shift(S, 6, out=R1)
        mix_prune(S, R1)
        np.bitwise_right_shift(R1, 5, out=R2)
        mix_prune(R1, R2)
        np.bitwise_left_shift(R2, 11, out=R3)
        mix_prune(R2, R3)
        S=R3
        if n > N-3:
            printd(R3) 
    if store_results:
        return S, mat_results
    return S

def parse(text_data):
    return np.array([int(line) for line in text_data.split("\n")], dtype=np.uint64)

def solve_quiz1(fn=None, test_data=None, N=2000):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    return go_on(data, N)


def hash_num(x, N=0):
    idxs=x>0
    Y=np.zeros_like(x)
    Y = (9+x) * np.power(10, N)
    Y[idxs] = x[idxs]*np.power(10, N+4)
    return Y


def collect_bananas(seq, unique_seq, price_seq):
    bananas=[]
    for gs in tqdm(unique_seq):
        idxs=np.where(seq==gs)
        banana_gs=0
        for idx in np.unique(idxs[1]): # for each buyer
            idx_t=idxs[0][idxs[1]==idx][0]
            banana_gs+= price_seq[idx_t, idx]
        bananas.append(banana_gs)
    return np.array(bananas)


def solve_quiz2(fn=None, test_data=None, N=2000):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    _, mat = go_on(data, N, store_results=True)
    
    prices=np.mod(mat,10)
    diff = prices[1:] - prices[:-1]
    diff=diff.astype(np.int8)
    hn = hash_num    
    seq = hn(diff[0:-3], 0) + hn(diff[1:-2], 1) + hn(diff[2:-1], 2) + hn(diff[3:], 3)

    unique_seq=np.unique(seq)[::-1]
    price_seq=prices[4:]
    bananas=collect_bananas(seq, unique_seq, price_seq)
    return bananas

if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day22.txt"

    test_data = """123"""
    new_test_data=test_data
    true_results = [15887950,16495136,527345,704524,1553684,12683156,11100544,12249484,7753432,5908254]
    for t,tr in enumerate(true_results):
        est = solve_quiz1(test_data=new_test_data, N=1)
        check_test(f"\t1.0.{t} comparison", est[0], true_result=tr)
        new_test_data=str(est[0])   
    est=solve_quiz1(test_data=test_data, N=len(true_results))
    check_test(f"\t1.0 comparison", est[0], true_result=true_results[-1])
        
    test_data="""1
10
100
2024"""
    true_results=[8685429,4700978,15273692,8667524]
    est = solve_quiz1(test_data=test_data, N=2000)
    for t,tr in enumerate(true_results):
        check_test(f"\t1. comparison", est[t], true_result=tr)
    final_res = np.sum(est)
    check_test(f"\t1. comparison", final_res, true_result=37327623)

    solution=solve_quiz1(fn=quiz_fn, N=2000)
    check_solution(1, np.sum(solution), 17724064040)        
    test_data="""1
2
3
2024"""
    bananas = solve_quiz2(test_data=test_data, N=2000)
    check_test(f"\t2. comparison", np.max(bananas), true_result=23)
    
    bananas = solve_quiz2(fn=quiz_fn, N=2000)
    check_solution(2, np.max(bananas), 1998)        
        

# %%