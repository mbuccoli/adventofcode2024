# %%
from common import INPUT_DIR, check_test, get_data, parse_mat, print_mat
from common import deltas_cross as deltas
import numpy as np
from numpy.linalg import norm


# %%

def parse(text_data):
    codes=[]
    codes_int=[]
    codes_str=[]
    for text_code in text_data.split("\n"):
        codes.append([int(i) for i in text_code[:-1]])
        codes_int.append(int(text_code[:-1]))
        codes_str.append(text_code)
    data={"codes":codes, "codes_int":codes_int,"codes_str":codes_str}
    return data


def diff2seq(diff, what_first=-1):
    # if what_first=-1: you decide
    # else: 0: first x; 1= first y
    if what_first==-1:
        return diff2seq(diff, int(diff[1]<=0)) # turn left before going up/down, IF POSSIBLE
    move_x={-1:"^", 1:"v", 0:"."}
    move_y={-1:"<", 1:">", 0:"."}
    str_updown = move_x[np.sign(diff[0])]*np.abs(diff[0])
    str_leftright = move_y[np.sign(diff[1])]*np.abs(diff[1])
    if what_first==0:
        return  str_updown + str_leftright 
    if what_first==1:
        return  str_leftright + str_updown 
    raise NameError("PROBLEM")
 

class RobotDirNumericKeypad:
    def __init__(self):
        self.mat_code=np.array([[7,8,9],[4,5,6],[1,2,3],[-1,0,10]])
        self.symbols=np.arange(11)
        self.min_paths=[["" for _ in self.symbols] for _ in self.symbols]
        
  
        for s, start_sym  in enumerate(self.symbols):
            for e, end_sym in  enumerate(self.symbols):
                if e<=s:
                    continue
                pos_s=np.array(np.where(self.mat_code==start_sym))
                pos_e=np.array(np.where(self.mat_code==end_sym))
                diff = np.squeeze(pos_e-pos_s)
                if start_sym==0 and end_sym in [1,4,7]: # If I start from 0, FIRST I go up, then I go left/right
                    self.min_paths[s][e] = diff2seq(diff, 0)
                    self.min_paths[e][s] = diff2seq(-diff, 1)
                elif end_sym==10 and start_sym in [1,4,7]: # If I end in 10, first I go left and then I go down
                    self.min_paths[s][e] = diff2seq(diff, 1)
                    self.min_paths[e][s] = diff2seq(-diff, 0)
                else:         
                    self.min_paths[s][e] = diff2seq(diff, -1)
                    self.min_paths[e][s] = diff2seq(-diff, -1)
                    
        
    def type_code(self, code):
        code_seq = [10,]+code+[10,] # from activation to code to activation
        seq=""
        for i in range(len(code_seq)-1):
            seq+=self.min_paths[code_seq[i]][code_seq[i+1]]+"A" # I move from X to Y and then activate
        return seq
    def type(self, seq):
        new_seq=""
        subseqs = seq.split("A")[:-1]
        idx=np.squeeze(np.where(self.mat_code==10))
        sym_dict={"v":np.array(([1,0])),
                  "^":np.array(([-1,0])),
                  ">":np.array(([0,1])),
                  "<":np.array(([0,-1])),
                  }
        
        for subseq in subseqs:
            delta=np.array([0,0])
            for sym in subseq:
                delta+= sym_dict[sym]
            idx+=delta
            new_sym=self.mat_code[*idx]
            new_sym=str(new_sym)
            if new_sym=="10":
                new_sym="A"
            new_seq+=new_sym
        return new_seq    


class RobotDirectionalKeypad:
    def __init__(self):
        self.mat_code=np.array([["","^","A"],["<","v",">"]])
        self.symbols="<v>^A"

        self.min_paths=[["" for _ in self.symbols] for _ in self.symbols]
        
  
        for s, start_sym  in enumerate(self.symbols):
            for e, end_sym in  enumerate(self.symbols):
                if e<=s:
                    continue
                pos_s=np.array(np.where(self.mat_code==start_sym))
                pos_e=np.array(np.where(self.mat_code==end_sym))
                diff = np.squeeze(pos_e-pos_s)
                if start_sym=="<": # from left to everywhere else: first go right than go everywhere else
                    self.min_paths[s][e]= diff2seq(diff, 1) 
                    self.min_paths[e][s]= diff2seq(-diff, 0)
                else:
                    self.min_paths[s][e] = diff2seq(diff,-1)  
                    self.min_paths[e][s] = diff2seq(-diff,-1)
        
    def type_code(self, code):
        code_seq = list("A"+code) # from activation to code to activation
        
        idx = lambda i: self.symbols.find(code_seq[i])
        seq=""
        for i in range(len(code_seq)-1):
            seq+=self.min_paths[idx(i)][idx(i+1)]+"A" # I move from X to Y and then activate
        return seq
    def type(self, seq):
        new_seq=""
        subseqs = seq.split("A")[:-1]
        idx=np.squeeze(np.where(self.mat_code=="A"))
        sym_dict={"v":np.array(([1,0])),
                  "^":np.array(([-1,0])),
                  ">":np.array(([0,1])),
                  "<":np.array(([0,-1])),
                  }
        
        for subseq in subseqs:
            delta=np.array([0,0])
            for sym in subseq:
                delta+= sym_dict[sym]
            idx+=delta
            new_seq+=self.mat_code[*idx]
        return new_seq    


def solve_quiz1(fn=None, test_data=None, max_ps=2):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    complexities=[]
    for c, code in enumerate(data["codes"]):# FOR EACH CODE
        # 1. find the sequence that robot1 needs to type into the numerical keypad
        robot2 = RobotDirNumericKeypad()
        seq1 = robot2.type_code(code)
        print(code, "\n  ",seq1)
        assert robot2.type(seq1)==data["codes_str"][c]
    # 2. find the sequence that robot2 needs to type into the directional keyboard to move robot1
        robot3 = RobotDirectionalKeypad()
        seq2 = robot3.type_code(seq1)
        assert robot3.type(seq2)==seq1
        print("  ", seq2)
        
    # 3. find the sequence that I need to type into the directional keyboard to move robot2
        seq3 = robot3.type_code(seq2)
        print("  ", seq3)
            
    # 5. compute complexity as length of the sequence * code
        complexities.append(int(data["codes_int"][c])*len(seq3))
    return complexities



# %%
if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day21.txt"

    test_data = """029A
980A
179A
456A
379A"""

    complexities = solve_quiz1(test_data=test_data)
    total_complexity = np.sum(complexities) 
    i=0
    for complexity, true_compl in zip(complexities, (68*29, 60*980, 68*179, 64*456, 64*379)):
        check_test(f"\t1.{i+1} Comparing complexity", complexity, true_result=true_compl)
        i+=1

    complexities = solve_quiz1(fn=quiz_fn)
    total_complexity = np.sum(complexities) 
    check_test(f"🎄 🎄 🎄 Quiz1 result is", total_complexity,-1)
        

# %%
# TRUE: <v<A >>^A vA ^A <vA  <A   A >>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
# MINE: v<<A >>^A vA ^A v<<A >>^A A v<A<A>>^AAvAA^<A>Av<A^>AA<A>Av<A<A>>^AAA<Av>A^A
robotNum=RobotDirNumericKeypad()
robotDir=RobotDirectionalKeypad()

seq3="<v<A >>^A vA ^A <vA  <A   A >>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"
seq2=robotDir.type(seq3.replace(" ",""))
seq1=robotDir.type(seq2)
code=robotNum.type(seq1)
# %%
# CODE         3           7  9   A
# seq1_true = '^A  <<^^    A>>AvvvA'
# seq1_mine = '^A  ^^<<    A>>AvvvA'
# 
# SEQ1          ^ A           < <    ^ ^  A
# seq2_true = '<A>A       v<< A A >^ A A >A         vAA^A<vAAA>^A'
# SEQ1 mine                 ^ ^    < <    A
# seq2_mine = '<A>A       < A A v< A A >>^A         vAA^Av<AAA^>A'

# SEQ 2           <    A  >  A   
# seq3 true = '<v<A >>^A vA ^A <vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^    AAAvA<^A>A'
# seq3 mine = 'v<<A >>^A vA ^A v<<A>>^AAv<A<A>>^AAvAA^<A>Av<A^>AA<A>Av<A<A>>^AAA<Av>A^A'
