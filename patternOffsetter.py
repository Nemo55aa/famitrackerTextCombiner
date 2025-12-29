import sys

def main():
	numPatternOffset = int('11', 16)
	f = open('./The Rabbit has Landed.txt', "r+")
	lines = f.readlines()
	f.close()

	for idxNum in range(len(lines)):
		if("PATTERN" in lines[idxNum]):
			tmpNumPattern :int = 0
			print(lines[idxNum].rstrip())
			print(lines[idxNum].rstrip()[-2:])
			print(int(lines[idxNum].rstrip()[-2:], 16))
			tmpNumPattern = int(lines[idxNum].rstrip()[-2:], 16)
			tmpNumPattern += numPatternOffset
			print("PATTERN " + '{:X}'.format(tmpNumPattern))
			lines[idxNum] = "PATTERN " + '{:X}'.format(tmpNumPattern) + "\r\n"
	
	f = open("./out.txt", "w")
	f.writelines(lines)
	f.close()

if __name__ == '__main__':
    main()