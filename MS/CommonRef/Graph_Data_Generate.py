import xlrd
import random
import sets
import itertools
import json

dat = xlrd.open_workbook('data.xlsx').sheet_by_name('Main dataset')
final = {}
final['nodes'] = []
final['links'] = []

node_list = []
y = [0] * (2015-1990+1)
for rownum in range(1,dat.nrows):
    num = dat.cell(rownum, 16).value
    title = dat.cell(rownum,2).value
    year = dat.cell(rownum, 1).value
    if dat.cell(rownum, 0).value == "InfoVis":
        color = 'darkturquoise'
    elif dat.cell(rownum, 0).value == "SciVis":
        color = 'forestgreen'
    elif dat.cell(rownum, 0).value == "VAST":
        color = 'gold'
    else:
        color = 'orangered'
    y[int(year-1990)] += 5
    if num != -1:
        if isinstance(num,float):
            num = int(num)
        if not num in node_list:
           node_list.append((str(num), int(year), y[int(year-1990)], title, color))
for it in range(len(node_list)):
    final['nodes'].append({'name':node_list[it][0], 'x':(node_list[it][1]-1989)*50, 'y':node_list[it][2], 'title':node_list[it][3], 'color':node_list[it][4]})

dict_list = {}
for rownum in range(1,dat.nrows):
    num = dat.cell(rownum, 16).value
    if num == -1:
        continue
    if isinstance(num,float):
        num = int(num)
    list_ref = []
    if dat.cell_type(rownum, 18) == xlrd.XL_CELL_EMPTY:
	continue
    arr = dat.cell(rownum, 18).value
    if not isinstance(arr,float):
        arr_split = arr.split(';')
        for it in range(len(arr_split)):
            list_ref.append(str(arr_split[it]))
    else:
        list_ref.append(str(int(arr)))
    for it in range(len(list_ref)):
        if list_ref[it] in (t[0] for t in node_list):
	    if list_ref[it] in dict_list:
		dict_list[list_ref[it]].append(str(num))
	    else:
		dict_list[list_ref[it]] = []
	        dict_list[list_ref[it]].append(str(num)) #dict list created with common reference as keys
link_list = sets.Set(())
for it,arr in dict_list.iteritems():
    arr.sort()
    temp = list(itertools.combinations(arr,2))
    for i in range(len(temp)):
        link_list.add(temp[i])     #added only once (because sorted!) and get weights also!
for it in range(len(link_list)):
    temp = link_list.pop()
    final['links'].append({'source':[t[0] for t in node_list].index(temp[0]), 'target':[t[0] for t in node_list].index(temp[1])})

with open('data_format.json', 'w') as outfile:
    json.dump(final, outfile, ensure_ascii=False)
