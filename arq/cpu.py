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
		print("Preparando-se para ler dados no endereço do primeiro argumento...")
		registerV[0] = loadword(parameters[1])
		print("Preparando-se para ler dados no endereço do segundo argumento...")
		registerV[1] = loadword(parameters[2])

		print("Data 1: "+str(int(registerV[0], 2)))
		print("Data 2: "+str(int(registerV[1], 2)))
	return

def loadword(addr):
	global arqMemory
	#Verifica a disponibilidade dos dados na memória cacheHit
	data = cacheVerification(addr, True)
	return data

def storeword(addr, data):
	global arqMemory

	result = cacheVerification(addr, False)
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
		print("")
		print("Preparando-se para salvar resultado da conta na memória...")
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

def validateCache(blockNumber, calcTag, calcPos):
# Verifica se o dado na cache eh valido
	result = -1
	print("")
	print("=======================")
	print("Cache validation start")
	print("Parameters: blockNumber = "+str(blockNumber)+" calcTag = "+str(calcTag)+" calcPos = "+str(calcPos))
	print("Is valid at blocknumber position: "+str(cacheValidity[blockNumber]))
	print("Tag at blockNumber position: "+str(cacheTag[blockNumber]))

	if(int(cacheTag[blockNumber], 2) == calcTag):
		if(cacheValidity[blockNumber] == True):
			result = int(cacheData[blockNumber], 2)
			print("Whole cache block value: "+str('{0:032b}'.format(result)))
			print("Bitwise check: "+str(calcPos))
			if calcPos == 0:
				result = result & 0b11111111000000000000000000000000
			elif calcPos == 1:
				result = result & 0b00000000111111110000000000000000
			elif calcPos == 2:
				result = result & 0b00000000000000001111111100000000
			else:
				result = result & 0b00000000000000000000000011111111
			print("Post process data result: "+str('{0:032b}'.format(result)))
			result = result >> 8 * (3 - calcPos)
			print("Post bitwise shift result: "+str('{0:032b}'.format(result)))
			result = str('{0:08b}'.format(result))
	print("=======================")
	print("")
	return result


def cacheVerification(addr, bool):
	global arqMemory
	trueAddr = int(addr, 2)
	blockNumber = trueAddr%4
	calcTag = trueAddr>>4
	calcPos = trueAddr & 0b00000011
	valor = validateCache(blockNumber, calcTag, calcPos)
	if(bool==False):
		print("Verificando se precisa anular validade de dados na cache...")

	print("Value returned from initial validation: "+str(valor))
	if((valor == -1) and bool):
		print("Cache miss! Buscando da memória..")
		#Traz dados da memória secundária para a cache
		addressBring = trueAddr%4
		memoryPos = arqMemory.tell()
		arqMemory.seek(0, (trueAddr-addressBring)*8)

		data = arqMemory.read(32)
		cacheData[blockNumber] = data
		cacheValidity[blockNumber] = True
		cacheTag[blockNumber] = str('{0:04b}'.format(calcTag))
		valor = validateCache(blockNumber, calcTag, calcPos)
		print("Valor novo após busca de dados na memória: "+str(valor))
		if(valor == -1):
			print("Há algo errado!")
		else:
			print("Busca na memória secundária concluída com sucesso!")
	elif((valor != -1) and (bool == False)):
		cacheValidity[blockNumber] = False
		print("Informações no bloco "+str(blockNumber)+" invalidadas!")
		print("")
	elif(valor != -1):
		print("Cache hit!")
	return valor


# === === === === === === === === === === === === === === === === === ==

registerV = {}# CPU SPECIFICATIONS
pc = 0
sp = 0
stackReg = {}
parameters = {}
opcode = 0x0000
cacheData = {}
cacheTag = {}
cacheSpec = {}
cacheHit = False
cacheValidity = {}
running = True #bit de execução

for i in range(0, 4):
	cacheData[i] = "00000000000000000000000000000000"
	cacheTag[i] = "0000"
	cacheSpec[i] = "00"
	cacheValidity[i] = False

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
	print("PC: "+(str)(pc))

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
