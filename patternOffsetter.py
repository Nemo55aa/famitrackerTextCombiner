import sys # for commandline arg
import os

# --- source configurations ---
debug = False
bRunAsGUI:bool = False	# set as True you wanna use this script from another script
class pattenOffsetter:
	#private:
	__strPathToFileOffset 	:str	= ''	# Put path of famitracker exported textfile that you wanna offset "PATTERN"s and "ORDER"s
	__iNumToOffset 			:int	= 0
	#public:
	def __init__(self):
		pass

	def setPath(self, str:str):
		self.__strPathToFileOffset = str

	def setOffset(self, num:int):
		self.__iNumToOffset = num
		
	def offsetPTRNlines(self, offset:int, lines:list[str]) -> str:
		tmpNumPattern :int = 0
		
		for idx in range(len(lines)):
			if("PATTERN" in lines[idx]):
				tmpNumPattern = int(lines[idx].rstrip()[-2:], 16)
				tmpNumPattern += offset
				lines[idx] = "PATTERN " + '{:X}'.format(tmpNumPattern) + "\n"
				
	# // ========================
	# // insertORDERlines 
	# // Add "ORDER" sentenses that we offsetted
	# // args:
	# // 	offset:
	# // 		amount of offsetted
	# // 	strLines:
	# // 		Please provide a list of strings obtained by f.readlines from a Famitracker file.
	# // return:
	# // 	list of str that ORDER sentense appended
	# // ========================
	def insertORDERlines(self, offset:int, strLines:list[str]) -> list[str]:
		idxLastLineOfORDER:int = 0	# last row of "ORDER" line
		tmpOrderList:list[str] = []	# list of "ORDER" strings to we going to add
		if(len(strLines) <= 0):
			return ["error", ]
		else:	
			# 行毎に処理を行う
			for idxNum in range(len(strLines)):
				# ORDER文の最終行であるかチェック
				if("ORDER" in strLines[idxNum] and (not ("ORDER" in strLines[idxNum + 1]))):
					numStr = strLines[idxNum].rstrip()[-2:]
					# ------ 追加分のORDERの行を作る ------
					for addIdx in range(offset):
						tmpNum = int(numStr, 16) + addIdx + 1
						# もとの文字列の16進数を置換をして追加分の行の文字列を作成する
						lineReplaced = strLines[idxNum].rstrip().replace(numStr, '{:X}'.format(tmpNum)) + "\n"
						tmpOrderList.append(lineReplaced)
					# --- 後述のリスト挿入処理用に位置を保存しておく ---
					idxLastLineOfORDER = idxNum + 1

			# --- 作ったORDERの行をファイル書き込み用のリストへ挿入する ---
			strLines[idxLastLineOfORDER:idxLastLineOfORDER] = tmpOrderList
			return strLines
		
	def doAll(self):
		try	:
			f = open(self.__strPathToFileOffset, "r+")
		except Exception as e:
			print("unable to open file")
			print(e.__str__)
			return -1
		
		lines = f.readlines()
		f.close()

		# ==== pattern offsetting ====
		self.offsetPTRNlines(self.__iNumToOffset, lines)

		# ==== add "ORDER" lines because we offsetted "PATTERN"s ====
		lines = self.insertORDERlines(self.__iNumToOffset, lines)

		# ==== save result into out*.txt ====
		for i in range(255):
			tmpPathToWrite = "./out" + str(i) + ".txt"
			if(os.path.isfile(tmpPathToWrite)):
				continue
			else:
				f = open(tmpPathToWrite, "w")
				f.writelines(lines)
				f.close()
				print("change is written to" + tmpPathToWrite)
				return
		print("There are too many result file on output dir!")

def printCmdUsage():
	print("usage:")
	print("\tpatternOffsetter [txt that youwanna of set] [number of offset]")
	
	print("\tpatternOffsetter:")
	print("\t\tthis command is for textfile exported by famitracker")
	print("\t\tand this is useful when you wanna combine two separately composed track")
	
	print("\t[txt that youwanna of set]:")
	print("\t\tenter text file's path that you wanna offset PATTERN and ORDER field")
	
	print("\t[number of offset]:")
	print("\t\tenter number that you wanna offset")
	print("\t\tNOTE: Please enter Number as Hexadecimal")

def main():
	offsetter = pattenOffsetter()
	args = sys.argv
	if(3 != len(args)):
		printCmdUsage()
		return 0
	else:
		offsetter.setPath(args[1])
		offsetter.setOffset(int(args[2], 16))
	
	offsetter.doAll()

if __name__ == '__main__':
    main()