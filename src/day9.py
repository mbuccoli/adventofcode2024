# %%
from common import INPUT_DIR, check_test
import numpy as np
# %%
def parse(text):
    array = []
    extend_array = []
    id_=0
    for c in range(0,len(text)-1,2):
        array.append((id_, int(text[c])))
        array.append((-1, int(text[c+1])))
        extend_array.append(id_*np.ones(int(text[c])))
        extend_array.append(-1*np.ones(int(text[c+1])))
        id_+=1
    if len(text) % 2 == 1:
        array.append((id_, int(text[-1])))
        extend_array.append(id_*np.ones(int(text[-1])))
    return np.array(array), np.concatenate(extend_array)
         
def move_array(extended_array):
    while True:    
        first_empty = np.where(extended_array==-1)[0][0]
        last_val = np.where(extended_array!=-1)[0][-1]
        if first_empty>last_val:
        # all the free space is at the end
            return extended_array
        
        extended_array[first_empty] = extended_array[last_val]
        extended_array[last_val] = -1

def compute_checksum(extended_array):
    first_empty = np.where(extended_array==-1)[0][0]
    checksum = np.sum(np.arange(first_empty)*extended_array[:first_empty])
    return checksum

def solve_quiz1(fn=None, test_data=None):
    if fn is not  None:
        with open(fn, "r") as fp:
            text_data = fp.read()
    elif test_data is not None:
        text_data = test_data
    else:
        raise NameError("Either test_data or fn must be not None")

    _, array = parse(text_data)
    array = move_array(array)
    return compute_checksum(array)


if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day9.txt"    

    test_data = """2333133121414131402"""

    result_test1 = solve_quiz1(test_data=test_data)
    check_test(1, result_test1, true_result=1928)
    print("Quiz1 result is", solve_quiz1(fn=quiz_fn))
    # result_test2 = d8q.solve_quiz2(test_data=test_data)
    # check_test(2, result_test2, true_result=34)
    # print("Quiz2 result is", d8q.solve_quiz2())

