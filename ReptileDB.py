#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import time
#import pandas as pd
import json
import os
os.chdir('C:\Arvin\Personal\IIIT\MS\Lab Projects\IndicWiki\\files')


# In[2]:


driver = webdriver.Chrome(executable_path='C:/Arvin/Personal/IIIT/MS/chromedriver.exe')
#driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.get("https://reptile-database.reptarium.cz/")
driver.implicitly_wait(2)
driver.find_element(By.XPATH, "//input[contains(@type,'text')]").send_keys("a")
driver.find_element(By.XPATH, "//input[contains(@type,'submit')]").click()
pages= driver.find_elements(By.XPATH, "//a[contains(@href,'/species')]")

#"//a[contains(@href,'/species')]"
#driver.quit()


# In[ ]:


"""
Rptl_URL = {}
for i in range (len(pages)):
#for i in range (10):
    if i%1000==0:
        print(i)
    Rptl_URL[pages[i].text] = pages[i].get_attribute('href')

with open("URL.json", "w") as outfile:
    json.dump(Rptl_URL, outfile)    
outfile.close()    
"""


# In[4]:


Rptls_URL = {}
with open("URL.json") as urls:
    Rptls_URL = json.load(urls)
urls.close()

titles = []
urls = []
for key in Rptls_URL.keys():
    titles.append(key)
    urls.append(Rptls_URL[key])

print(len(urls))
print(len(titles))

error_log = open("log.txt","w")


# In[5]:


def fetch_dtl(URL):
    rpt_dic = {}
    img_lst = []
    rpt_dic['URL'] = URL
    
    driver.get(URL)
    
    try:
        images = driver.find_elements(By.XPATH, "//div[@class = 'galleria-thumbnails-list']/div/div/img")
        for img in (images):
            img_lst.append(img.get_attribute('src'))
    except:
        log = "Image_1 Error: " + URL 
        error_log.write(log)
    
    try:
        images = driver.find_elements(By.XPATH, "//*[@id='inatwidgetmsg']/div/a[@class='inat-observation-image']/img")
        for img in (images):
            #print (img.get_attribute('src'))
            img_lst.append(img.get_attribute('src'))
    except:
        log = "Image_2 Error: " + URL
        error_log.write(log)
        
    rpt_dic['img'] = img_lst
        
    try:
        table = driver.find_elements(By.XPATH, "//*[@id='content']/table/tbody")
        # table[0] #table is list of web element with one element. cso taking first element
        
        for row in table[0].find_elements_by_xpath("child::*"):
            TData = row.find_elements_by_xpath("child::*")
            rpt_dic[TData[0].text] = TData[1].text
    except:
        log = "Table Error: " + URL
        error_log.write(log)
    
    return rpt_dic

    


# In[6]:


"""
Rptls_Data = {}

i=0
for rptl in Rptls_URL.keys():
    i = i+1
    if i%25 == 0:
        time.sleep(1)
    url_data = fetch_dtl(Rptls_URL[rptl])
    Rptls_Data[rptl] = url_data
        
"""
Rptls_Data = {}
#for i in range (1):
for i in range (4001, len(urls)):
    
    if i%500 == 0:
        error_log.close()
        error_log = open("log.txt","a")
        print("Last index is: {}, Last reptile is: {}".format(i, titles[i]))
        file_name = "reptile_" + str(i) + ".json"
        
        with open(file_name, "w") as outfile:
            json.dump(Rptls_Data, outfile)
        outfile.close()
        Rptls_Data = {}
    
    if i%25 == 0:
        time.sleep(1)
        
    title = titles[i]
    url = urls[i]
    url_data = fetch_dtl(url)
    Rptls_Data[title] = url_data
    
if i%500 != 0:
    file_name = "reptile_" + str(i) + ".json"
    with open(file_name, "w") as outfile:
        json.dump(Rptls_Data, outfile)
    outfile.close()

    
    


# In[12]:


#for i in Rptls_Data.keys():
#    print (i)


# In[14]:


Rptls = {}

#attr.add('URL')   #attr.add('img')

for i in range(24):
    j=i*500
    file_name = "reptile_" + str(j) + ".json"
    file = open(file_name, "r")
    rptl_batch = {}
    rptl_batch = json.load(file)
    file.close()
    
    for k1 in rptl_batch.keys():
        Rptls[k1] = rptl_batch[k1]
        for k2 in rptl_batch[k1].keys():
            attr.add(k2)
    
file_name = "reptile_11689.json"
file = open(file_name, "r")
rptl_batch = {}
rptl_batch = json.load(file)
file.close()
    
for k1 in rptl_batch.keys():
    Rptls[k1] = rptl_batch[k1]
    for k2 in rptl_batch[k1].keys():
        attr.add(k2)

file_name = "reptile_full_data.json"
with open(file_name, "w") as outfile:
    json.dump(Rptls, outfile)
outfile.close()        


# In[2]:


attr = set()

file_name = "reptile_full_data.json"
file = open(file_name, "r")

Rptls = json.load(file)
file.close()
    
for r1 in Rptls.keys():
    for r2 in Rptls[r1].keys():
            attr.add(r2)
print (attr)            


# In[3]:


import pandas as pd

AttrLst = ['Name', 'Common Names', 'Synonym', 'Higher Taxa', 'Types', 'Subspecies', 'Reproduction', 'Diagnosis','Distribution','Comment','Etymology','Image','References','URL','External links']
len(AttrLst)
df = pd.DataFrame(columns = AttrLst)

for r1 in Rptls.keys():
    row = {}
    row['Name'] = r1
    for atr in AttrLst[1:]:
        r2=atr
        if atr == 'Image':
            r2='img'
        
        try:
            value = Rptls[r1][r2]
        except:
            value = ''
        row[atr] = value
    df = df.append(row, ignore_index = True)
    #df = df.append(row)


# In[4]:


df
#df.to_csv('Reptiles.csv', index=False)


# In[22]:


for i, r1 in enumerate(Rptls.keys(), start=0):
    nmLst = []
    scName = r1
    scName = scName.split(',')[0]
    scName = scName.split(' (')[0]
    nmLst.append(scName)
    
    try:
        cNames = Rptls[r1]['Common Names']
        #print (cNames)
        cNameLst = cNames.split('\n')
        for j in range (len(cNameLst)):
            cNm = cNameLst[j]
            cNm = cNm.split('E: ')
            if len(cNm) > 1:
                nmLst.extend (cNm[1].split(','))
                for k in range (len(nmLst)):
                    nmLst[k] = nmLst[k].strip()
                #print (nmLst)
            #EngCmName
        print(len(tmp))
    except:
        temp = ''
        
    if i == 10:
        break
    
    

    
    
    
    


# In[16]:


a = '12345 ,dfs'
print (len(a.split(',')[0]))

