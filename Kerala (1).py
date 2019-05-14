
# coding: utf-8

# In[4]:


#importing libraries
import csv
import re
import requests
from bs4 import BeautifulSoup


# In[5]:


#scraping data from thrissurkerala.com for MLA
URL = 'http://www.thrissurkerala.com/mp-mla-kerala/kerala-mlas-phone-numbers-email-address.html'
r = requests.get(URL)
soup = BeautifulSoup(r.content)
output_rows = []
table = soup.find('table',width = '800',border = '1')
for table_row in table.findAll('tr'):
    columns = table_row.findAll('td')
    output_row = []
    for column in columns:
        #print(column.string)
        output_row.append(column.text)
    output_rows.append(output_row)
#exporting it to a temporary csv file to be read in Pandas   
with open('KeralaMLA.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_rows)


# In[6]:


import pandas as pd
#read the temporary file and remove redundent columns
f = pd.read_csv("KeralaMLA.csv",encoding="ISO-8859-1")
del f['Constituency']
del f['District']
f.columns = ["Name","Email","Phone Number"]
output_headers = f.columns.values.tolist()
output_rows =f.values.tolist()
output_rows.insert(0,output_headers)


# In[7]:


#Scrape www.thrissurKerala.com for MP data
URL = 'http://www.thrissurkerala.com/mp-mla-kerala/kerala-mps-phone-numbers-email-lok-sabha.html'
r = requests.get(URL)
soup = BeautifulSoup(r.content)
output= []
table = soup.find('table',width = '600',border = '0')
for table_row in table.findAll('tr'):
    for td in table_row.findAll('td',valign = "middle"):
        output.append(td.text)
        #print(td.text)


# In[8]:


#Remove redundent Characters
i=0 
length = len(output) 
while(i<length):
    if(output[i]==':' or output[i]=='\xa0'):
        output[i] = ' '
        continue
    i = i+1
    


# In[9]:


#Get Names email and phone from Vertical table using indices positions
get_indexes = lambda output, xs: [i for (y, i) in zip(xs, range(len(xs))) if output  == y]
indexes_names = (get_indexes("Constituency",output))
indexes_email = (get_indexes("Email",output))
indexes_phone = (get_indexes("Phone (Kerala) ",output))


# In[10]:


#Store each information in lists
names =[]
email = []
phone =[]
for i in indexes_names:
    names.append((output[i-1]))
for i in indexes_email:
    email.append((output[i+2]))
for i in indexes_phone:
    phone.append(output[i+2])


# In[11]:


#combine columns
rowsMP = zip(names,email,phone)


# In[12]:


#export to csv file
with open("Kerala.csv","w",newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_rows)
    for row in rowsMP:
        writer.writerow(row)


# In[16]:


#convert csv to excel
import os
import glob
import csv
from xlsxwriter.workbook import Workbook


for csvfile in glob.glob(os.path.join('Kerala.csv')):
    workbook = Workbook(csvfile[:-4] + '.xlsx')
    worksheet = workbook.add_worksheet()
    with open(csvfile, 'rt', encoding='ISO-8859-1') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    workbook.close()

