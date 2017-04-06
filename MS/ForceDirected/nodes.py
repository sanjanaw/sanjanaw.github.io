import xlrd

sh = xlrd.open_workbook('nodes.xlsx').sheet_by_index(0)
english = open("nodes.txt", 'w')
try:
    for rownum in range(sh.nrows):
        english.write("{\"id\" : \"" +str(sh.cell(rownum, 0).value)+"\", \"group\": 1},\n")
finally:
    english.close()
