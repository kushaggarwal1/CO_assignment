opcode={"add":"00000","sub":"00001","mov":"00010","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"10000","jgt":"10001","je":"10010","hlt":"10011"}
register_address={"r0":"000","r1":"001","r2":"010","r3":"011","r4":"100","r5":"101","r6":"110","flag":"111"}

def decimalToBinary(n):
    x = bin(n).replace("0b", "")
    y = len(x)
    z = (8-y)*"0" + str(x)
    return z

def typeA(op,reg1,reg2,reg3):
    a=opcode(op)+"00"+register_address(reg1)+register_address(reg2)+register_address(reg3)
    return a

def typeB(op, reg1, val):
    a = opcode(op) + register_address(reg1) + decimalToBinary(val)
    return a
def typeC(op, reg1, reg2):
    a = opcode(op) + "00000" + register_address(reg1) + register_address(reg2)
    return a

def typeD(op, reg1, mem):
    a = opcode(op) + register_address(reg1) + "memory"
    return a

def typeE(op, mem):
    a = opcode(op) + "000" + "memory"
    return a

def typeF(op):
    a = opcode(op) + "00000000000"
    return a

def checkTypeA(arr):
    if len(arr)!=4:
        return False

    if arr[1] not in register_address.keys():
        return False
    if arr[2] not in register_address.keys():
        return False
    if arr[3] not in register_address.keys():
        return False
    return True


def checkTypeB(arr):
    if len(arr)!=3:
        return False
    if arr[1] not in register_address.keys():
        return False
    if type(arr[2]) != int:
        return False

    if type(arr[2]) == int:
        if arr[2]>255 or arr[2]<0:
            return False

    return True

def checkTypeC(arr):
    if len(arr)!=3:
        return False
    if arr[1] not in register_address.keys():
        return False
    if arr[2] not in register_address.keys():
        return False
    return True

def checkTypeD(arr):

    return

def checkTypeE(arr):

    return

def checkTypeF(arr):
    if len(arr) != 1:
        return False
    return True


def checkError(arr):
    if arr[0] == "add":
        return checkTypeA(arr)
    elif arr[0] == "sub":
        return checkTypeA(arr)
    elif arr[0] == "mov":
        return checkTypeB(arr) or checkTypeC
    elif arr[0] == "ld":
        return checkTypeD(arr)
    elif arr[0] == "st":
        return checkTypeD(arr)
    elif arr[0] == "mul":
        return checkTypeA(arr)
    elif arr[0] == "div":
        return checkTypeC(arr)
    elif arr[0] == "rs":
        return checkTypeB(arr)
    elif arr[0] == "ls":
        return checkTypeB(arr)
    elif arr[0] == "xor":
        return checkTypeA(arr)
    elif arr[0] == "or":
        return checkTypeA(arr)
    elif arr[0] == "and":
        return checkTypeA(arr)
    elif arr[0] == "not":
        return checkTypeC(arr)
    elif arr[0] == "cmp":
        return checkTypeC(arr)
    elif arr[0] == "jmp":
        return checkTypeE(arr)
    elif arr[0] == "jlt":
        return checkTypeE(arr)
    elif arr[0] == "jgt":
        return checkTypeE(arr)
    elif arr[0] == "je":
        return checkTypeE(arr)
    elif arr[0] == "hlt":
        return checkTypeF(arr)
    else:
        return False


def main():
    instruction_list = []
    var_list = []
    binary_out = []
    while True:
        try:
            line = input()
            instruction_list.append(line)

        except EOFError:
            break
    for i in instruction_list:
        arr = i.split(" ")
        if arr[0] == 'var':
            instruction_list.append(instruction_list.pop())





if __name__== "__main__":
    main()


