# =====================================================    
def get_instr_type(opcode):
    if opcode == '00000001':
        print("Arithmethic ADD.")
        return 1
    elif opcode == '00000010':
        print("Arithmethic SUB.")
        return 2
    elif opcode == '00000011':
        print("LOAD WORD")
        return 3
    elif opcode == '00000100':
        print("STORE WORD")
        return 4
    else:
        print("Unknown opcode type: "+str(opcode))
        return 0
    
def find_data(instruction, instructionType, pc):
    global arqRom
    if instructionType == 1 or instructionType == 2:
        parameters = arqRom.read(pc+24)
        print(parameters)
        pc = pc + 24
    return

def execute(instructionType, data):
    return

#=====================================================

registerV = [4]
#CPU SPECIFICATIONS
pc = 0
sp = 0
stackReg = []
opcode = 0x0000        
running = True
    
    
#Carrega arquivos de memória
arqMemory = open("memory.bin", 'wb+')
print("Arquivo de memória: "+arqMemory.name)
arqRom = open("rom.bin", 'r')
print("Arquivo de ROM: "+arqRom.name)
print("Carregou arquivos de memória com sucesso!")
arqRom.seek(0, 0)

while running:
	pc = arqRom.tell()
	opcode = (arqRom.read(8))
	print("Instr. read: "+str(opcode))
	print(pc)
	instructionType = get_instr_type(opcode)
    
	#find data of decoded opcode
	parameters = find_data(opcode, instructionType, pc)    
    
	#Halt on unknown opcode execution
	if instructionType == 0:
		running = False