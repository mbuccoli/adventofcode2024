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


def fast_blink(array, blink_times):
    new_array=array.copy()
    new_array[new_array==0]=1
    val_log10 = np.floor(np.log10(new_array))
    idxs_log10 = np.mod(val_log10,2)==1
    val_log10 = val_log10[idxs_log10]
    idxs_log10=idxs_log10[idxs_log10]
    div_value = np.power(10, 1+val_log10//2)
    upper_part = new_array[idxs_log10] // div_value 
    lower_part = new_array[idxs_log10] - upper_part*div_value
    for i in idxs_log10[::-1]:
        new_array = np.insert(new_array, np.array([upper_part[i], lower_part[i]]),i)
    
    new_array[even_values] 
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


def solve_quiz1(fn=None, test_data=None, blink_times=25):
    text_data = get_data(fn, test_data)
    array = parse_array(text_data)
    blinked_array = blink(array, blink_times)
    return len(blinked_array)




if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day11.txt"

    test_data = """125 17"""

    result_test1 = solve_quiz1(test_data=test_data, blink_times=6)
    check_test(1, result_test1, true_result=22)
    result_test1 = solve_quiz1(test_data=test_data)
    check_test(1, result_test1, true_result=55312)

    print("Quiz1 result is", solve_quiz1(fn=quiz_fn))
    print("Quiz2 result is", solve_quiz1(fn=quiz_fn, blink_times=75))
