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
    # result_test2 = solve_quiz2(test_data=test_data)
    # check_test(2, result_test2, true_result=81)
    # print("Quiz2 result is", solve_quiz2(fn=quiz_fn))
