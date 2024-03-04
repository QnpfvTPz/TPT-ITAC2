

opcodes = { # [opcode, format] ; (I) marks for availability for immediate value or label
    "HLT" : [0x10,0x0000],  # HLT
    "BOM" : [0x01,0x0000],  # BOM
    "BOMB": [0x01,0x0000],  # BOMB
    "f02" : [0x02,0x0001],  # f02 [rd]
    "BIC" : [0x03,0x2107],  # BIC [rd] [rs1] [rs2 (I)]
    "&~"  : [0x03,0x2107],  # BIC [rd] [rs1] [rs2 (I)]
    "OR"  : [0x04,0x2107],  # OR [rd] [rs1] [rs2 (I)]
    "|"   : [0x04,0x2107],  # | [rd] [rs1] [rs2 (I)]
    "AND" : [0x05,0x2107],  # AND [rd] [rs1] [rs2 (I)]
    "&"   : [0x05,0x2107],  # & [rd] [rs1] [rs2 (I)]
    "XOR" : [0x06,0x2107],  # XOR [rd] [rs1] [rs2 (I)]
    "^"   : [0x06,0x2107],  # ^ [rd] [rs1] [rs2 (I)]
    "SRA" : [0x07,0x2107],  # SRA [rd] [rs1] [rs2 (I)]
    "SLL" : [0x08,0x2107],  # SLL [rd] [rs1] [rs2 (I)]
    "<<"  : [0x08,0x2107],  # << [rd] [rs1] [rs2 (I)]
    "SRL" : [0x09,0x2107],  # SRL [rd] [rs1] [rs2 (I)]
    ">>"  : [0x09,0x2107],  # >> [rd] [rs1] [rs2 (I)]
    "ADD" : [0x0A,0x2107],  # ADD [rd] [rs1] [rs2 (I)]
    "+"   : [0x0A,0x2107],  # + [rd] [rs1] [rs2 (I)]
    "MOV" : [0x0A,0x0203],  # MOV [rd] [rs (I)]
    "SUB" : [0x0B,0x2107],  # SUB [rd] [rs1] [rs2 (I)]
    "-"   : [0x0B,0x2107],  # - [rd] [rs1] [rs2 (I)]
    "B"   : [0x1C,0x0021],  # B [rd]
    "BNE" : [0x0C,0x1027],  # BNE [inst addr (I)] [rs1] [rs2]
    "B!=" : [0x0C,0x1027],  # B!= [inst addr (I)] [rs1] [rs2]
    "B<>" : [0x0C,0x1027],  # B!= [inst addr (I)] [rs1] [rs2]
    "BEQ" : [0x1C,0x1027],  # BEQ [inst addr (I)] [rs1] [rs2]
    "B==" : [0x1C,0x1027],  # B== [inst addr (I)] [rs1] [rs2]
    "BLT" : [0x0D,0x0127],  # BLT [inst addr (I)] [rs1] [rs2]
    "B<"  : [0x0D,0x0127],  # B< [inst addr (I)] [rs1] [rs2]
    "B>"  : [0x0D,0x1027],  # B> [inst addr (I)] [rs1] [rs2]
    "BGE" : [0x1D,0x0127],  # BGE [inst addr (I)] [rs1] [rs2]
    "B>=" : [0x1D,0x0127],  # B>= [inst addr (I)] [rs1] [rs2]
    "B<=" : [0x1D,0x1027],  # B<= [inst addr (I)] [rs1] [rs2]
    "f14" : [0x0E,0x0001],  # f14 [rd]
    "f15" : [0x0F,0x0001],  # f15 [rd]
}

# ST [data source] [RAM address] [offset (I)]
# LD [rd] [RAM address] [offset (I)]

# operation format:
# (loc. of operand 2)(loc op1)(loc op0)(existence of operands)


registers = {
    "r0" : 0x00,
    "r1" : 0x01,
    "r2" : 0x02,
    "r3" : 0x03,
    "r4" : 0x04,
    "r5" : 0x05,
    "r6" : 0x06,
    "r7" : 0x07,
    "r8" : 0x08,
    "r9" : 0x09,
    "r10" : 0x0A,
    "r11" : 0x0B,
    "r12" : 0x0C,
    "r13" : 0x0D,
    "r14" : 0x0E,
    "r15" : 0x0F,
    "r16" : 0x10,
    "r17" : 0x11,
    "r18" : 0x12,
    "r19" : 0x13,
    "r20" : 0x14,
    "r21" : 0x15,
    "r22" : 0x16,
    "r23" : 0x17,
    "r24" : 0x18,
    "r25" : 0x19,
    "r26" : 0x1A,
    "r27" : 0x1B,
    "r28" : 0x1C,
    "r29" : 0x1D,
    "r30" : 0x1E,
    "r31" : 0x1F,

    "0"   : 0x00,
    "PC"  : 0x01,
    "MAR"  : 0x02,
    "MBR"  : 0x03

}


def enc(op,func,imm,r0,r1,r2):
	r2 = r2 << 16
	r1 = r1 << 11
	r0 = r0 << 6
	imm = imm << 5
	func = func << 4
	op = op << 0
	return (hex(op+func+imm+r0+r1+r2))
	
def dec(inst):
	r2 = (inst >> 16) & 0x3FFF
	r1 = (inst >> 11) & 0x1F
	r0 = (inst >> 6) & 0x1F
	imm = (inst >> 5) & 0x1
	func = (inst >> 4) & 0x1
	op = (inst >> 0) & 0xF
	return (op,func,imm,r0,r1,r2)


def openFile(source_path):
    print("\nloading...")
    code = []
    try:
        with open(source_path, 'r', encoding='utf-8') as src:
            index = 0
            for line in src:
                code.append(line.split())
                code[index].insert(0,index)
                index = index + 1
        print(code)
        print("loaded...\n")
        return code
    
    except Exception as e:
        print(f'Error: {e}\n')


def saveFile(code, save_path):
    print("\nsaving...")
    try:
        with open(save_path, 'w', encoding='utf-8') as ret:
            for line in code:
                #del line[0]
                #ret.write((hex(line[0]))+"\n")
                ret.write(line+"\n")
        print(f'Saved to {save_path}\n')

    except Exception as e:
        print(f'Error: {e}\n')



def compileCode(code):
    print("\nprocessing...")
    
    mcode = []              # compiled code will be stored here
    index = 0
    labels = {}

    for line in code:               # filtering actual instuctions

        if (len(line) == 1):                # filtering blanks
            continue
        elif (line[1][-1] == ":"):              # filtering labels
            labels[line[1][:-1]] = index
            code[line[0]] = []
        else:                               # actual instructions
            temp = [0,0]
            temp[0] = index
            temp[1] = line[1:]
            mcode.append(temp)
            index += 1
    
    code = mcode
    mcode = []

    for line in code:
        print(line)
        opcode = opcodes[line[1][0]][0]
        form = opcodes[line[1][0]][1]
        operand = [0,0,0]
        immediateFlag = 0
        for i in range(3):
            if (form & (1 << i)):
                tempForm = (form >> ((i + 1) * 4)) & 0xF
                tempOperand = line[1][1+i]
                    
                if (tempOperand in registers):
                    tempOperand = registers[tempOperand]
                elif(tempOperand in labels):
                    tempOperand = labels[tempOperand]
                    immediateFlag += 1
                else:
                    try:
                        immvalue = int(tempOperand, base=0)
                        if (tempForm == 2):
                            tempOperand = immvalue
                            immediateFlag += 1
                        else:
                            print(f"Error: Inappropriate Operand: {tempOperand} cannot be number")
                    except:
                        print(f"Error: Inappropriate Operand: {tempOperand}")

                operand[tempForm] = tempOperand
        mcode.append(enc(opcode,0,immediateFlag,operand[0],operand[1],operand[2]))
        print(mcode[-1])
            
            
            
            
            
    print(mcode)
    print("labels:", labels)
    print("processed\n")
    return mcode






src_path = 'asm240228.txt'
ret_path = 'mc.txt'

code = openFile(src_path)
code = compileCode(code)
saveFile(code, ret_path)
