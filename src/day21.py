# %%
from common import INPUT_DIR, check_test, get_data, parse_mat, print_mat
from common import deltas_cross as deltas
import numpy as np
from numpy.linalg import norm


# %%
def printd(*args):
    #print(*args)
    pass
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
    def get_minpath(self, couple):
        idx = lambda char: self.symbols.find(char)
        return self.min_paths[idx(couple[0])][idx(couple[1])]


def solve_quiz1(fn=None, test_data=None, num_robots=2):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    complexities=[]
    for c, code in enumerate(data["codes"]):# FOR EACH CODE
        # 1. find the sequence that robot1 needs to type into the numerical keypad
        robotNum = RobotDirNumericKeypad()
        seq1 = robotNum.type_code(code)
        
        printd(data["codes_str"][c], "\n  ",seq1)
        assert robotNum.type(seq1)==data["codes_str"][c]
    # 2. find the sequence that robot2 needs to type into the directional keyboard to move robot1
        
        robotDir = RobotDirectionalKeypad()
        seq_i=seq1
        for i in range(num_robots-1):
            seq_next = robotDir.type_code(seq_i)
            assert robotDir.type(seq_next)==seq_i
            printd("  ", seq_next)
            seq_i=seq_next
        
    # 3. find the sequence that I need to type into the directional keyboard to move robot2
        seq_end = robotDir.type_code(seq_i)
        printd("  ", seq_end)
            
    # 5. compute complexity as length of the sequence * code
        complexities.append(int(data["codes_int"][c])*len(seq_end))
        printd(f"\t {int(data["codes_int"][c])}*{len(seq_end)} = {complexities[-1]}")
    return complexities

def populate_hashcount(seq, couples):
    hash_seqs={couple:0 for couple in couples}
    if seq=="":
        return hash_seqs
    for i in range(len(seq)-1):
        couple=seq[i]+seq[i+1]
        hash_seqs[couple]+=1
    return hash_seqs
def seq2instr(resp):
    list_instr=[]
    prev_r="A"
    for r in range(len(resp)):
        list_instr.append(prev_r+resp[r])
        prev_r=resp[r]
    return list_instr


def solve_quiz2(fn=None, test_data=None, num_robots=2):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    complexities=[]
    for c, code in enumerate(data["codes"]):# FOR EACH CODE
        # 1. find the sequence that robot1 needs to type into the numerical keypad
        robotNum = RobotDirNumericKeypad()
        seq1 = robotNum.type_code(code)
        printd(data["codes_str"][c], "\n  ",seq1)
        assert robotNum.type(seq1)==data["codes_str"][c]
        # E.g. for 029A is <A^A^^>AvvvA
        # create a robot directional keypad        
        robotDir = RobotDirectionalKeypad()
        # create the list of all possible combinations 
        symbols="<v>^A" 
        couples=[]
        for s in symbols:
            for s2 in symbols:
                if s+s2 in ["<>", "><", "^v", "v^"]:
                    continue
                couples.append(s+s2)
        # now I create few think
        # hashcount: how many examples are there for each couple? We always start with "A"
        hash_seqs=populate_hashcount("A"+seq1, couples) # remember to start from A
        hash_resp={couple:robotDir.get_minpath(couple)+"A" for couple in couples}
        # for each couple, what is the corresponding path?
        resp_hash={v: seq2instr(v) for _, v in hash_resp.items()}
        # for each path, what are the couples that compose it?
        for _ in range(num_robots):     # for each robot       
            new_hash_seqs=populate_hashcount("", couples)
            for instr, count in hash_seqs.items(): # now I know there are N counts
                resp = hash_resp[instr] 
                new_instrs= resp_hash[resp]
                for nin in new_instrs:
                    new_hash_seqs[nin]+= count
            hash_seqs = new_hash_seqs            
        
        len_seq=np.sum([c for _, c in hash_seqs.items()])
        
        
    # 5. compute complexity as length of the sequence * code
        complexities.append(int(data["codes_int"][c])*len_seq)
        printd(f"\t {int(data["codes_int"][c])}*{len_seq} = {complexities[-1]}")
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
    check_test(f"🎄 🎄 🎄 Quiz1 result is", total_complexity,179444)



    complexities = solve_quiz2(test_data=test_data, num_robots=2)
    total_complexity = np.sum(complexities) 
    i=0
    for complexity, true_compl in zip(complexities, (68*29, 60*980, 68*179, 64*456, 64*379)):
        check_test(f"\t2.{i+1} Comparing complexity", complexity, true_result=true_compl)
        i+=1

    complexities = solve_quiz2(fn=quiz_fn, num_robots=2)
    total_complexity = np.sum(complexities) 
    check_test(f"🎄 🎄 🎄 Quiz1 result with fast solution is", total_complexity,179444)

    complexities = solve_quiz2(fn=quiz_fn, num_robots=25)
    total_complexity = np.sum(complexities) 
    check_test(f"🎅 🎅 🎅 Quiz2 result is", total_complexity,223285811665866)
