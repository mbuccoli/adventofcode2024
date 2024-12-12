# %%
from common import INPUT_DIR, check_test, get_data
import numpy as np

# %%

def parse_array(text_data):
    return [int(val) for val in text_data.split(" ")]

def blink(array, blink_times):
    new_array=[]
    for val in array:
        if val==0:
            new_array.append(1)
        elif (len(str(val))%2) ==0:
            str_val=str(val)
            i=len(str_val)//2
            new_array.extend([int(str_val[:i]),int(str_val[i:])])
        else:
            new_array.append(val*2024)
    if blink_times==1:
        return new_array
    return blink(new_array, blink_times-1)


def solve_hash(array, blink_times):
    hash_howmany={val:1 for val in array}
    hash_whatafter={}
    for _ in range(blink_times):
        new_hash_howmany={}
        for elem, howmany in hash_howmany.items():            
            if elem not in hash_whatafter:
                hash_whatafter[elem]=blink([elem], 1)
            for wa in hash_whatafter[elem]:
                howmany_current = new_hash_howmany.get(wa, 0)
                new_hash_howmany[wa] = howmany_current + howmany
        hash_howmany = new_hash_howmany            
    
    return np.sum([v for _, v in hash_howmany.items()])


def solve_quiz(fn=None, test_data=None, blink_times=25):
    text_data = get_data(fn, test_data)
    array = parse_array(text_data)
    # blinked_array = blink(array, blink_times)
    # return len(blinked_array)
    return solve_hash(array, blink_times)

            
          

if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day11.txt"

    test_data = """125 17"""
    
    result_test1 = solve_quiz(test_data=test_data, blink_times=6)
    check_test(1, result_test1, true_result=22)
    result_test1 = solve_quiz(test_data=test_data)
    check_test(1, result_test1, true_result=55312)
    print("Quiz1 result is", solve_quiz(fn=quiz_fn))


    print("Quiz2 result is", solve_quiz(fn=quiz_fn, blink_times=75))
# %%
 