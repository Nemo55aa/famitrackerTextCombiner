debug = True

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
	f = open("./out.txt", "w")
	f.writelines(lines)
	f.close()

if __name__ == '__main__':
    main()