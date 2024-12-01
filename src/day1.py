# https://adventofcode.com/2024/day/1
# %% IMPORT 
from typing import Union
from pathlib import Path
from common import INPUT_DIR
import numpy as np

# %% UTILITY FUNCTIONS

def fromstring(text:str)->np.array:
    """Attempt to redefine fromstring for easier access

    Parameters
    ----------
    text : str
        text to parse

    Returns
    -------
    np.array
        parsed text
    """
    array_list=[]
    for line in text.split("\n"):
        if line=="":
            return
        numbers=line.split(" ")
        array_list.append((int(numbers[0]),int(numbers[-1])))        

    return np.array(array_list)

def parse_file(text: Union[str, Path], open_file:bool=False)->np.array :
    """Parse quiz files

    Parameters
    ----------
    text : Union[str, path]  
        text to parse, if open_file is True, filename to open to get the text
    open_file : bool, optional
        whether the text is the filenaname with the quiz or the string to be parsed, by default False

    Returns
    -------
    np.array
        an array with different lists on columns
    """
    if open_file:
        fn = Path(text)
        assert fn.exists(), f"{fn} does not exist"
        with open(fn, "r") as fp:
            text= fp.read()
    return fromstring(text)

def sort(lists:np.ndarray)->np.ndarray:
    """Return lists sorted by rows

    Parameters
    ----------
    lists : np.ndarray
        input lists

    Returns
    -------
    np.ndarray
        sorted lists
    """
    sorted_lists = lists.copy()
    return np.sort(sorted_lists, axis=0)

def find_sum_min_dist(lists:np.ndarray)->int:
    """Return the sum of the distances between two lists

    Parameters
    ----------
    lists : np.ndarray
        the lists, assumes that are sorted

    Returns
    -------
    int
        sum of the distances
    """
    return np.sum(np.abs(lists[:,1]-lists[:,0]))

def compute_similarity_score(lists:np.ndarray)-> int:
    """Brute force similarity score as explained by the quiz

    Parameters
    ----------
    lists : np.ndarray
        the lists

    Returns
    -------
    int
        similarity score
    """
    uniques, counts=np.unique(lists[:,0], return_counts=True)
    similarity_score=0
    for num, count in zip(uniques, counts):
        similarity_score+=count * num * np.count_nonzero(lists[:,1]==num)
    return similarity_score



# %%
TEST_QUIZ="""3   4
4   3
2   5
1   3
3   9
3   3"""

FILE_QUIZ = INPUT_DIR/"day1.txt"

# %%
def main_quiz1():
    lists = parse_file(FILE_QUIZ, True)
    sorted_lists = sort(lists)
    result = find_sum_min_dist(sorted_lists)
    return result

def test_quiz1():    
    lists = parse_file(TEST_QUIZ, False)
    sorted_lists = sort(lists)
    result = find_sum_min_dist(sorted_lists)
    assert result==11, "Result for quiz1 is wrong, check your code"

def main_quiz1():
    lists = parse_file(FILE_QUIZ, True)
    sorted_lists = sort(lists)
    result = find_sum_min_dist(sorted_lists)
    return result

def test_quiz2():    
    lists = parse_file(TEST_QUIZ, False)
    sorted_lists = sort(lists)
    result = compute_similarity_score(sorted_lists)
    assert result==31, "Result for quiz2 is wrong, check your code"

def main_quiz2():
    lists = parse_file(FILE_QUIZ, True)
    sorted_lists = sort(lists)
    result = compute_similarity_score(sorted_lists)
    return result


if __name__=="__main__":
    test_quiz1()
    print("Result for quiz 1 is", main_quiz1())
    test_quiz2()
    print("Result for quiz 2 is", main_quiz2())
