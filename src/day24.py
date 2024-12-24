"""Notes

"""
# %%
import numpy as np
from common import INPUT_DIR, get_data, check_test,check_solution
from tqdm import tqdm
import matplotlib.pyplot as plt
def printd(*args):
    #print(*args)
    pass

# %%

xor = lambda x, y: x!=y 

def parse(text_data):
    inputs, outputs = text_data.split("\n\n")
    input_dict={}
    for line in inputs.split("\n"):
        var, val = line.split(": ")
        input_dict[var] = bool(int(val))
    maxZ=0
    out_ops=[]
    lastZ=0
    for l, line in enumerate(outputs.split("\n")):
        inputs, output = line.split(" -> ")
        var1, op, var2 = inputs.split(" ")
        op=op.lower()
        if op=="xor":
            op="!="
        if var1 > var2: # let's keep input var with alphabetical order
            var1, var2 = var2, var1
        out_op = [output, var1, op, var2]
        out_ops.append(out_op)
        if output.startswith("z"):
            maxZ=max(maxZ, int(output[1:]))
            lastZ = l
    return {"input_dict":input_dict, "out_ops":out_ops, "maxZ":maxZ, "lastZ":lastZ}    

def build_data2(data):
    # WHAT DO I NEED?
    # I need, for each var, to understand WHERE they were used.
    Nbits=0
    for x in data["input_dict"]:
        Nbits=max(Nbits, int(x[1:]))
    data["Nbits"]=Nbits+1 # number of bits actually used
    cmd_as_in={}
    cmd_as_out={}
    def add_in_list(dict_, key_, val):
        list_=dict_.get(key_, [])
        list_.append(val)
        dict_[key_]=list_
        return dict_
    for i, op_i in enumerate(data["out_ops"]):
        o, v1, _, v2 = op_i
        cmd_as_out = add_in_list(cmd_as_out, o, i)
        cmd_as_in = add_in_list(cmd_as_in, v1, i)
        cmd_as_in = add_in_list(cmd_as_in, v2, i)
    data["cmd_as_in"]=cmd_as_in 
    data["cmd_as_out"]=cmd_as_out
    return data

def build_data(data):
    out_ops =data["out_ops"]
    out_eval = []
    inp = lambda var : f"input_dict['{var}']"
        
    for op_tuple in out_ops:
        _, var1, op, var2 = op_tuple
        cmd = f"{inp(var1)} {op} {inp(var2)}"
        out_eval.append(cmd)
    data["out_eval"] = out_eval
    return build_data2(data)

input_var = lambda v, i: f"{v}{str(i).zfill(2)}"

def find_out(data, var1=None, var2=None, op_="and"):
    common_op = set(data["cmd_as_in"][var1]) & set(data["cmd_as_in"][var2])
    for c in common_op:
        out_name, v1, o, v2 = data["out_ops"][c]
        if [v1, v2] in [[var1,var2], [var2, var1]] and o==op_:
            return out_name, c
    return "", -1
                         
def switch(data, out1, out2):
    o1= data["cmd_as_out"][out1][0]
    o2= data["cmd_as_out"][out2][0]
    data["out_ops"][o1][0] = out2
    data["out_ops"][o2][0] = out1
    return build_data2(data) # rebuild dicts

def find_ins(data, out):
    c= data["cmd_as_out"][out][0]
    op_line = data["out_ops"][c]
    return op_line[1], op_line[3], c 
def check_connection(data):
    # now, hopefully the wires should be something like:
    # z0 = x0 xor y0
    # carry_0 = x0 and y0
    #
    #
    # add_i = xi xor yi
    # zi = add_i xor carry_{i-1}
    #
    # and_i = xi and yi
    # carry_i_a = add_i AND carry_i-1
    # carry_i  = carry_i_a OR and_i
    # for now, let's just check
    # 
    assert ["z00", "x00", "!=", "y00"] in data["out_ops"], "This is the first problem"
    carry0_var, _ = find_out(data, "x00", "y00", "and") # find report    
    
    assert carry0_var != "", "Couldn't find a carry"
    prev_carry_var=carry0_var
    iv=input_var
    wrong_connections=[]
    for i in range(1,data["Nbits"]):
        add_i_var, add_i_c = find_out(data, iv("x",i), iv("y",i), "!=")
        zi_var, z_i_c = find_out(data, prev_carry_var, add_i_var, "!=")
        if z_i_c == -1:
            v1, v2, _ = find_ins(data, iv("z",i))
            v_change = v1 if v1 != prev_carry_var else v2
            wrong_connections.extend([v_change, add_i_var])
            
            switch(data, add_i_var, v_change)
            add_i_var, add_i_c = find_out(data, iv("x",i), iv("y",i), "!=")
            zi_var, z_i_c = find_out(data, prev_carry_var, add_i_var, "!=")
        if zi_var != iv("z",i): # Two possible problems: either not switched to the correct zi, or the carry was wrong. 
            wrong_connections.extend([zi_var,iv("z",i)])
            data = switch(data, zi_var, iv("z",i)) 
        and_i_var, and_i_c = find_out(data, iv("x",i), iv("y",i), "and")
        carry_i_a_var, carry_i_a_c = find_out(data, add_i_var, prev_carry_var, "and")         
        carry_i_var, carry_i_c = find_out(data, carry_i_a_var, and_i_var, "or")
        # Now, any of those MAY BE NOT CORRECT. In that case, I need to find the switch, but how?
        for i_c in [add_i_c, z_i_c, and_i_c, carry_i_a_c, carry_i_c]:
            if i_c==-1:
                print("HERE THERE IS A PROBLEM!")
        prev_carry_var = carry_i_var

    if prev_carry_var!=iv("z", i+1):#  CARRY
        wrong_connections.append(prev_carry_var)
        wrong_connections.append(iv("z",i+1))
            
    wrong_connections.sort()
    data["wc"]=wrong_connections
    return data
def find_num(data):
    input_dict = data["input_dict"]
    printd(input_dict)
    N = len(data["out_eval"])
    ops_done=[False for _ in range(N)] 
    opsN=0
    c=0
    zN=-1
    entire_loop=0
    while opsN<N and zN<data["maxZ"]:
        if ops_done[c]:
            c = (c+1)%N
        
            continue
        out_var, in_var1, _, in_var2 = data["out_ops"][c]
        
        if in_var1 not in input_dict or in_var2 not in input_dict:
            c = (c+1)%N
        
            continue
        
        cmd = data["out_eval"][c]
        printd(cmd)    
        input_dict[out_var] = eval(cmd)
        opsN+=1
        ops_done[c]=True
        if out_var[0]=="z":
            zN+=1
        c = (c+1)%N
        if c==0:
            entire_loop+=1
        if entire_loop>2: # 2 loops, I'm fine, MAYBE?
            break

    printd(input_dict)
    num=0
    for i in range(data["maxZ"]+1):
        varZ = f"z{str(i).zfill(2)}"
        num += int(input_dict[varZ])<<(i)
    data["num"]=num
    return data


def solve_quiz1(fn=None, test_data=None):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    data = build_data(data)
    data=find_num(data)
    return data["num"]

def solve_quiz2(fn=None, test_data=None):
    text_data = get_data(fn, test_data)
    data = parse(text_data)
    data = build_data(data)
    data = check_connection(data)
    
    return ",".join(data["wc"])



if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day24.txt"

    test_data = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""
    sol = solve_quiz1(test_data=test_data)
    check_test(f"\t1.1 comparison", sol, true_result=4)

    test_data="""x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

    sol2 =  solve_quiz1(test_data=test_data)
    check_test(f"\t1.2 comparison", sol2, true_result=2024)
        
    
    solution=solve_quiz1(fn=quiz_fn)
    check_solution(1, solution, 51410244478064)        
    

    solution=solve_quiz2(fn=quiz_fn)
    check_solution(2, solution, "gst,khg,nhn,tvb,vdc,z12,z21,z33")     

# %%
