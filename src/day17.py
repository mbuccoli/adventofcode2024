"""

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

class PC:
    def __init__(self):
        
        self.pointer=0
        self.reg={"A":0, "B": 0, "C": 0}
        self.reg_combo={4:"A", 5: "B", 6: "C"}
        
        self.program=[]
        self.ops=[            
            self.adv, # (opcode 0)
            self.bxl, # (opcode 1)
            self.bst, # (opcode 2)
            self.jnz, # (opcode 3)
            self.bxc, # (opcode 4)
            self.out, # (opcode 5)
            self.bdv, # (opcode 6)
            self.cdv, # (opcode 7)
        ]

        self.outs=[]
    def get_combo_op(self, op):
        """
        Combo operands 0 through 3 represent literal values 0 through 3.
        Combo operand 4 represents the value of register A.
        Combo operand 5 represents the value of register B.
        Combo operand 6 represents the value of register C.
        Combo operand 7 is reserved and will not appear in valid programs.
        """

        if op<=3:
            return op
        return self.reg[self.reg_combo[op]]
    

    def parse(self, text_data):
        registers, program=text_data.split("\n\n")
        for reg in registers.split("\n"):
            name, value = reg.split(": ")
            name = name.split(" ")[1]
            self.reg[name]=int(value)
        self.program = [int(op) for op in program.split(": ")[1].split(",")]
        self.pointer = 0
        

    def xdv(self, op, reg):
        """
        The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.
        """
        num = self.reg["A"]
        den = 2**(self.get_combo_op(op))
        
        self.reg[reg]=num//den
    def adv(self, op):
        """
        The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.
        """
        self.xdv(op,"A")

    def bxl(self, op):
        """
        The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.
        """

        self.reg["B"] = np.bitwise_xor(op, self.reg["B"])

    def bst(self, op):    
        """The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.
        """
        self.reg["B"] = self.get_combo_op(op)%8
    def jnz(self, op):
        """The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction."""
        if self.reg["A"]==0:
            return
        self.pointer = op - 2 # we will increase it by 2 afterwards
    def bxc(self, op):
        """
        The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
        """
        self.reg["B"] = np.bitwise_xor(self.reg["B"], self.reg["C"])
    def out(self, op):
        """The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)"""

        self.outs.append(self.get_combo_op(op)%8)
    def bdv(self, op):
        """The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)"""
        self.xdv(op,"B")
    def cdv(self, op):

        """The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)"""
        self.xdv(op,"C")
    def run(self):
        while self.pointer<len(self.program):
            opcode = self.program[self.pointer]
            operand = self.program[self.pointer+1]
            self.ops[opcode](operand)
            self.pointer+=2
    def print_outs(self):
        #(If a program outputs multiple values, they are separated by commas.)
        return ",".join([str(out) for out in self.outs])

def solve_quiz1(fn=None, test_data=None):
    text_data = get_data(fn, test_data)
    pc = PC()
    pc.parse(text_data)
    pc.run()
    return pc.print_outs()




if __name__ == "__main__":
    quiz_fn = INPUT_DIR / "day17.txt"

    test_data = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
    
    outs = solve_quiz1(test_data=test_data)
    check_test(f"1.1 ", outs, true_result="4,6,3,5,6,3,5,2,1,0")
    
    outs = solve_quiz1(fn=quiz_fn)
    check_solution(1, outs, "7,6,5,3,6,5,7,0,4")
# %%
"""
--- Day 17: Chronospatial Computer ---

The eight instructions are as follows:

Here are some examples of instruction operation:

If register C contains 9, the program 2,6 would set register B to 1.
If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
If register B contains 29, the program 1,7 would set register B to 26.
If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
The Historians' strange device has finished initializing its debugger and is displaying some information about the program it is trying to run (your puzzle input). For example:

Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
Your first task is to determine what the program is trying to output. To do this, initialize the registers to the given values, then run the given program, collecting any output produced by out instructions. (Always join the values produced by out instructions with commas.) After the above program halts, its final output will be 4,6,3,5,6,3,5,2,1,0.

Using the information provided by the debugger, initialize the registers to the given values, then run the program. Once it halts, what do you get if you use commas to join the values it output into a single string?

To begin, get your puzzle input.
"""