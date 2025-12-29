debug = False

def offsetPTRNline(strLine:str, offset:int) -> str:
	tmpNumPattern :int = 0
	if(True == debug):
		print(strLine.rstrip())
		print(strLine.rstrip()[-2:])
		print(int(strLine.rstrip()[-2:], 16))
	tmpNumPattern = int(strLine.rstrip()[-2:], 16)
	tmpNumPattern += offset
	if(True == debug):
		print("PATTERN " + '{:X}'.format(tmpNumPattern))
	strLine = "PATTERN " + '{:X}'.format(tmpNumPattern) + "\r\n"
	return strLine

def main():
	numPatternOffset = int('11', 16)
	f = open('./The Rabbit has Landed.txt', "r+")
	lines = f.readlines()
	f.close()

	for idxNum in range(len(lines)):
		if("PATTERN" in lines[idxNum]):
			lines[idxNum] = offsetPTRNline(lines[idxNum], numPatternOffset)
	
	f = open("./out.txt", "w")
	f.writelines(lines)
	f.close()

if __name__ == '__main__':
    main()