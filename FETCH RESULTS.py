import requests
import re
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame, Series
branch = input('Enter the name of the branch -->')
init = int(input('Enter the starting Roll Number of the branch -->'))
final = int(input('Enter the ending Roll Number of  the branch -->'))
rn = []
cgpa,name0,sgpa = [],[], []
for i in range(init, final+1):
    rn.append(str(i))
#print(rn)
serviceurl = 'http://59.144.74.15/scheme18/studentResult/details.asp'
count=0
found_rn = []
end=0
item=init
while item<=final:
    if end>=5:
        rt=1+(item//1000)
        rt*=1000
        rt+=1
        item=rt
        end=0
    if item>final:
        break
    count+=1
    ss = str(item)
    
    try:
        payload = {'RollNumber': item, 'B1': 'Submit'}
        data = requests.post(serviceurl, data=payload)
        data = data.text
        get = re.match(str(ss), data)
        if get==False:
        	continue
        #print(get)
        soup = BeautifulSoup(data, 'html.parser')
        name = soup.find('table', class_='ewTable').find('td', class_='auto-style5', style='width: 256px; height: 22px;').text.strip()
        #print(name)
        soup = soup.prettify()
        found_rn.append(item)
        GPA = re.findall('=([0-9,.]+)', soup)
        #print(GPA)
        if len(GPA)<2:
            continue
        CGPA = (GPA[len(GPA)-1])
        SGPA = (GPA[len(GPA)-2])
	#print(ls)
	#print(name)
        cgpa.append(CGPA)
        sgpa.append(SGPA)
        name0.append(name)
        #print(item, name, GPA)
        print('Retrieving file {0}    Roll Number = {1}'.format(count, item))
    except:
        end=end+1
        count=count-1
        pass
    item += 1
count=0
name=name0
##for item in FINAL_RESULT:
##    count+=1
##    print('RANK {}'.format(count), end=' --> ')
##    print(item[0], item[2], item[1])

print()
print()
#print(len(found_rn))
#print(len(cgpa))
#print(len(sgpa))
#print(len(name))
df = DataFrame({'Roll Number' : found_rn, 'Name': name, 'SGPA': sgpa, 'CGPA': cgpa})
df = df.sort_values(by='CGPA', ascending=False)
new_index = np.arange(1, len(name)+1)
df['RANK'] = new_index
df.set_index(['RANK'], inplace=True)
print(df)
df.to_csv('/home/abhishek/Desktop/CSE(2018-2022)Result.csv')






