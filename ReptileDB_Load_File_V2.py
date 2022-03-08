#!/usr/bin/env python
# coding: utf-8

# In[18]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import time
#import pandas as pd
import json
import os
os.chdir('C:\Arvin\Personal\IIIT\MS\Lab Projects\IndicWiki\\files')


# In[19]:


driver = webdriver.Chrome(executable_path='C:/Arvin/Personal/IIIT/MS/chromedriver.exe')
#driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()

#"//a[contains(@href,'/species')]"
#driver.quit()


# In[20]:


attr = set()

file_name = "reptile_full_data_iNat.json"
file = open(file_name, "r")

Rptls = json.load(file)
file.close()
    
for r1 in Rptls.keys():
    for r2 in Rptls[r1].keys():
            attr.add(r2)
print (attr)            


# In[21]:


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


# In[23]:


df
#df.to_csv('Reptiles_iNat.csv', index=False)


# In[6]:


os.chdir('C:\Arvin\Personal\IIIT\MS\Lab Projects\IndicWiki\\files\\5000')
Rptls_iNat = {}


url_p0 = "https://www.inaturalist.org/"
url_p1 = "search?utf8=%E2%9C%93&q="
url_p3 = "&commit=Go"

for i, r1 in enumerate(Rptls.keys(), start=0):
    if i >=4500 and i<=5000:
        nmLst = []
        scName = r1
        scName = scName.split(',')[0]
        scName = scName.split(' (')[0]
    
        Rptls_iNat_dlt ={}
        Rptls_iNat_dlt = Rptls[r1]
    
        try:
            cNames = Rptls[r1]['Common Names']
            #print("Sarisarp number: {0}".format(i))
            #print ("Sarisarp Common names: {0}".format(cNames))
            cNameLst = cNames.split('\n')
            for j in range (len(cNameLst)):
                cNm = cNameLst[j]
                cNm = cNm.split('E: ')
                if len(cNm) > 1:
                    nmLst.extend (cNm[1].split(','))
        
        except:
            temp = ''

        nmLst.append(scName)
        #print ("Full Name List: {0}".format(nmLst))
    
    
        serchMatch=False
        for k in range (len(nmLst)):
            nmLst[k] = nmLst[k].strip()
        
            url_p2 = nmLst[k].replace("+", "%2B")
            url_p2 = url_p2.replace(" ", "+")
            url_p2 = url_p2.replace("$", "%24")
            url_p2 = url_p2.replace("&", "%26")
            url_p2 = url_p2.replace(",", "%2C")
            url_p2 = url_p2.replace("/", "%2F")
            url_p2 = url_p2.replace(":", "%3A")
            url_p2 = url_p2.replace(";", "%3B")
            url_p2 = url_p2.replace("=", "%3D")
            url_p2 = url_p2.replace("?", "%3F")
            url_p2 = url_p2.replace("@", "%40")        
        
            #print ("{}th formated Name is: {}".format(k,url_p2))    
        
            #Need to handle below items
            #1. No Result:    "desert arvin"
            #2. many Results: "Ablepharus budaki"
            #3. Many Results: "desert"
            #4. One Result Results: "Two-Streaked Snake-Eyed Skink"
        
            srch_url = url_p0+url_p1+url_p2+url_p3
        
            #Rptls_iNat_dlt['inaturalist.org']=''
            try:
                driver.get(srch_url)
                srch_rslt = driver.find_elements(By.XPATH, "//*[@id='wrapper']/div/div[2]/div/div[@class='media taxon-result']")
            
                if len(srch_rslt) == 1:
                    serchMatch = True
                    element = driver.find_element(By.XPATH, "//*[@id='wrapper']/div/div[2]/div/div/div[2]/h4/span[1]/span[1]/a")
                    url_srch_rslt = element.get_attribute('href')
                
                    Rptls_iNat_dlt['inaturalist.org'] = url_srch_rslt
                    Rptls_iNat [r1] = Rptls_iNat_dlt
                
                    break
            
            except:
                temp=''
            
            if serchMatch == False:
                Rptls_iNat_dlt['inaturalist.org'] = ''
                Rptls_iNat [r1] = Rptls_iNat_dlt
            
        #print('\n')
    
        if i%25 == 0:
            time.sleep(1)
        
        if i%50 == 0:
            print (i)
    
        #if i%500 == 0:
        if i%50 == 0:
            print("Last index is: {}, Last reptile is: {}".format(i, r1))
            file_name = "reptile_inatural" + str(i) + ".json"
        
            with open(file_name, "w") as outfile:
                json.dump(Rptls_iNat, outfile)
            outfile.close()
            Rptls_iNat = {}        
        
"""    
file_name = "reptile_full_data_iNat.json"
with open(file_name, "w") as outfile:
    json.dump(Rptls_iNat, outfile)
outfile.close() 
"""


# In[17]:


os.chdir('C:\Arvin\Personal\IIIT\MS\Lab Projects\IndicWiki\\files')
Rptls_iNat = {}

#attr.add('URL')   #attr.add('img')

file_name = "reptile_full_data_iNat.json"
file = open(file_name, "r")
rptl_batch = {}
rptl_batch = json.load(file)
file.close()
for k1 in rptl_batch.keys():
    Rptls_iNat[k1] = rptl_batch[k1]

os.chdir('C:\Arvin\Personal\IIIT\MS\Lab Projects\IndicWiki\\files\\5000')

#for i in range(24):
#    j=i*500
for i in range(11):
    j=4500+ (i*50)
    file_name = "reptile_inatural" + str(j) + ".json"
    file = open(file_name, "r", encoding="utf8")
    rptl_batch = {}
    #print(file_name)
    try:
        rptl_batch = json.load(file)
    except:
        print (file_name)
    file.close()
    
    for k1 in rptl_batch.keys():
        Rptls_iNat[k1] = rptl_batch[k1]
        
"""    
file_name = "reptile_inatural11687.json"
file = open(file_name, "r")
rptl_batch = {}
rptl_batch = json.load(file)
file.close()
    
for k1 in rptl_batch.keys():
    Rptls_iNat[k1] = rptl_batch[k1]
"""    

file_name = "reptile_full_data_iNat.json"
with open(file_name, "w") as outfile:
    json.dump(Rptls_iNat, outfile)
outfile.close()        


# In[ ]:


print("Last index is: {}, Last reptile is: {}".format(i, r1))
file_name = "reptile_inatural" + str(i) + ".json"

with open(file_name, "w") as outfile:
    json.dump(Rptls_iNat, outfile)
    outfile.close()
    #Rptls_iNat = {}


# In[ ]:


for r1 in Rptls_iNat.keys():
    print (r1)
    print (Rptls_iNat[r1]['inaturalist.org'])


# In[13]:


for i in range(11):
    j=4500+ (i*50)
    
    print (j)

