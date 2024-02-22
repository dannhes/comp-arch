import sys
def check_rd(rd):
    dic_rd = {
        0: "zero",
        1: "ra",
        2: "sp",
        3: "gp",
        4: "tp",
        5: "t0",
        6: "t1",
        7: "t2",
        8: "s0",
        9: "s1",
        10: "a0",
        11: "a1",
        12: "a2",
        13: "a3",
        14: "a4",
        15: "a5",
        16: "a6",
        17: "a7",
        18: "s2", 19: "s3", 20: "s4", 21: "s5", 22: "s6", 23: "s7", 24: "s8", 25: "s9", 26: "s10", 27: "s11",
        28: "t3", 29: "t4", 30: "t5", 31: "t6"
    }
    return dic_rd[rd]
dict_text={}
def parse_im(a):
    res = int(a,2)-2**(len(a))*int(a[0])
    return str(res)


def b_type_parse(a):
    imm = a[0]*20+a[24]+a[1:7]+a[20:24]+"0"
    return parse_im(imm)
def check_func(a,flag):
    global count
    global cur_begin,dict_text,dict_text_1
    t = cur_begin
    if t in dict_text and flag!=1:
        file1.write( "\n%08x \t<%s>:\n" % (int(hex(t),16),dict_text[t]))
    elif t in dict_text_1 and flag!=1:
        file1.write("\n%08x \t<%s>:\n" % (int(hex(t),16), "L"+dict_text_1[t]))

    oppcode = a[-7:]
    rd = a[-12:-7]
    funct3 = a[-15:-12]
    rs1 = a[-20:-15]
    rs2 = a[-25:-20]
    funct7 = a[:-25]
    if oppcode == "0110111":
        imm = a[:-12]
        imm = parse_im(imm)
        imm = int(imm)
        if imm<=0:
            imm+=2**32
        return "LUI".lower(), check_rd(int(rd, 2)), "-", "-", hex(imm)
    if oppcode == "0010111":
        imm = a[:-12]
        imm = parse_im(imm)
        imm = int(imm)
        if imm < 0:
            imm += 2 ** 32
        return "AUIPC".lower(), check_rd(int(rd, 2)), "-", "-", hex(imm)
    if oppcode == "1101111":
        imm = a[:-12]
        imm_new = imm[0]*12 + imm[12:20]+imm[11]+imm[1:11]+"0"
        if int(t+int(parse_im(imm_new))) in dict_text:
            return "JAL".lower(), check_rd(int(rd, 2)), "-", "-", hex(t + int(parse_im(imm_new))), dict_text[int(t + int(parse_im(imm_new)))]
        else:

            if t+int(parse_im(imm_new)) not in dict_text_1:
                count += 1
                dict_text_1[t+int(parse_im(imm_new))]=str(count)
            imm_new_1=str(count)
            return "JAL".lower(), check_rd(int(rd, 2)), "-", "-", hex(t + int(parse_im(imm_new))), "L"+dict_text_1[t+int(parse_im(imm_new))]
    if oppcode == "1100111":
        if funct3 == "000":
            imm = funct7+rs2
            imm_new = imm[0]*12
            return "JALR".lower(), check_rd(int(rd, 2)),"-", "-", parse_im(funct7+rs2),check_rd(int(rs1, 2))
    if oppcode == "1100011":
        if t+int(b_type_parse(a)) in dict_text:
            imm_new_1 = dict_text[t+int(b_type_parse(a))]
        else:

            if t +int(b_type_parse(a)) not in dict_text_1:
                count += 1
                dict_text_1[t +int(b_type_parse(a))] = str(count)
            imm_new_1 = "L"+dict_text_1[t +int(b_type_parse(a))]

        if funct3 == "000":
            return "BEQ".lower(), "-", check_rd(int(rs1, 2)), check_rd(int(rs2, 2)), hex(t+int(b_type_parse(a))),imm_new_1
        if funct3 == "001":
            return "BNE".lower(), "-", check_rd(int(rs1, 2)), check_rd(int(rs2, 2)), hex(t+int(b_type_parse(a))),imm_new_1
        if funct3 == "100":
            return "BLT".lower(), "-", check_rd(int(rs1, 2)), check_rd(int(rs2, 2)), hex(t+int(b_type_parse(a))),imm_new_1
        if funct3 == "101":
            return "BGE".lower(), "-", check_rd(int(rs1, 2)), check_rd(int(rs2, 2)), hex(t+int(b_type_parse(a))),imm_new_1
        if funct3 == "110":
            return "BLTU".lower(), "-", check_rd(int(rs1, 2)), check_rd(int(rs2, 2)), hex(t+int(b_type_parse(a))),imm_new_1
        if funct3 == "111":
            return "BGEU".lower(), "-", check_rd(int(rs1, 2)), check_rd(int(rs2, 2)), hex(t+int(b_type_parse(a))),imm_new_1
    if oppcode == "0000011":
        if funct3 == "000":
            return "LB".lower(), check_rd(int(rd, 2)), "-", "-", parse_im(funct7+rs2),check_rd(int(rs1, 2))
        if funct3 == "001":
            return "LH".lower(), check_rd(int(rd, 2)), "-", "-", parse_im(funct7+rs2),check_rd(int(rs1, 2))
        if funct3 == "010":
            return "LW".lower(), check_rd(int(rd, 2)), "-", "-", parse_im(funct7+rs2),check_rd(int(rs1, 2))
        if funct3 == "100":
            return "LBU".lower(), check_rd(int(rd, 2)), "-", "-", parse_im(funct7+rs2),check_rd(int(rs1, 2))
        if funct3 == "101":
            return "LHU".lower(), check_rd(int(rd, 2)), "-", "-", parse_im(funct7+rs2),check_rd(int(rs1, 2))
    if oppcode == "0100011":
        if funct3 == "000":
            return "SB".lower(), "-", "-", check_rd(int(rs2, 2)), parse_im(funct7+rd),check_rd(int(rs1, 2))
        if funct3 == "001":
            return "SH".lower(), "-", "-", check_rd(int(rs2, 2)), parse_im(funct7+rd),check_rd(int(rs1, 2))
        if funct3 == "010":
            return "SW".lower(), "-", "-", check_rd(int(rs2, 2)), parse_im(funct7+rd),check_rd(int(rs1, 2))
    if oppcode == "0010011":
        if funct3 == "000":
            return "ADDI".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), "-", parse_im(funct7+rs2)
        if funct3 == "010":
            return "SLTI".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), "-", parse_im(funct7+rs2)
        if funct3 == "011":
            return "SLTIU".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), "-", parse_im(funct7+rs2)
        if funct3 == "100":
            return "XORI".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), "-", parse_im(funct7+rs2)
        if funct3 == "110":
            return "ORI".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), "-", parse_im(funct7+rs2)
        if funct3 == "111":
            return "ANDI".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), "-", parse_im(funct7+rs2)
        if funct3 == "001":
            if funct7 == "0000000":
                return "SLLI".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), str(int(rs2,2)), "-"
        if funct3 == "101":
            if funct7 == "0000000":
                return "SRLI".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), str(int(rs2,2)), "-"
            if funct7 == "0100000":
                return "SRAI".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), str(int(rs2,2)), "-"
    if oppcode == "0110011":
        if funct3 == "000":
            if funct7 == "0000000":
                return "ADD".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), check_rd(int(rs2, 2)), "-"
            if funct7 == "0100000":
                return "SUB".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), check_rd(int(rs2, 2)), "-"
        if funct3 == "001":
            if funct7 == "0000000":
                return "SLL".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), check_rd(int(rs2, 2)), "-"
        if funct3 == "010":
            if funct7 == "0000000":
                return "SLT".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), check_rd(int(rs2, 2)), "-"
        if funct3 == "011":
            if funct7 == "0000000":
                return "SLTU".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), check_rd(int(rs2, 2)), "-"
        if funct3 == "100":
            if funct7 == "0000000":
                return "XOR".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), check_rd(int(rs2, 2)), "-"
        if funct3 == "101":
            if funct7 == "0000000":
                return "SRL".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), check_rd(int(rs2, 2)), "-"
            if funct7 == "0100000":
                return "SRA".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), check_rd(int(rs2, 2)), "-"
        if funct3 == "110":
            if funct7 == "0000000":
                return "OR".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), check_rd(int(rs2, 2)), "-"
        if funct3 == "111":
            if funct7 == "0000000":
                return "AND".lower(), check_rd(int(rd, 2)), check_rd(int(rs1, 2)), check_rd(int(rs2, 2)), "-"
    if oppcode=="0001111":
        if a == "10000011001100000000000000001111":
            return "fense.i"
        if a == "00000001000000000000000000001111":
            return 'pause'
        else:
            pr1 = a[24:28]
            suc = a[20:24]
            pr = "i"*int(a[-28])+"o"*int(a[-27])+"r"*int(a[-26])+"w"*int(a[-25])
            sc = "i"*int(a[-24])+"o"*(int(a[-23]))+"r"*int(a[-22])+"w"*int(a[-21])
            return "fence",pr,sc
    if oppcode=="1110011":
        if a=="00000000000000000000000001110011":
            return 'ecall',"-","-"
        else:
            return "ebreak","-","-"
    if  oppcode=="0110011":
        if funct3=="000":
            return "mul",check_rd(int(rd,2)),check_rd(int(rs1,2)),check_rd(int(rs2,2))
        if funct3=="001":
            return "mulh",check_rd(int(rd,2)),check_rd(int(rs1,2)),check_rd(int(rs2,2))
        if funct3=="010":
            return "mulhsu",check_rd(int(rd,2)),check_rd(int(rs1,2)),check_rd(int(rs2,2))
        if funct3=="011":
            return "mulhu",check_rd(int(rd,2)),check_rd(int(rs1,2)),check_rd(int(rs2,2))
        if funct3=="100":
            return "div",check_rd(int(rd,2)),check_rd(int(rs1,2)),check_rd(int(rs2,2))
        if funct3=="101":
            return "divu",check_rd(int(rd,2)),check_rd(int(rs1,2)),check_rd(int(rs2,2))
        if funct3=="110":
            return "rem",check_rd(int(rd,2)),check_rd(int(rs1,2)),check_rd(int(rs2,2))
        if funct3=="111":
            return "remuw",check_rd(int(rd,2)),check_rd(int(rs1,2)),check_rd(int(rs2,2))
    return "invalid_instruction"

def check_symtab(a):
    global dict_text
    dict1 = {
        0:"NOTYPE", 1:"OBJECT", 2:"FUNC",3:"SECTION",4:"FILE",5:"COMMON",6:"TLS",
        10:"LOOS",12:"HIOS",13:"LOPROC",15:"HIPROC"
    }
    dict2 = {
        0:"LOCAL",1:"GLOBAL",2:"WEAK",10:"LOOS",12:"HIOS",13:"LOPROC",15:"HIPROC"
    }
    dict3 = ["DEFAULT","INTERNAL","HIDDEN","PROTECTED"]
    dict4 = {
        "0xff00":"LORESERVE","0x0":"UNDEF","0x0ff00":"LOPROC","0xff1f":"HIPROC",
        "0xfff1":"ABS","0xfff2":"COMMON","0xffff":"HIRESERVE"
    }
    name = int.from_bytes(a[:4],"little")
    value = int.from_bytes(a[4:8],"little")
    size = int.from_bytes(a[8:12],"little")
    type = int.from_bytes(a[12:13],"little") & 15
    bind = int.from_bytes(a[12:13],"little") >> 4
    vis = int.from_bytes(a[13:14],"little")
    ind = hex(int.from_bytes(a[14:16],"little"))
    s = ""

    s+=str(value)+" "
    s += str(size)+" "
    if type not in dict1:
        s+= str(type)+" "
    else:
        s += dict1[type]+" "
    if bind not in dict2:
        s+=str(bind)+" "
    else:
        s += dict2[bind]+" "
    s += dict3[vis]+ " "
    if ind not in dict4:
        s+=str(int(ind,16))+" "
    else:
        s+= dict4[ind]+" "
    j = name
    while int.from_bytes([strtab[j]],"little")!=0:
        s+=chr(strtab[j])
        j+=1

    return s

count = -1
dict_text_1={}
file = open(sys.argv[1],"rb")

file1 = open(sys.argv[2],'w')
f = file.read()
file1.write(".text\n")
section_header = int.from_bytes(f[32:36],"little")
section_header_size = int.from_bytes(f[46:48],"little")
section_header_count = int.from_bytes(f[48:50],"little")
if f[:4] != b"\x7fELF":
    file1.write("inv")
    exit(0)
strtab=""
symtab=""
section_headers = ""
text=""
begin_com_adr=0
for i in range(section_header_count):
    section_headers = f[section_header+section_header_size*(i):section_header+section_header_size*(i+1)]
    if int.from_bytes(section_headers[4:8],"little")==2:
        symtab = f[int.from_bytes(section_headers[16:20],"little"):int.from_bytes(section_headers[16:20],"little")+int.from_bytes(section_headers[20:24],"little")]
        symtab_size = int.from_bytes(section_headers[20:24],"little")
    elif int.from_bytes(section_headers[4:8],"little")==1 and int.from_bytes(section_headers[8:12],"little")==6:
        text = f[int.from_bytes(section_headers[16:20],"little"):int.from_bytes(section_headers[16:20],"little")+int.from_bytes(section_headers[20:24],"little")]
        text_size = int.from_bytes(section_headers[20:24],"little")
        begin_com_adr = int.from_bytes(section_headers[12:16],"little")
    elif int.from_bytes(section_headers[4:8],"little") == 3 and i != int.from_bytes(f[50:52],"little"):
        strtab = (f[int.from_bytes(section_headers[16:20],"little"):int.from_bytes(section_headers[16:20],"little")+int.from_bytes(section_headers[20:24],"little")])

absolute = []
b = []

for i in range(symtab_size // 16):
    comm = symtab[16 * i:16 * (i + 1)]
    if check_symtab(comm).split()[2] == "FUNC":
        dict_text[int(check_symtab(comm).split()[0])] = check_symtab(comm).split()[-1]
    b.append(check_symtab(comm))

for i in range(text_size//4):
    cur_begin = begin_com_adr+4*i
    comm = int.from_bytes(text[4*i:4*(i+1)],"little")
    comm = bin(comm)[2:]
    func = check_func((32-len(comm))*"0"+comm,flag=1)

count=-1
for i in range(text_size//4):
    cur_begin = begin_com_adr+4*i
    comm = int.from_bytes(text[4*i:4*(i+1)],"little")
    comm = bin(comm)[2:]
    func = check_func((32-len(comm))*"0"+comm,flag=0)
    ans=""
    ans= str(hex(cur_begin) +" "+ hex(int((32-len(comm))*"0"+comm,2)))+ " " +ans
    load = set(list(['lb', 'lh', 'lw', 'lbu', 'lhu']))
    store = set(list(['sb', 'sh', 'sw']))
    B_type = set(list(['beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu']))
    for i in range(len(func)):
        if func[i]!="-":
            ans+=func[i]+" "
    ans=ans.split()
    if ans[2] in load or ans[2] == "jalr" or ans[2] in store:
        file1.write("   %05x:\t%08x\t%7s\t%s, %d(%s)\n" % (int(ans[0],16),int(ans[1],16),ans[2],ans[3],int(ans[4]),ans[5]))
    elif ans[2] == "jal":
        file1.write("   %05x:\t%08x\t%7s\t%s, 0x%x <%s>\n" % (int(ans[0],16),int(ans[1],16),ans[2],ans[3],int(ans[4],16),ans[5]))
    elif ans[2] in B_type:
        file1.write("   %05x:\t%08x\t%7s\t%s, %s, 0x%x, <%s>\n" % (int(ans[0],16),int(ans[1],16),ans[2],ans[3],ans[4],int(ans[5],16),ans[6]))
    elif ans[2]=="fence":
        file1.write("   %05x:\t%08x\t%7s\t%s, %s\n" % (int(ans[0],16),int(ans[1],16),ans[2],ans[3],ans[4]))
    elif len(ans)==3:
        file1.write("   %05x:\t%08x\t%7s\n" % (int(ans[0],16),int(ans[1],16),ans[2]))
    elif len(ans)==6:
        file1.write("   %05x:\t%08x\t%7s\t%s, %s, %s\n" % (int(ans[0],16),int(ans[1],16),ans[2],ans[3],ans[4],ans[5]))
    elif len(ans)==5:
        file1.write("   %05x:\t%08x\t%7s\t%s, %s\n" % (int(ans[0],16),int(ans[1],16),ans[2],ans[3],ans[4]))
    else:
        file1.write("   %05x:\t%08x\t%-7s\n" % (int(ans[0],16),int(ans[1],16),ans[2]))

file1.write("\n\n.symtab\n")

file1.write("\nSymbol Value              Size Type     Bind     Vis       Index Name\n")
for i in range(symtab_size // 16):
    comm = symtab[16 * i:16 * (i + 1)]
    if check_symtab(comm).split()[2] == "FUNC":
        dict_text[int(check_symtab(comm).split()[0])] = check_symtab(comm).split()[-1]
    answer = check_symtab(comm).split()
    answer[0] = hex(int(answer[0]))

    #answer+=" "
    if len(answer)==7:
        file1.write("[%4i] 0x%-15X %5i %-8s %-8s %-8s %6s %s\n" % (i, int(answer[0], 16), int(answer[1]), answer[2], answer[3], answer[4], answer[5], answer[6]))
    else:
        file1.write("[%4i] 0x%-15X %5i %-8s %-8s %-8s %6s \n" % (i, int(answer[0], 16), int(answer[1]), answer[2], answer[3], answer[4], answer[5]))

