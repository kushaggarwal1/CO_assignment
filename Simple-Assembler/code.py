opcode={"add":"00000","sub":"00001","mov":"00010","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"10000","jgt":"10001","je":"10010","hlt":"10011"}
register_address={"r0":"000","r1":"001","r2":"010","r3":"011","r4":"100","r5":"101","r6":"110","flag":"111"}


def decimalToBinary(n):
    x = bin(n).replace("0b", "")
    y = len(x)
    z = (8-y)*"0" + str(x)
    return z;

def typeA(op,reg1,reg2,reg3):
    a=opcode(op)+"00"+register_address(reg1)+register_address(reg2)+register_address(reg3)
    return a

def typeB(op, reg1, val):
    a = opcode(op) + register_address(reg1) + decimalToBinary(val)
    return a;
def typeC(op, reg1, reg2):
    a = opcode(op) + "00000" + register_address(reg1) + register_address(reg2)
    return a;

def typeD(op, reg1, mem):
    a = opcode(op) + register_address(reg1) + "memory"
    return a;

def typeE(op, mem):
    a = opcode(op) + "000" + "memory"
    return a;

def typeF(op):
    a = opcode(op) + "00000000000"
    return a;

def checkError()


