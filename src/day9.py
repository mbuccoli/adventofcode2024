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
    return np.array(array).astype(int), np.concatenate(extend_array).astype(int)
         
def move_array(extended_array):
    while True:    
        first_empty = np.where(extended_array==-1)[0][0]
        last_val = np.where(extended_array!=-1)[0][-1]
        if first_empty>last_val:
        # all the free space is at the end
            return extended_array
        
        extended_array[first_empty] = extended_array[last_val]
        extended_array[last_val] = -1

def move_array_defrag(array):
    array_copy=array.copy()
    # idx_ext_array=np.zeros_like(array_copy[:,0])
    # idx_ext_array[1:]=np.cumsum(array_copy)[1:]
    for id_file, blocks_file in array[::-1]:
        if id_file==-1: # this is a space
            continue
        idx_file = np.where(array_copy[:,0]==id_file)[0][0]
        idx_space = np.where((array_copy[:,0]==-1) & (array_copy[:,1]>=blocks_file))[0]
        if idx_space.size==0:
            continue
        idx_space=idx_space[0]
        if idx_space > idx_file:
            continue
        array_copy[idx_space,1] -= blocks_file
        if array_copy[idx_space,1] == 0:
            array_copy[idx_space] = array_copy[idx_file]
        else:
            array_copy = np.insert(array_copy, idx_space, array_copy[idx_file], axis=0)
            idx_file+=1
        array_copy[idx_file,0] = -1

    ext_array = [val*np.ones(count) for val, count in array_copy]
    return np.concatenate(ext_array).astype(int)
    

def compute_checksum(extended_array):
    # first_empty = np.where(extended_array==-1)[0][0]
    # checksum = np.sum(np.arange(first_empty)*extended_array[:first_empty])
    checksum = np.sum(np.arange(extended_array.size)*np.clip(extended_array, 0, None))
    return checksum

def get_data(fn, test_data):
    if fn is not  None:
        with open(fn, "r") as fp:
            text_data = fp.read()
    elif test_data is not None:
        text_data = test_data
    else:
        raise NameError("Either test_data or fn must be not None")
    return text_data
def solve_quiz1(fn=None, test_data=None):
    text_data = get_data(fn, test_data)
    _, array = parse(text_data)
    array = move_array(array)
    return compute_checksum(array)

def solve_quiz2(fn=None, test_data=None):
    text_data = get_data(fn, test_data)
    array, _ = parse(text_data)
    ext_array = move_array_defrag(array)
    return compute_checksum(ext_array)


if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day9.txt"    

    test_data = """2333133121414131402"""

    result_test1 = solve_quiz1(test_data=test_data)
    check_test(1, result_test1, true_result=1928)
    print("Quiz1 result is", solve_quiz1(fn=quiz_fn))
    result_test2 = solve_quiz2(test_data=test_data)
    check_test(2, result_test2, true_result=2858)
    print("Quiz2 result is", solve_quiz2(fn=quiz_fn))

