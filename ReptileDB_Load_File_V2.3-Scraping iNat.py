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

#"//a[contains(@href,'/species')]"
#driver.quit()


# In[4]:


Rptls = {}
attr = set()

file_name = "reptile_full_data_iNat_uniqueid_v2.json"

file = open(file_name, "r")
Rptls = json.load(file)
file.close()

for i, r1 in enumerate (Rptls.keys()):
    for r2 in Rptls[r1].keys():
            attr.add(r2)
    
print (attr)    


# In[105]:


dbName = set()
for i, r1 in enumerate(Rptls.keys()):
    if len(Rptls[r1]['inaturalist.org'] ) != 0:
        iNatRptls = {}
        
        #print (Rptls[r1]['inaturalist.org'])
        #driver.get(Rptls[r1]['inaturalist.org'])
        #driver.get('https://www.inaturalist.org/taxa/73584-Ablepharus-budaki')
        driver.get('https://www.inaturalist.org/taxa/32012-Abronia-graminea')
        #driver.get('https://www.inaturalist.org/taxa/32014-Abronia-fuscolabialis')
        #driver.get('https://www.inaturalist.org/taxa/32016-Abronia-fimbriata')
        
        Wiki = False
        
        #Locating if WikiPedia is Source           
        try:    
            srch_rslt = driver.find_elements(By.XPATH, "//*[@id='articles-tab']/div/div/div[1]/div/h2")
            print (srch_rslt[0].text)
            if srch_rslt[0].text =="Source: Wikipedia":
                Wiki = True
                #print (srch_rslt[0].text)
                a=srch_rslt[0].find_elements_by_xpath ("child::a")
                #print (a[0].get_attribute('href'))
                dbName.add('Wikipedia')
                iNatRptls['Wikipedia'] = a[0].get_attribute('href')
        except:
            temp=''
   
        #Locating Initial descrition           
        try:    
            if Wiki == True:
                srch_rslt = driver.find_elements(By.XPATH, "//*[@id='taxon_description']/div/p[2]")
                print (srch_rslt[0].text)
                print('\n')
                ##for row in srch_rslt[0].find_elements_by_xpath ("child::*"):
                ##print (row.text)
            #else:
                #srch_rslt = driver.find_elements(By.XPATH, "//*[@id='taxon_description']")
                #print (srch_rslt[0].text)
                #print('\n')
        except:
            temp=''    

            
        #Locating other attributes of Wikipedia
        try:    
            if Wiki == True:
                atrNameLst = driver.find_elements(By.XPATH, "//*[@id='taxon_description']/div/*[self::h2 or self::h3]")
                #atrNameLst.append (driver.find_elements(By.XPATH, "//*[@id='taxon_description']/div/h3"))
                #print("attribute count:{0}".format(len(atrNameLst)))
                
                for atr in atrNameLst:
                    atr_name = atr.find_elements_by_xpath("child::span")
                    try:
                        print (atr_name[1].text)                                 #Attribute Name
                    except:
                        print (atr_name[0].text)                                 #Attribute Name
                        
                    
                    
                    atr_value = atr.find_elements_by_xpath("following-sibling::*")
                    
                    #print(atr_value[0].tag_name)
                    if (atr_value[0].tag_name) == 'p':
                        print (atr_value[0].text)
                    
                    elif (atr_value[0].tag_name) == 'table':
                        temp=''


                        
                    elif (atr_value[1].tag_name) == 'div':   #first [0] element is style and next [1] is div
                        ref_text_lst = []
                        ref_list = atr_value[1].find_elements(By.XPATH, "div/ol/child::*")

                        #ref_list = driver.find_elements(By.XPATH, "//*[@id='taxon_description']/div/div[3]/div/ol/child::*")
                        
                        for ref in ref_list:
                            ref_text_lst.append(ref.text)
                        print(ref_text_lst)
                        
                    elif (atr_value[0].tag_name) == 'ul':
                        ext_text_lst = []
                        
                        ext_list = atr_value[0].find_elements(By.XPATH, "child::*")
                        #ext_list = driver.find_elements(By.XPATH, "//*[@id='taxon_description']/div/ul/child::*")
                        for ref in ext_list:
                            ext_text_lst.append(ref.text)
                        print(ext_text_lst)
                    print ('\n')
                
                
                
                #for atrId in range(len (atrNameLst)):
                 #   atrNameLst[atrId].find_elements_by_xpath("child::*")
                
                #//*[@id='taxon_description']/div/h2[atrId]/following-sibling::p[1]
                #//*[@id='taxon_description']/div/h2[7]/following-sibling::*/div/*/li[]
                
                
                
            #srch_rslt = driver.find_elements(By.XPATH, "//*[@id='taxon_description']/div/p[2]")
            #print (srch_rslt[0].text)
            #for row in srch_rslt[0].find_elements_by_xpath ("child::*"):
                #print (row.text)
        except:
            temp=''            
            
            
           #//*[@id="taxon_description"]/div/p
            
            
    if i >= 1:
        break


# In[ ]:





# j=0
# for i, r1 in enumerate (Rptls.keys()):
#     #print(i,int(Rptls[r1]['Id']))
#     if i < (int(Rptls[r1]['Id'])-j):
#         print(i,int(Rptls[r1]['Id']), j)
#         j = (int(Rptls[r1]['Id'])-j) -i
#         #j=j+1
#         #print (j)
#         #print ("Row count is {0} and id is{1}".format(i,(Rptls[r1]['Id']))
#     
# 

# In[ ]:





# In[ ]:


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


# In[ ]:


for i in range(11):
    j=4500+ (i*50)
    
    print (j)

