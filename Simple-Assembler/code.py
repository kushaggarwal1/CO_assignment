import re


opcode={"add":"00000","sub":"00001","mov":"00010","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"10000","jgt":"10001","je":"10010","hlt":"10011"}
register_address={"r0":"000","r1":"001","r2":"010","r3":"011","r4":"100","r5":"101","r6":"110"}
label_instructions={}
label_lineno={}
var_addr={}
ISA_list = ["add","sub","mov","ld","st","mul","div","rs","ls","xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt","var"]
instruction_list = []
var_list = []
binary_out = []

def decimalToBinary(n):
    x = bin(n).replace("0b", "")
    y = len(x)
    z = (8-y)*"0" + str(x)
    return z



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
    if len(arr)!=3:
        return False
    if arr[1] not in register_address.keys():
        return False
    if arr[2] not in var_addr.keys():
        return False
    return True

def checkTypeE(arr):
    if arr[1] not in label_lineno.keys():
        return False
    return True

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



def type_1_error(x):
    for i in x:
        if i[0] not in ISA_list:
            print "Invalid Syntax"
            return False
    return True

def type_2_error(x):
    for i in x:
        if i[0] == "ld" or i[0] == "st":
            if i[2] not in var_list:
                print "Use of undefined variable"
                return False
    return True

def type_3_error(x):
    for i in x:
        if i[0] in ["jmp","jlt","jgt","je"]:
            if i[1] not in label_lineno.keys():
                print "Use of undefined label"
                return False
    return True

def type_4_error(x):
    for i in x:
        if "FLAG" in i:
            if i[0]!= "mov":
                print "Illegal use of FLAGS register"
                return False
    return True

def type_5_error(x):
    for i in x:
        if i[0] in ["mov", "rs", "ls"]:
            if i[2][0] == "$":
                if int(i[2][1:]) > 255 or int(i[2][1:]) <0:
                    print "Invalid immediate value"
                    return False
    return True

def type_6_error(x):
    for i in label_lineno.keys():
        if i in var_list:
            return False
    return True

def type_7_error(x):

    for k in range(len(x)):
        if x[k][0] == "hlt":
            break
        if x[k][0] == "var":
            print "Variables not declared at the beginning"
            return False
    return True

def type_8_error(x):
    for i in x:
        if i[0] == "hlt":
            return True
    print "Missing hlt statement"
    return False

def type_9_error(x):
     count = 0
     for i in range(len(x)):
         if x[i][0] == "hlt":
             count+=1
         if count == 2:
             print "Multiple hlt statements"
             return False
     if x[len(x)-1][0] != "hlt":
        print "hlt not being used as the last instruction"
        return False

     return True



def type_10_error(x):
    if checkError(x):
        return True
    else:
        return False





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


def main():

    while True:
        try:
            line = input()
            if line != "":
                instruction_list.append(line)

        except EOFError:
            break
    for i in instruction_list:      #for adjusting the variables in the instruction list to the bottom of the instruction set
        arr = i.split(" ")
        if arr[0] == 'var':
            var_list.append(arr[1])
            instruction_list.append(instruction_list.pop())
        else:
            break

    for i in range(len(instruction_list)):      #for storing the address of the variables
        arr = instruction_list[i].split(" ")
        if arr[0] == 'var':
            var_addr[arr[1]]=i      ##delete var from end of list!!!!!!!!!!!
    
def extraSpaceRemoval(a):       #s-->string      
    return re.sub(' +',' ', a)  #this removes the excess white spaces in the string




if __name__== "__main__":
    main()


