import pandas as pd
import pprint
import json
import sqlite3

data = pd.read_excel(io ='D:\Project\Python\\testrasp2.xlsx', sheet_name='ПЕ-01,02б')

#print(data.columns)
pe = data[['дни', '№ пары', 'ПЕ-01б', 'ауд.']]



h = 0
treu = pe['ауд.'].isnull()
#print(pe['ауд.'].isnull())
for пара in treu:
    #print(пара.isnull())
    if пара:
        pe['ауд.'][h] = data['ауд..1'][h]
    h = h+ 1

#print(pe)

парыслияние = pe[pe['№ пары'].isnull()].index


for sl in парыслияние:
    pe['ПЕ-01б'][sl-1] = str(pe['ПЕ-01б'][sl-1]) +'; '+ str(data['ПЕ-01б'][sl])
    pe['ауд.'][sl-1] = str(pe['ауд.'][sl-1]) +', '+ str(data['ауд.'][sl])

pe.drop(labels = парыслияние ,axis = 0,  inplace=True)

pe = pe.reset_index(drop=True)
#print(pe)

daysTarget= ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']

days = pe['дни'].value_counts().index


indexDays =[]
for day in days:
    indexDays.append(pe[pe['дни'] == day].index)

dictDays = {}


start = indexDays[0][0]
indexDays.append(pd.Int64Index([31], dtype='int64'))#автоматизировать
for i in indexDays[1:]:
    i = i[0]
    day = pe.iloc[start:i]
    #print(day)
    dayname = day['дни'].head(1).values[0]
    #print(dayname)
    dictDays[dayname] = {}
    dayValues = day[['№ пары', "ПЕ-01б", "ауд."]].reset_index(drop=True)
    #print(dayname, dayValues,dayValues.index, '\n\n')

    for j in dayValues.index:
        massvalue = dayValues.iloc[j]
        #print(massvalue)
        numPar = massvalue['№ пары']
        pred = massvalue['ПЕ-01б']
        if type(pred) == float:
            pred = "None"
        kab = massvalue['ауд.']
        if type(kab) == float:
            kab = "None"
        dictDays[dayname][numPar] = [pred, kab]

    start = i


with open('testrasppp.json', 'w+') as outfile:
    json.dump(dictDays, outfile, ensure_ascii=False)