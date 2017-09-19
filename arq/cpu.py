# === === === === === === === === === === === === === === === === === ==
def get_instr_type(opcode):
	#Recebe um opcode do "rom.bin" e o decodifica apropriadamente
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
		print("\nOpcode desconhecido! Encerrando...")
		return 0

def find_data(instruction, instructionType, pc):
	#define as variáveis abaixo como variáveis globais
	global arqRom
	global arqMemory
	global registerV
	global parameters
	
	#Busca no "rom.bin" os parâmetros do opcode recebido previamente
	if instructionType != 0:
		parameters[0] = arqRom.read(8)
		pc = arqRom.tell()
		parameters[1] = arqRom.read(8)
		pc = arqRom.tell()
		parameters[2] = arqRom.read(8)
		pc = arqRom.tell()
		
		#transfere os parametros lidos para os registradores
		registerV[0] = loadword(parameters[1])
		registerV[1] = loadword(parameters[2])
		
		print("Data 1: "+str(int(registerV[0], 2)))
		print("Data 2: "+str(int(registerV[1], 2)))
	return

def loadword(addr):
	global arqMemory
	
	#Busca dados na memória, no caso, "memory.bin"
	arqMemory.seek((int(addr, 2))*8)
	data = arqMemory.read(8)
	return data
	
def storeword(addr, data):
	global arqMemory
	
	#Salva dados na memória, no caso, "memory.bin"
	arqMemory.seek(int(addr, 2)*8)
	arqMemory.write(data)
	return
	
def execute(instructionType):	
	global arqMemory
	global registerV
	global parameters
	
	#Função que contém o interpretador da CPU
	if instructionType == 1: #ADD
		#Um código parecido é usado para a função SUB.
		#A linha abaixo lê os dados dos registradores, converte-os para inteiros,
		#faz a soma, define a saída como um número binário de 8bits, e converte o resultado para String.
		registerV[2] = str('{0:08b}'.format(int(registerV[0], 2) + int(registerV[1], 2)))
		
		print("Resultado: "+str(int(registerV[2], 2)))
		storeword(parameters[0], registerV[2])
	
	elif instructionType == 2: #SUB
		#Mesma coisa do ADD, porém subtrai os dados.
		registerV[2] = str('{0:08b}'.format(int(registerV[0], 2) - int(registerV[1], 2)))
		print("Resultado: "+str(int(registerV[2], 2)))
		storeword(parameters[0], registerV[2])
	
	elif instructionType == 3: #LOAD
		registerV[2] = loadword(parameters[0])
	
	elif instructionType == 4: #STORE
		storeword(parameters[0], parameters[1])
	return

# === === === === === === === === === === === === === === === === === ==

registerV = {}# CPU SPECIFICATIONS
pc = 0
sp = 0
stackReg = {}
parameters = {}
opcode = 0x0000
running = True #bit de execução

# Carrega arquivos de memória
arqMemory = open("memory.bin", 'r+')
print("Arquivo de memória: " + arqMemory.name)
arqRom = open("rom.bin", 'r')
print("Arquivo de ROM: " + arqRom.name)
print("Carregou arquivos de memória com sucesso!")
arqRom.seek(0, 0)

while running:
	#define o PC para a posição na memória ROM
	pc = arqRom.tell()
	
	#Fetch
	opcode = (arqRom.read(8))
	
	#Decode
	instructionType = get_instr_type(opcode)

	find_data(opcode, instructionType, pc)
	
	#Execute
	execute(instructionType)
	
	#Interrompe execução ao ler um opcode inválido
	if instructionType == 0:
		running = False