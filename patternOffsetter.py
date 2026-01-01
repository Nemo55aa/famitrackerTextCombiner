import sys # for commandline arg
import os
import tkinter.messagebox as tkmsgbox
import tkinter.filedialog as tkfdlg

# --- source configurations ---
debug = False

# --- [IN] ---
bCallFromWindow:bool = False	# set as True you wanna use this script from another script
strPathToFileOffset	= ''		# Put path of famitracker exported textfile that you wanna offset "PATTERN"s and "ORDER"s

# --- [OUT] ---
# none (This file gonna spits just "out*.txt")

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
	strLine = "PATTERN " + '{:X}'.format(tmpNumPattern) + "\n"
	return strLine

# // ========================
# // insertORDERlines 
# // Add "ORDER" sentenses that we offsetted
# // args:
# // 	offset:
# // 		amount of offsetted
# // 	strLines:
# // 		Please provide a list of strings obtained by f.readlines from a Famitracker file.
# // return:
# // 	ORDER文が追記(挿入)された文字列のリストを返します
# // ========================
def insertORDERlines(offset:int, strLines:list[str]) -> list[str]:
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
	
def printCmdUsage(void):
	if(False == bCallFromWindow):
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
	if(False == bCallFromWindow):
		# if executed from commandline
		args = sys.argv
		if(3 != len(args)):
			printCmdUsage()
			return 0
		else:
			strPathToFileOffset = args[1]
			numPatternOffset = int(args[2], 16)

	try	:
		f = open(strPathToFileOffset, "r+")
	except Exception as e:
		print("unable to open file")
		print(e.__str__)
		return -1
	
	lines = f.readlines()
	f.close()

	# ==== pattern offsetting ====
	for idxNum in range(len(lines)):
		if("PATTERN" in lines[idxNum]):
			lines[idxNum] = offsetPTRNline(lines[idxNum], numPatternOffset)

	# ==== add "ORDER" lines because we offsetted "PATTERN"s ====
	lines = insertORDERlines(numPatternOffset, lines)

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
			break

if __name__ == '__main__':
    main()