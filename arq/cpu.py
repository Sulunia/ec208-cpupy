# === === === === === === === === === === === === === === === === === ==
def get_instr_type(opcode):
	if opcode == '00000001':
		print("\nArithmethic ADD.")
		return 1
	elif opcode == '00000010':
		print("\nArithmethic SUB.")
		return 2
	elif opcode == '00000011':
		print("\nLOAD WORD")
		return 3
	elif opcode == '00000100':
		print("\nSTORE WORD")
		return 4
	else :
		print("\nUnknown opcode type!")
		return 0

def find_data(instruction, instructionType, pc):
	global arqRom
	global arqMemory
	global registerV
	global parameters
	if instructionType != 0:
		parameters[0] = arqRom.read(8)
		pc = arqRom.tell()
		parameters[1] = arqRom.read(8)
		pc = arqRom.tell()
		parameters[2] = arqRom.read(8)
		pc = arqRom.tell()
		
		registerV[0] = loadword(parameters[1])
		registerV[1] = loadword(parameters[2])
		
		print("Data 1: "+str(int(registerV[0], 2)))
		print("Data 2: "+str(int(registerV[1], 2)))
	return

def loadword(addr):
	global arqMemory
	arqMemory.seek((int(addr, 2))*8)
	data = arqMemory.read(8)
	return data
	
def storeword(addr, data):
	global arqMemory
	arqMemory.seek(int(addr, 2)*8)
	arqMemory.write(data)
	return
	
def execute(instructionType):	
	global arqMemory
	global registerV
	global parameters
	if instructionType == 1:
		#linha do caralho que resolve TUDO
		registerV[2] = str('{0:08b}'.format(int(registerV[0], 2) + int(registerV[1], 2)))
		print("Resultado: "+str(int(registerV[2], 2)))
		storeword(parameters[0], registerV[2])
	elif instructionType == 2:
		registerV[2] = str('{0:08b}'.format(int(registerV[0], 2) - int(registerV[1], 2)))
		print("Resultado: "+str(int(registerV[2], 2)))
		storeword(parameters[0], registerV[2])
	elif instructionType == 3:
		registerV[2] = loadword(parameters[0])
	elif instructionType == 4:
		storeword(parameters[0], parameters[1])
	return

# === === === === === === === === === === === === === === === === === ==

registerV = {}# CPU SPECIFICATIONS
pc = 0
sp = 0
stackReg = {}
parameters = {}
opcode = 0x0000
running = True

# Carrega arquivos de memória
arqMemory = open("memory.bin", 'r+')
print("Arquivo de memória: " + arqMemory.name)
arqRom = open("rom.bin", 'r')
print("Arquivo de ROM: " + arqRom.name)
print("Carregou arquivos de memória com sucesso!")
arqRom.seek(0, 0)

while running:
	pc = arqRom.tell()
	opcode = (arqRom.read(8))
	#print("Instr. read: " + str(opcode))
	#print(pc)
	instructionType = get_instr_type(opcode)

	# find data of decoded opcode
	find_data(opcode, instructionType, pc)
	
	# execute decoded opcode with given arguments
	execute(instructionType)
	
	# Halt on unknown opcode execution
	if instructionType == 0:
		running = False