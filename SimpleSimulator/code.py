import numpy
reg_val = {"000": 0, "001": 0, "010": 0, "011": 0, "100": 0, "101": 0, "110": 0}
reg_list = ["000", "001", "010", "011", "100", "101", "110"]
flag_val = {"V": 0, "L": 0, "G": 0, "E": 0}
var_storage = {}
PC = 0
list_in = []
output = []
halted = False

def BinPC(n):
    n = int(n)
    x = bin(n).replace("0b", "")
    y = len(x)
    z = (8 - y) * "0" + str(x)
    return z


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

    if list_in[PC][0:5] == "00000":
        reset_flag()
        if reg_val[list_in[PC][10:13]] + reg_val[list_in[PC][13:16]] <= 65535:
            reg_val[list_in[PC][7:10]] = reg_val[list_in[PC][10:13]] + reg_val[list_in[PC][13:16]]
        else:
            flag_val["V"] = 1

    if list_in[PC][0:5] == "00001":
        reset_flag()
        if (reg_val[list_in[PC][10:13]] - reg_val[list_in[PC][13:16]]) <= 0:
            reg_val[list_in[PC][7:10]] = 0
        else:
            reg_val[list_in[PC][7:10]] = reg_val[list_in[PC][10:13]] - reg_val[list_in[PC][13:16]]

    if list_in[PC][0:5] == "00010":
        reset_flag()
        reg_val[list_in[PC][5:8]] = bin_to_dec(list_in[PC][8:16])

    if list_in[PC][0:5] == "00011":
        if list_in[PC][13:16] == "111":
            reg_val[list_in[PC][10:13]] = bin_to_dec(get_flag_val())
        else:
            reg_val[list_in[PC][10:13]] = reg_val[list_in[PC][13:16]]
        reset_flag()

    if list_in[PC][0:5] == "00100":
        reg_val[list_in[PC][5:8]] = bin_to_dec(list_in[bin_to_dec(list_in[PC][8:16])])

    if list_in[PC][0:5] == "00101":
        list_in[bin_to_dec(list_in[PC][8:16])] = decimalToBinary(reg_val[list_in[PC][5:8]])


    if list_in[PC][0:5] == "00110":
        reset_flag()
        reg_val[list_in[PC][7:10]] = reg_val[list_in[PC][10:13]] * reg_val[list_in[PC][13:16]]

    if list_in[PC][0:5] == "00111":
        reset_flag()
        reg_val["000"] = reg_val[list_in[PC][10:13]] // reg_val[list_in[PC][13:16]]
        reg_val["001"] = reg_val[list_in[PC][10:13]] % reg_val[list_in[PC][13:16]]

    if list_in[PC][0:5] == "01000":
        reset_flag()
        reg_val[list_in[PC][5:8]] = bin_to_dec(
            right_shift(decimalToBinary(reg_val[list_in[PC][5:8]]), bin_to_dec(list_in[PC][8:16])))

    if list_in[PC][0:5] == "01001":
        reset_flag()
        reg_val[list_in[PC][5:8]] = bin_to_dec(
            left_shift(decimalToBinary(reg_val[list_in[PC][5:8]]), bin_to_dec(list_in[PC][8:16])))

    if list_in[PC][0:5] == "01010":
        reset_flag()
        reg_val[list_in[PC][7:10]] = (reg_val[list_in[PC][10:13]] ^ reg_val[list_in[PC][13:16]])

    if list_in[PC][0:5] == "01011":
        reset_flag()
        reg_val[list_in[PC][7:10]] = (reg_val[list_in[PC][10:13]] | reg_val[list_in[PC][13:16]])

    if list_in[PC][0:5] == "01100":
        reset_flag()
        reg_val[list_in[PC][7:10]] = (reg_val[list_in[PC][10:13]] & reg_val[list_in[PC][13:16]])

    if list_in[PC][0:5] == "01101":
        reset_flag()
        reg_val[list_in[PC][10:13]] = bin_to_dec(bit_wise_not(decimalToBinary(reg_val[list_in[PC][13:16]])))

    if list_in[PC][0:5] == "01110":
        reset_flag()
        compare(reg_val[list_in[PC][10:13]], reg_val[list_in[PC][13:16]])

    if list_in[PC][0:5] == "01111":
        PC = update_PC(bin_to_dec(list_in[PC][8:16]))
        reset_flag()

    if list_in[PC][0:5] == "10000":
        if flag_val["L"] == 1:
            PC = update_PC(bin_to_dec(list_in[PC][8:16]))
        reset_flag()

    if list_in[PC][0:5] == "10001":
        if flag_val["G"] == 1:
            PC = update_PC(bin_to_dec(list_in[PC][8:16]))
        reset_flag()

    if list_in[PC][0:5] == "10010":
        if flag_val["E"] == 1:
            PC = update_PC(bin_to_dec(list_in[PC][8:16]))
        reset_flag()

    if list_in[PC][0:5] == "10011":
        reset_flag()
        halted = True

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

    while True:
        # if len(list_in) == 8:
        #     break

        try:
            line = input()
            if line != "":
                list_in.append(line)

        except EOFError:
            break

    for i in range(len(list_in),256):
        list_in.append("0000000000000000")
    while (True):
        x, halted = read_mem(PC)
        output.append(x)
        PC = update_PC(PC + 1)
        if halted == True:
            break

    for i in output:
        print(' '.join(i))
    memory_dump(list_in)


if __name__ == '__main__':
    main()
