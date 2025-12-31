import sys # for commandline arg
import os
import tkinter.messagebox as tkmbx
import tkinter.filedialog as tkfdlg

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
	if(0):	# 251231 to add commandline args
		numPatternOffset = int('11', 16)
	# (end 251231)

	if(0):
		# for future convinience 
		tkmbx.showinfo(title="Select file", message="Select first famitracker txt file")
		
		fTyp = [("Famitracker Text file", "*.txt")]
		iDir = os.path.abspath(os.path.dirname(__file__))
		file_name = tkfdlg.askopenfilename(filetypes=fTyp, initialdir=iDir)
		if(file_name == ''):
			tkmbx.showerror(message="file not selected!\nleaving...")
			return -1
		
	args = sys.argv
	if(3 != len(args)):
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
		return 0
	else:
		file_name = args[1]
		numPatternOffset = int(args[2], 16)
	
	if(0):	# 251231 to add commandline args
		f = open('./The Rabbit has Landed.txt', "r+")
	# (end 251231)

	try	:
		f = open(file_name, "r+")
	except UnboundLocalError as uble:
		print(uble.__str__)
		print("unable to open file")
		return -1
	
	lines = f.readlines()
	f.close()

	for idxNum in range(len(lines)):
		if("PATTERN" in lines[idxNum]):
			lines[idxNum] = offsetPTRNline(lines[idxNum], numPatternOffset)
		if("ORDER" in lines[idxNum] and (not ("ORDER" in lines[idxNum + 1]))):
			numStr = lines[idxNum].rstrip()[-2:]
			# ------ 追加分のORDERの行を作る ------
			tmpOrderList = []
			for addIdx in range(numPatternOffset - 1):
				tmpNum = int(numStr, 16) + addIdx + 1
				# ORDER 20 : 20 20 20 .... などをもとの文字列に対して置換をして作成する
				lineReplaced = lines[idxNum].rstrip().replace(numStr, '{:X}'.format(tmpNum)) + "\n"
				tmpOrderList.append(lineReplaced)
			# --- 後述のリスト挿入処理用に位置を保存しておく ---
			idxLastLineOfORDER = idxNum + 1
			
	# --- 作ったORDERの行をファイル書き込み用のリストへ挿入する ---
	if(True == debug):				
		print(tmpOrderList)
	
	lines[idxLastLineOfORDER:idxLastLineOfORDER] = tmpOrderList
	
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