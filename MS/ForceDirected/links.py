import xlrd

sh = xlrd.open_workbook('load.xlsx').sheet_by_index(0)
english = open("nodes.txt", 'w')
try:
    for rownum in range(sh.nrows):
	line = str(sh.cell(rownum, 18).value)
	if line:	
		if ';' in line:
			currentline = line.split(";");
			if currentline:
				for word in currentline:
					try:
					        english.write("{\"source\" : \"" +str(sh.cell(rownum, 16).value)+"\", \"target\": \"" +str(float(word)) + "\", \"value\":1},\n")
					except:
						english.write("{\"source\" : \"" +str(sh.cell(rownum, 16).value)+"\", \"target\": \"" +str(word) + "\", \"value\":1},\n")
		else:
			english.write("{\"source\" : \"" +str(sh.cell(rownum, 16).value)+"\", \"target\": \"" +str(line) + "\", \"value\":1},\n")

finally:
    english.close()
