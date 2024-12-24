"""Notes

"""
# %%
import numpy as np
from common import INPUT_DIR, get_data, check_test,check_solution
from tqdm import tqdm
import matplotlib.pyplot as plt
def printd(*args):
    print(*args)
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
        out_op = (output, var1, op, var2)
        out_ops.append(out_op)
        if output.startswith("z"):
            maxZ=max(maxZ, int(output[1:]))
            lastZ = l
    return {"input_dict":input_dict, "out_ops":out_ops, "maxZ":maxZ, "lastZ":lastZ}    

def build_data(data):
    out_ops =data["out_ops"]
    out_eval = []
    inp = lambda var : f"input_dict['{var}']"
        
 
    for op_tuple in out_ops:
        _, var1, op, var2 = op_tuple
        cmd = f"{inp(var1)} {op} {inp(var2)}"
        out_eval.append(cmd)
    data["out_eval"] = out_eval
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
    check_solution(1, solution)        
    