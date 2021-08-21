reg_val={"000":0,"001":0,"010":0,"011":0,"100":0,"101":0,"110":0,"111":0}
flag_val={"v":0,"l":0,"g":0,"e":0}

def get_flag_val():
    return "000000000000"+str(flag_val("v"))+str(flag_val("l"))+str(flag_val("g"))+str(flag_val("e"))

def memory_dump(x):
    for i in x:
        print(i)
    for i in range(len(x),256):
        print("0000000000000000")
    

def main():
    pass
if __name__ == '__main__':
    main()