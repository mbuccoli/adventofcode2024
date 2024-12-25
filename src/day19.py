# I will start with this day for an attempt to make my way to the leaderboard (a private one)
# So solving MOST recent problems is more likely to give me more points

# now the stripes.
# Patterns
# r, wr, b, g, bwu, rb, gb, br
# Designs
# brwrr
# bggr
# gbbr
# rrbgbr
# ubwu
# bwurrg
# brgr
# bbrgwb

# So, maybe first I can simplify my problem by using a list of symbols (patterns) that are unique.
# E.g., why keeping rb and gb and br if I can use b, r, and g to use them? 
# (this actually means to solve the same problem across substring, not easy!)
# a dummy way is to start with smaller symbols and then compose it to form complex and complex symbols and remove them from patterns
# b, r, g are 1 letter, so I check bb, rr, gg, br, rb, bg, gb, gr, rg, and remove what I find.
# Now I compose any two letter symbols with the 1 letter and see what happens.
# etc.


# Patterns
# r, wr, b, g, bwu, 
# now is much easier! I have 5 symbols! 
# Now, for each design, I'll only consider the patterns that are its substrings. 

# brwrr --> r, wr, b
# bggr --> b,g,r
# gbbr ->  b, g, r
# rrbgbr -> r, b, g
# ubwu -> bwu, 
# bwurrg -> bwu, r, g
# brgr -> b,r,g
# bbrgwb -> b,r, g

# First thing first: in the design, is there any letter that is not covered by a substring? well, yes, let's show it in capital letter
# brwrr --> r, wr, b
# bggr --> b,g,r
# gbbr ->  b, g, r
# rrbgbr -> r, b, g
# Ubwu -> bwu,  --> IMPOSSIBLE
# bwurrg -> bwu, r, g  
# brgr -> b,r,g
# bbrgWb -> b,r, g --> IMPOSSIBLE

# Now, this is how we can solve the example, but possibly not the entire exercize.
# Suppose we have patterns bw wu and design bwu.
# While bw and wu BOTH belong to the design, there is NO WAY I can have them.
# I can exploit, however, the length of the design and the length of the "possible" symbols
# if len(bwu) = 3, I need to find ONLY combinations of 3*1, or 1+2, or 2+1, or 3. I can't use 2+2
# how can I find it?
# well, I can say
# D (len of design)
# P (len of patterns) = [P1, P2, P3, ... P]<D
# to find combinations of D, I start by looking recursively or iteratively combinations of D-P1, D-P2, etc.
# where I can't find it, I remove the sequence all toghether 

# ok, now let's be also smarter, what this stuff looks like? It looks like CODING. 
# Can I code a design with symbols? 

# I can try to divide and conquer by counting for each letter of the design how many patterns apply.
# Let's start with those that appears the least, because THOSE will simplify my problem.
# ok D D D D D D D
#    4 5 3 1 2 4 3
# hey, there is a D that only appears once. let's split and now look for all possible combinations of the substrings.
# (does it look easy?, well, recursively it may work!)

# (what is the brute force? check ALL the possible combinations and remove the design that shows it, until just few nonpossible designs remain)

# %%
import numpy as np
from common import INPUT_DIR, check_solution, check_test, get_data, printd, dontprint


printd=dontprint
from tqdm import tqdm
def parse(text_data):
    patterns, designs = text_data.split("\n\n")
    patterns = patterns.split(", ")
    designs = designs.split("\n")
    return {"patterns": patterns, "designs":designs}

def find_all(string, substring):
    indices=[]
    
    start_str=0
    while start_str<len(string):        
        k=string[start_str:].find(substring)
        if k==-1:
            break
        indices.append(k+start_str)
        start_str+=k+1

    return indices

def is_possible(design, patterns):
    good_patterns=[]
    design_num=np.zeros((len(patterns), len(design)))
    for p, pattern in enumerate(patterns):
        idxs=find_all(design, pattern)
        P=len(pattern)
        if len(idxs)>0:
            good_patterns.append(p)
        for idx in idxs:
            Pend=min(len(design), idx+P)
            design_num[p, idx:Pend]+=1
    if np.any(np.sum(design_num, axis=0)==0):
        return False, None
    good_patterns=np.array(good_patterns)
    design_num=design_num[good_patterns,:]
    good_patterns=[patterns[p] for p in good_patterns]
    return True, good_patterns # non True, but let's try

def find_combination_substr(design,patterns):
    possible_combinations=[]
    found_it=False
    for pattern in patterns:
        if not design.startswith(pattern):
            continue
        if design==pattern:
            found_it=True
        if design.startswith(pattern):
            possible_combinations.append(pattern)
            
    return possible_combinations, found_it

def sort_by_length(array):
    lengths=[len(a) for a in array] 
    
    array=[array[i] for i in np.argsort(lengths)]
    return array


def find_combination(design,patterns):
    possible_combinations, found_it = find_combination_substr(design, patterns)
    if found_it:
        return True
    possible_combinations=sort_by_length(possible_combinations)[::-1]
    for pc in possible_combinations:
        if find_combination(design[len(pc):], patterns):
            return True
    return False

def get_possible_designs(data):
    is_present=[]
    N_present=0
    for design in tqdm(data["designs"]):
        is_possible_design, good_patterns = is_possible(design, data["patterns"])
        if not is_possible_design:
            is_present.append(False)
            continue
        is_present.append(find_combination(design, good_patterns))
        N_present+=int(is_present[-1])
    data["is_present"]=is_present
    data["N_present"]=N_present
    
    return data

def clean_patterns(data):
    data["patterns"]=sort_by_length(data["patterns"])[::-1]
    remove_P=[]
    for p, pattern in enumerate(data["patterns"][:-1]):
        if find_combination(pattern, data["patterns"][p+1:]):
            remove_P.append(p)
            if len(remove_P)==1:
                printd("Removing: ", end="")
            printd(f" {pattern} ", end="")
    printd()
    for p in remove_P[::-1]:
        del data["patterns"][p]
    
    return data


def get_possible_designs2(data):
    designs=data["designs"]
    patterns=data["patterns"]
    hash_info={}
    def rec_func(design, patterns):
        if design in hash_info:
            return hash_info[design]
        if len(design)==0:
            return 1
        ans=0
        for p in patterns:
            
            if design.startswith(p):
                ans += rec_func(design[len(p):], patterns)

        hash_info[design]=ans
        return ans
    num_design=[]
    for design in tqdm(designs):
        num_design.append(rec_func(design, patterns))
    data["num_design"]=num_design
    return data

def solve_quiz1(fn=None, test_data=None, ):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    data = clean_patterns(data)

    data = get_possible_designs(data)
    return data["N_present"]

def solve_quiz2(fn=None, test_data=None, ):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    
    data = get_possible_designs2(data)
    return np.sum(data["num_design"])
# %%
if __name__=="__main__":
    quiz_fn = INPUT_DIR / "day19.txt"
    
    test_data="""r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

    N=solve_quiz1(test_data=test_data)
    check_test(1, N, true_result=6)

    N = solve_quiz1(fn=quiz_fn)
    check_solution(1, N, 300)

    N=solve_quiz2(test_data=test_data)
    check_test(1, N, true_result=16)

    N = solve_quiz2(fn=quiz_fn)
    check_solution(2, N)
