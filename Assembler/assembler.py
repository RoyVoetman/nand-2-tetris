outFile = open('out.hack', 'w')
 
inFile = open('pong/Pong.asm', 'r')
lines = inFile.readlines()

compLookupTable = {
    "0"  : "101010",
    "1"  : "111111",
    "-1" : "111010",
    "D"  : "001100",
    "A"  : "110000",
    "M"  : "110000",
    "!D" : "001101",
    "!A" : "110001",
    "!M" : "110001",
    "-D" : "001111",
    "-A" : "110011",
    "-M" : "110011",
    "D+1": "011111",
    "A+1": "110111",
    "M+1": "110111",
    "D-1": "001110",
    "A-1": "110010",
    "M-1": "110010",
    "D+A": "000010",
    "D+M": "000010",
    "D-A": "010011",
    "D-M": "010011",
    "A-D": "000111",
    "M-D": "000111",
    "D&A": "000000",
    "D&M": "000000",
    "D|A": "010101",
    "D|M": "010101"
}
 
jumpLookupTable = {
    ""   : "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

symbolTable = {
    "R0"    : 0,
    "SP"    : 0,
    "R1"    : 1,
    "LCL"   : 1,
    "R2"    : 2,
    "ARG"   : 2,
    "R3"    : 3,
    "THIS"  : 3,
    "R4"    : 4,
    "THAT"  : 4,
    "R5"    : 5,
    "R6"    : 6,
    "R7"    : 7,
    "R8"    : 8,
    "R9"    : 9,
    "R10"   : 10,
    "R11"   : 11,
    "R12"   : 12,
    "R13"   : 13,
    "R14"   : 14,
    "R15"   : 15,
    "SCREEN": 16384,
    "KBD"   : 24576
}

valueForNewSymbol = 16

def main():
    programCounter = 0

    for i in range(2):
        for line in lines:
            line = line.strip()

            # Remove code comments
            line = line.split('//')[0].strip()

            # Ignore whitespace
            if (line == ""):
                continue

            # First pass: resolve labels
            if i == 0:
                if line[0] == "(" and line[-1] == ")":
                    symbolTable[line[1:-1]] = programCounter
                else:
                    programCounter += 1
            
            # Second pass: parse instructions
            if i == 1:
                if line[0] == "(" and line[-1] == ")":
                    continue

                machineCode = ""

                if (line[0] == "@"):
                    machineCode += parseAInstruction(line)
                
                else:
                    machineCode += parseCInstruction(line)
                    
                outFile.writelines(machineCode + "\n")
        
    inFile.close()
    outFile.close()

def parseAInstruction(instruction):
    """
    A-instruction parser
    (e.g. @50)
    """
    # Remove "@" sign
    instruction = instruction[1:]

    # Symbol handeling
    if not instruction.isnumeric():
        if instruction in symbolTable:
            instruction = symbolTable[str(instruction)]

        # add new symbol
        else:
            global valueForNewSymbol
            symbolTable[str(instruction)] = valueForNewSymbol
            instruction = valueForNewSymbol
            valueForNewSymbol += 1

    return "0" + "{0:015b}".format(int(instruction))

def parseCInstruction(instruction):
    """
    C-instruction parser
    (e.g. dest = comp; jump)
    """
    dest = ""
    comp = ""
    jump = ""

    # Retrieve dest, comp, and jump segments
    segments = instruction.split('=')

    if (len(segments) == 2):
        dest = segments[0].strip()
        instruction = segments[1].strip()
    else:
        instruction = segments[0].strip()

    segments = instruction.split(';')

    comp = segments[0].strip()

    if (len(segments) == 2):
        jump = segments[1].strip()

    # Build machine code
    machineCode = "111"

    machineCode += "1" if comp.find("M") != -1 else "0"

    machineCode += compLookupTable[comp]

    machineCode += "1" if dest.find("A") != -1 else "0"
    machineCode += "1" if dest.find("D") != -1 else "0"
    machineCode += "1" if dest.find("M") != -1 else "0"

    machineCode += jumpLookupTable[jump]

    return machineCode

if __name__ == "__main__":
    main()
