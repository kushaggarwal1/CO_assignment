import matplotlib.pyplot as plt

reg_val = {"000": 0, "001": 0, "010": 0, "011": 0, "100": 0, "101": 0, "110": 0}
reg_list = ["000", "001", "010", "011", "100", "101", "110"]
flag_val = {"V": 0, "L": 0, "G": 0, "E": 0}
var_storage = {}
PC = 0
mem_touched = []
cycle_touched = []
list_in = []
output = []
halted = False
cycle = 0

def BinPC(n):
    n = int(n)
    x = bin(n).replace("0b", "")
    y = len(x)
    z = (8 - y) * "0" + str(x)
    return z

def last16(x):
    return x[-16:]

def bin_to_dec(n):
    return int(n, 2)


def decimalToBinary(n):
    n = int(n)
    x = bin(n).replace("0b", "")
    y = len(x)
    z = (16 - y) * "0" + str(x)
    return z


def update_PC(new_PC):
    PC = new_PC
    return PC


def left_shift(x, y):
    x = x + y * "0"
    x = x[-16:]
    return x


def right_shift(x, y):
    x = y * "0" + x
    x = x[:16]
    return x


def bit_wise_not(x):
    y = ""
    for i in range(len(x)):
        if x[i] == "0":
            y += "1"
        else:
            y += "0"
    return y


def reset_flag():
    flag_val["E"] = 0
    flag_val["G"] = 0
    flag_val["L"] = 0
    flag_val["V"] = 0


def compare(x, y):
    flag_val["E"] = 0
    flag_val["G"] = 0
    flag_val["L"] = 0

    if x == y:
        flag_val["E"] = 1
    if x > y:
        flag_val["G"] = 1
    if x < y:
        flag_val["L"] = 1


def read_mem(PC):
    global halted
    global cycle
    global cycle_touched
    global mem_touched


    if list_in[PC][0:5] == "00000":  # add
        reset_flag()
        if reg_val[list_in[PC][10:13]] + reg_val[list_in[PC][13:16]] <= 65535:
            reg_val[list_in[PC][7:10]] = reg_val[list_in[PC][10:13]] + reg_val[list_in[PC][13:16]]
        else:
            reg_val[list_in[PC][7:10]] = bin_to_dec(last16(decimalToBinary(reg_val[list_in[PC][10:13]] + reg_val[list_in[PC][13:16]])))
            flag_val["V"] = 1

    if list_in[PC][0:5] == "00001":  # sub
        reset_flag()
        if (reg_val[list_in[PC][10:13]] - reg_val[list_in[PC][13:16]]) <= 0:
            reg_val[list_in[PC][7:10]] = 0
        else:
            reg_val[list_in[PC][7:10]] = reg_val[list_in[PC][10:13]] - reg_val[list_in[PC][13:16]]

    if list_in[PC][0:5] == "00010":  # mov imm
        reset_flag()
        reg_val[list_in[PC][5:8]] = bin_to_dec(list_in[PC][8:16])

    if list_in[PC][0:5] == "00011":  # mov reg
        if list_in[PC][13:16] == "111":
            reg_val[list_in[PC][10:13]] = bin_to_dec(get_flag_val())
        else:
            reg_val[list_in[PC][10:13]] = reg_val[list_in[PC][13:16]]
        reset_flag()

    if list_in[PC][0:5] == "00100":  # load
        reset_flag()
        reg_val[list_in[PC][5:8]] = bin_to_dec(list_in[bin_to_dec(list_in[PC][8:16])])
        mem_touched.append(bin_to_dec(list_in[PC][8:16]))
        cycle_touched.append(cycle)

    if list_in[PC][0:5] == "00101":  # store
        reset_flag()
        list_in[bin_to_dec(list_in[PC][8:16])] = decimalToBinary(reg_val[list_in[PC][5:8]])
        mem_touched.append(bin_to_dec(list_in[PC][8:16]))
        cycle_touched.append(cycle)

    if list_in[PC][0:5] == "00110":  # mul
        reset_flag()
        if (reg_val[list_in[PC][10:13]] * reg_val[list_in[PC][13:16]]) <= 65535:
            reg_val[list_in[PC][7:10]] = reg_val[list_in[PC][10:13]] * reg_val[list_in[PC][13:16]]
        else:
            reg_val[list_in[PC][7:10]] = bin_to_dec(
                last16(decimalToBinary(reg_val[list_in[PC][10:13]] * reg_val[list_in[PC][13:16]])))
            flag_val["V"] = 1

    if list_in[PC][0:5] == "00111":  # div
        reset_flag()
        reg_val["000"] = reg_val[list_in[PC][10:13]] // reg_val[list_in[PC][13:16]]
        reg_val["001"] = reg_val[list_in[PC][10:13]] % reg_val[list_in[PC][13:16]]

    if list_in[PC][0:5] == "01000":  # right shift
        reset_flag()
        reg_val[list_in[PC][5:8]] = bin_to_dec(
            right_shift(decimalToBinary(reg_val[list_in[PC][5:8]]), bin_to_dec(list_in[PC][8:16])))

    if list_in[PC][0:5] == "01001":  # left shift
        reset_flag()
        reg_val[list_in[PC][5:8]] = bin_to_dec(
            left_shift(decimalToBinary(reg_val[list_in[PC][5:8]]), bin_to_dec(list_in[PC][8:16])))

    if list_in[PC][0:5] == "01010":  # xor
        reset_flag()
        reg_val[list_in[PC][7:10]] = (reg_val[list_in[PC][10:13]] ^ reg_val[list_in[PC][13:16]])

    if list_in[PC][0:5] == "01011":  # or
        reset_flag()
        reg_val[list_in[PC][7:10]] = (reg_val[list_in[PC][10:13]] | reg_val[list_in[PC][13:16]])

    if list_in[PC][0:5] == "01100":  # and
        reset_flag()
        reg_val[list_in[PC][7:10]] = (reg_val[list_in[PC][10:13]] & reg_val[list_in[PC][13:16]])

    if list_in[PC][0:5] == "01101":  # not
        reset_flag()
        reg_val[list_in[PC][10:13]] = bin_to_dec(bit_wise_not(decimalToBinary(reg_val[list_in[PC][13:16]])))

    if list_in[PC][0:5] == "01110":  # cmp
        reset_flag()
        compare(reg_val[list_in[PC][10:13]], reg_val[list_in[PC][13:16]])

    if list_in[PC][0:5] == "01111":  # jmp
        PC = update_PC(bin_to_dec(list_in[PC][8:16]))
        reset_flag()

    if list_in[PC][0:5] == "10000":  # jlt
        if flag_val["L"] == 1:
            PC = update_PC(bin_to_dec(list_in[PC][8:16]))
        reset_flag()

    if list_in[PC][0:5] == "10001":  # jgt
        if flag_val["G"] == 1:
            PC = update_PC(bin_to_dec(list_in[PC][8:16]))
        reset_flag()

    if list_in[PC][0:5] == "10010":  # je
        if flag_val["E"] == 1:
            PC = update_PC(bin_to_dec(list_in[PC][8:16]))
        reset_flag()

    if list_in[PC][0:5] == "10011":  # hlt
        reset_flag()
        halted = True
    mem_touched.append(PC)
    cycle_touched.append(cycle)
    cycle+=1
    list1 = []

    list1.append(BinPC(PC))

    for i in reg_list:
        list1.append(decimalToBinary(reg_val[i]))

    list1.append(get_flag_val())
    return list1, halted


def get_flag_val():
    return "000000000000" + str(flag_val["V"]) + str(flag_val["L"]) + str(flag_val["G"]) + str(flag_val["E"])


def memory_dump(memory):
    for i in memory:
        print(i)

    for i in range(len(memory), 256):
        print("0000000000000000")


def main():
    global PC
    global cycle
    global cycle_touched
    global mem_touched

    while True:

        try:
            line = input()
            if line != "":
                list_in.append(line)

        except EOFError:
            break

    for i in range(len(list_in), 256):
        list_in.append("0000000000000000")
    while (True):
        x, halted = read_mem(PC)
        output.append(x)
        PC = update_PC(PC + 1)
        if halted == True:
            break

    plt.scatter(x=cycle_touched,y=mem_touched)
    for i in output:
        print(' '.join(i))
    memory_dump(list_in)
    plt.show()

if __name__ == '__main__':
    main()
