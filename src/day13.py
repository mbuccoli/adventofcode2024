# %%
from common import INPUT_DIR, check_test, get_data
import numpy as np

# %%

COST_A=3
COST_B=1

def parse(text_data):
    data=[]
    claw_machines=text_data.split("\n\n")
    for claw in claw_machines:
        
        a_text, b_text, prize_text = claw.split("\n") 
        claw_data={
            "Ax":int(a_text.split("X+")[1].split(",")[0]),
            "Ay":int(a_text.split("Y+")[1]),
            "Bx":int(b_text.split("X+")[1].split(",")[0]),
            "By":int(b_text.split("Y+")[1]),
            "px":int(prize_text.split("X=")[1].split(",")[0]),
            "py":int(prize_text.split("Y=")[1]),
        }
        data.append(claw_data)
    return data

def solve_test(claws):
    total_cost=0
    for claw in claws:
        Nb = claw["px"]*claw["Ay"]- claw["py"]*claw["Ax"]
        Nb/= (claw["Bx"]*claw["Ay"] - claw["By"]*claw["Ax"])        
        Na = (claw["px"]-Nb*claw["Bx"])/claw["Ax"] 
        if Na-int(Na)!=0 or Nb-int(Nb)!=0:
            continue # not integer
        if Na > 100 or Nb > 100:
            continue
        claw["Na"]=int(Na)
        claw["Nb"]=int(Nb)
        claw["cost"]=Na*COST_A+Nb*COST_B
        total_cost += claw["cost"]
    return claws, total_cost    
def solve_quiz(fn=None, test_data=None):
    text_data = get_data(fn, test_data)
    claws = parse(text_data)
    claws, total_cost = solve_test(claws)

    return total_cost
            
          

if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day13.txt"

    test_data = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
    
    result_test1 = solve_quiz(test_data=test_data)
    check_test(1, result_test1, true_result=480)
    
    print("🎄 🎄 🎄 Quiz1 result is", solve_quiz(fn=quiz_fn))


# %%

# prize_x = N_a * a_x + N_b * b_x
# prize_y = N_a * a_y + N_b * b_y

# N_a = prize_x/a_x - (N_b*b_x)/a_x = prize_y/a_y - (N_b*b_y)/a_y

# N_b*(b_x/a_x - b_y/a_y) = prize_x/a_x - prize_y/a_y
# 
#           prize_x*a_y - prize_y*a_x       
# N_b =     --------------------------    
#              (b_x*a_y - b_y*a_x)   