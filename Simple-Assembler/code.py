opcode={"add":"00000","sub":"00001","mov":"00010","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"10000","jgt":"10001","je":"10010","hlt":"10011"}
register_address={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110", "FLAGS":"111"}
label_lineno={}
var_addr={}
ISA_list = ["add","sub","mov","ld","st","mul","div","rs","ls","xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt","var"]
typeA_list = ["add","sub","mul","xor","or","and"]
typeB_list = ["rs","ls"]
typeC_list = ["div","not","cmp"]
typeD_list = ["ld","st"]
typeE_list = ["jmp","jlt","jgt","je"]
typeF_list = ["hlt"]

instruction_list = []
var_list = []
binary_out = []

def decimalToBinary(n):
    x = bin(n).replace("0b", "")
    y = len(x)
    z = (8-y)*"0" + str(x)
    return z

def checkTypeA(arr):
    if arr[0][len(arr[0])-1] == ":":
        i = 1
        if len(arr)!=5:
            return False
    else:
        i = 0
        if len(arr)!=4:
            return False

    if arr[i+1] not in register_address.keys():
        return False
    if arr[i+2] not in register_address.keys():
        return False
    if arr[i+3] not in register_address.keys():
        return False
    return True


def checkTypeB(arr):

    if arr[0][len(arr[0])-1] == ":":
        i = 1
        if len(arr)!=4:
            return False
    else:
        i = 0
        if len(arr)!=3:
            return False

    if arr[i+1] not in register_address.keys():
        return False
    if arr[i+2][0] != "$":
        return False

    if type(arr[i+2]) == int:
        if arr[i+2]>255 or arr[2]<0:
            return False

    return True

def checkTypeC(arr):

    if arr[0][-1] == ":":
        i = 1
        if len(arr)!=4:
            return False
    else:
        i = 0
        if len(arr)!=3:
            return False

    if arr[i+1] not in register_address.keys():
        return False
    if arr[i+2] not in register_address.keys():
        return False
    return True

def checkTypeD(arr):

    if arr[0][len(arr[0])-1] == ":":
        i = 1
        if len(arr)!=4:
            return False
    else:
        i = 0
        if len(arr)!=3:
            return False

    if arr[i+1] not in register_address.keys():
        return False
    if arr[i+2] not in var_addr.keys():
        return False
    return True

def checkTypeE(arr):
    if arr[0][len(arr[0])-1] == ":":
        i = 1
        if len(arr)!=3:
            return False
    else:
        i = 0
        if len(arr)!=2:
            return False

    if arr[i+1] not in label_lineno.keys():
        return False
    return True

def checkTypeF(arr):
    if arr[0][len(arr[0])-1] == ":":
        i = 1
        if len(arr)!=2:
            return False
    else:
        i = 0
        if len(arr)!=1:
            return False
    return True



def checkError(x):
    bool = True

    for arr in x:
        if arr[0][len(arr[0])-1] == ":":
            i = 1
        else:
            i = 0
        if arr[i] in typeA_list:
            if checkTypeA(arr) == False:
                bool = False
                break
        elif arr[i] in typeB_list:
            if checkTypeB(arr) == False:
                bool = False
                break
        elif arr[i] in typeC_list:
            if checkTypeC(arr) == False:
                bool = False
                break

        elif arr[i] in typeD_list:
            if checkTypeD(arr) == False:
                bool = False
                break
        elif arr[i] in typeE_list:
            if checkTypeE(arr) == False:
                bool = False
                break
        elif arr[i] in typeF_list:
            if checkTypeF(arr) == False:
                bool = False
                break
        elif arr[i] == "mov":
            if arr[i+2][0] == "$":
                if checkTypeB(arr)==False:
                    bool = False
                    break
            else:
                if checkTypeC(arr) == False:
                    bool = False
                    break

        elif arr[i] not in ISA_list:
            bool = False
            break
    return bool


def type_1_error(x):
    for i in x:
        if i[0][-1] == ":":
            k = 1
        else:
            k = 0

        if i[k+0] not in ISA_list:
            print ("Invalid Syntax")
            return False
    return True

def type_2_error(x):
    for i in x:
        if i[0][len(i[0])-1] == ":":
            k = 1
        else:
            k = 0
        if i[k+0] == "ld" or i[k+0] == "st":
            if i[k+2] not in var_list:
                print ("Use of undefined variable")
                return False
    return True

def type_3_error(x):
    for i in x:
        if i[0][len(i[0])-1] == ":":
            k = 1
        else:
            k = 0

        if i[k+0] in ["jmp","jlt","jgt","je"]:
            if i[k+1] not in label_lineno.keys():
                print ("Use of undefined label")
                return False
    return True

def type_4_error(x):
    for i in x:
        if i[0][len(i[0])-1] == ":":
            k = 1
        else:
            k = 0
        if "FLAGS" in i:
            if i[k+0] != "mov":
                print ("Illegal use of FLAGS register")
                return False
    return True

def type_5_error(x):
    for i in x:
        if i[0][len(i[0])-1] == ":":
            k = 1
        else:
            k = 0
        if i[k+0] in ["mov", "rs", "ls"]:
            if i[k+2][0] == "$":
                if int(i[k+2][1:]) > 255 or int(i[2][1:]) <0:
                    print ("Invalid immediate value")
                    return False
    return True

def type_6_error(x):
    for i in label_lineno.keys():
        if i in var_list:
            print("Misuse of labels as variables")
            return False
    return True

def type_7_error(x):

    for k in range(len(x)):
        if x[k][-1] == ":":
            m = 1
        else:
            m = 0

        if x[k][m+0] == "var":
            print ("Variables not declared at the beginning")
            return False
    return True

def type_8_error(x):
    for i in x:
        if i[0][len(i[0])-1] == ":":
            k = 1
        else:
            k = 0
        if i[k+0] == "hlt":
            return True
    print ("Missing hlt statement")
    return False

def type_9_error(x):
     count = 0
     z =0
     for i in range(len(x)):
         if x[i][len(x[i]) - 1] == ":":
             m = 1
         else:
             m = 0
         if x[i][m+0] == "hlt":
             count+=1
         if count == 2:
             print ("Multiple hlt statements")
             return False

     if x[len(x)-1][0][-1] == ":":
         z = 1

     if x[len(x)-1][z+0] != "hlt":
        print ("hlt not being used as the last instruction")
        return False

     return True



def type_10_error(x):
    if checkError(x):
        return True
    else:
        print ("Wrong syntax used for instructions")
        return False


def all_errors(x):
    for i in x:
        if len(i) == 1 and i[0][-1] == ":":
            print ("Invalid Syntax")
            return False

    if type_1_error(x) and type_2_error(x) and type_3_error(x) and type_4_error(x) and type_5_error(x) and type_6_error(x) and type_7_error(x) and type_8_error(x) and type_9_error(x) and type_10_error(x):
        return True

    else:
        return False


def typeA(op,reg1,reg2,reg3):

    a = opcode[op]+"00"+register_address[reg1]+register_address[reg2]+register_address[reg3]

    return a

def typeB(op, reg1, val):
    a = opcode[op] + register_address[reg1] + decimalToBinary(int(val[1:]))
    return a
def typeC(op, reg1, reg2):
    if op == "mov":
        a = "00011" + "00000" + register_address[reg1] + register_address[reg2]
    else:
        a = opcode[op] + "00000" + register_address[reg1] + register_address[reg2]
    return a

def typeD(op, reg1, mem):
    a = opcode[op] + register_address[reg1] + decimalToBinary(int(var_addr[mem]))
    return a

def typeE(op, mem):
    a = opcode[op] + "000" + decimalToBinary(int(label_lineno[mem]))
    return a

def typeF(op):
    a = opcode[op] + "00000000000"
    return a


def main():


    while True:

        try:
            line = input()
            if line != "":
                instruction_list.append(line)

        except EOFError:
            break


    for i in range(len(instruction_list)):
        arr = instruction_list[i].split()
        instruction_list[i] = arr

    for i in range(len(instruction_list)):

        if instruction_list[i][0] == "var":
            var_addr[instruction_list[i][1]] = i
            var_list.append(instruction_list[i][1])
        else:
            break

    boolean = True
    while boolean == True:
        if instruction_list[0][0] == "var":
            instruction_list.pop(0)
        else:
            boolean = False

    for i in var_addr:
        var_addr[i] += len(instruction_list)

    for i in range(len(instruction_list)):
        if instruction_list[i][0][-1] == ":":
            label_lineno[instruction_list[i][0][0:-1]] = i

    if all_errors(instruction_list) == False:
        exit()

    for i in instruction_list:
        if i[0][-1] == ":":
            label_flag = 1
        else:
            label_flag = 0
        if i[label_flag] in typeA_list:
            binary_out.append(typeA(i[label_flag+0],i[label_flag+1],i[label_flag+2],i[label_flag+3]))
        if i[label_flag] in typeB_list:
            binary_out.append(typeB(i[label_flag+0],i[label_flag+1],i[label_flag+2]))
        if i[label_flag] in typeC_list:
            binary_out.append(typeC(i[label_flag+0],i[label_flag+1],i[label_flag+2]))
        if i[label_flag] in typeD_list:
            binary_out.append(typeD(i[label_flag + 0], i[label_flag + 1], i[label_flag + 2]))
        if i[label_flag] in typeE_list:
            binary_out.append(typeE(i[label_flag + 0], i[label_flag + 1]))
        if i[label_flag] in typeF_list:
            binary_out.append(typeF(i[label_flag + 0]))
        if i[label_flag] == "mov":
            if i[label_flag+2][0] == "$":
                binary_out.append(typeB(i[label_flag+0],i[label_flag+1],i[label_flag+2]))
            else:
                binary_out.append(typeC(i[label_flag + 0], i[label_flag + 1], i[label_flag + 2]))
    for i in binary_out:
        print(i)


if __name__== "__main__":
    main()


