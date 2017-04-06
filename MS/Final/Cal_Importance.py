import xlrd
import math
import json

dat = xlrd.open_workbook('data.xlsx').sheet_by_name('Main dataset')
aut_count = xlrd.open_workbook('data.xlsx').sheet_by_name('HelperSheet-AuthorSplit')

num_citations = {}
link_list = []
node_list = []
y = [0] * (2015-1990+1)
aut_rank = {}
year_list = {}
for i in range(1990,2016):
    year_list[i] = []
final = {}
final['nodes'] = []
final['links'] = []
for i in range(1990,2016):
    final[i] = []

for rownum in range(1,dat.nrows):
    paper = dat.cell(rownum, 16).value 
    if not isinstance(paper,float):
        paper = str(paper)
    else:
        paper = str(int(paper))
    cit = dat.cell(rownum, 18).value 
    cit_year = int(dat.cell(rownum, 1).value) #year of publication
    if not isinstance(cit,float):
        cit_split = cit.split(';')
        for i in range(len(cit_split)):
            cit_split[i] = str(cit_split[i])
            link_list.append((paper,cit_split[i])) 
            if cit_split[i] in num_citations:
                cnt = num_citations[cit_split[i]][0]
                yr = int(num_citations[cit_split[i]][1])
                if cit_year>yr:
                    num_citations[cit_split[i]] = (cnt+1,cit_year)
                else:
                    num_citations[cit_split[i]] = (cnt+1,yr)
            else:
                num_citations[cit_split[i]] = (1, cit_year)
    else:
        cit = str(int(cit))
        link_list.append((paper,cit)) 
        if cit in num_citations:
            cnt = num_citations[cit][0]
            yr = int(num_citations[cit][1])
            if cit_year>yr:
                num_citations[cit] = (cnt+1,cit_year)
            else:
                num_citations[cit] = (cnt+1,yr)
        else:
            num_citations[cit] = (1, cit_year)

for rownum in range(1,dat.nrows):
    num = dat.cell(rownum, 16).value
    keywords = dat.cell(rownum, 15).value
    keyword = keywords.split(',')
    authors = unicode(dat.cell(rownum,13).value).encode("utf-8")
    abstract = unicode(dat.cell(rownum,9).value).encode("utf-8")
    paper_type = str(dat.cell(rownum,8))
    link = str(dat.cell(rownum,4).value)
    title = str(dat.cell(rownum,2).value)
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
        num = str(num)
        if num in num_citations:
            citations = num_citations[num][0]
            cit_yr = num_citations[num][1]
        else:
            #decide this criteria
            citations = 0
            cit_yr = year
        importance = (citations+1) * math.exp(-(2017-year)*(2017-year)/(10*(cit_yr-year+1)))
        node_list.append([num,int(year),int(citations),cit_yr, title, color, importance, 0, y[int(year-1990)],str(keywords),authors,abstract,link,paper_type])
        if str(keyword[0])=='':
            year_list[int(year)].append([num,1, num, title])
        else:
            year_list[int(year)].append([num,1, str(keyword[0]),title])  #atleast one count to each paper

for rownum in range(1,dat.nrows):
    paper = dat.cell(rownum, 16).value 
    if not isinstance(paper,float):
        paper = str(paper)
    else:
        paper = str(int(paper))
    if paper != "-1":
        year = int(dat.cell(rownum, 1).value)
        count = 0
        cit = dat.cell(rownum, 18).value
        cit_year = int(dat.cell(rownum, 1).value)
        if not isinstance(cit,float):
            cit_split = cit.split(';')
            for i in range(len(cit_split)):
                cit_split[i] = str(cit_split[i])
                if cit_split[i] in [t[0] for t in year_list[year]]:
                    count = count + 2
        else:
            cit = str(int(cit))
            if cit in [t[0] for t in year_list[year]]:
                count = 2
        index = [t[0] for t in year_list[year]].index(paper)
        year_list[year][index][1] = year_list[year][index][1]+count

for rownum in range(1,dat.nrows):
    paper = dat.cell(rownum, 16).value 
    if not isinstance(paper,float):
        paper = str(paper)
    else:
        paper = str(int(paper))
    if paper != "-1":
        authors = dat.cell(rownum,13).value
        aut_split = authors.split(';')
        ind = [t[0] for t in node_list].index(paper)
        for it in range(len(aut_split)):
            name = unicode(aut_split[it]).encode("utf-8") 
            if name in aut_rank:
                aut_rank[name] = aut_rank[name] + node_list[ind][6]
            else:
                aut_rank[name] = node_list[ind][6] 
for rownum in range(1,dat.nrows):
    paper = dat.cell(rownum, 16).value 
    if not isinstance(paper,float):
        paper = str(paper)
    else:
        paper = str(int(paper))
    if paper != "-1":
        authors = dat.cell(rownum,13).value
        aut_split = authors.split(';')
        ind = [t[0] for t in node_list].index(paper)
        pre_rank = node_list[ind][7]
        for it in range(len(aut_split)):
            name = unicode(aut_split[it]).encode("utf-8") 
            if pre_rank < aut_rank[name]:
                pre_rank = aut_rank[name]
        node_list[ind][7] = pre_rank

#print node_list
#print link_list
#print year_list
#print aut_rank
#print min([t[7] for t in node_list])

for it in range(len(node_list)):
    final['nodes'].append({'name':node_list[it][0], 'x':(node_list[it][1]-1989), 'y':node_list[it][6], 'title':node_list[it][4], 'color':node_list[it][5], 'size':node_list[it][2], 'author':node_list[it][7], 'y_pos':node_list[it][8], 'keywords':node_list[it][9], 'authors':node_list[it][10], 'abstract':node_list[it][11],'link':node_list[it][12],'paper_type':node_list[it][13]})

for it in range(len(link_list)):
    if link_list[it][1] in [t[0] for t in node_list]:
        source_index = [t[0] for t in node_list].index(link_list[it][0])
        target_index = [t[0] for t in node_list].index(link_list[it][1])
        final['links'].append({'source':source_index, 'target':target_index, 'sourceName':link_list[it][0], 'targetName':link_list[it][1], 'sourceSize':node_list[source_index][2], 'targetSize':node_list[target_index][2]})

for i in range(1990,2016):
    for it in range(len(year_list[i])):
        final[i].append(year_list[i][it])

with open('data_format.json', 'w') as outfile:
    json.dump(final, outfile, ensure_ascii=False)
