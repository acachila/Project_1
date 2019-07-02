#!/usr/bin/env python
# coding: utf-8

# In[94]:


#Load Packages 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
pd.options.display.max_columns=None


# In[95]:


#Read all csvs 
df = pd.read_csv('C:\\Users\\btm9355\\Desktop\\opioid2013.csv')
df1 = pd.read_csv('C:\\Users\\btm9355\\Desktop\\opioid2014.csv')
df2 = pd.read_csv('C:\\Users\\btm9355\\Desktop\\opioid2015.csv')
df3 = pd.read_csv('C:\\Users\\btm9355\\Desktop\\opioid2016.csv')


# In[96]:


#Create Column for year
df['Year'] = 2013
df1['Year'] = 2014
df2['Year'] = 2015
df3['Year'] = 2016


# In[97]:


#Append Files together 
df_apped = df.append(df2, sort=True)
dfp = df_apped.append(df1, sort= True)
dfpp = dfp.append(df3, sort=True)


# In[98]:


#Want to rename the dataframe to make it easier to remember this is the raw data appended together 
df_raw = dfpp


# In[99]:


#Notice all the missing values or blanks in the data...replace with zero 
df_raw.count()


# In[100]:


df_final = df_raw.fillna(0)


# In[101]:


#No msising values now 
df_final.count()


# In[102]:


#Remove all the bullshit columns and keep the ones we care about, but first you want to rename them to make it easier 
df_clean = df_final.rename(columns={'Specialty Description': 'specialty',
                        'Opioid Claim Count': 'opioid_count', 
                        'Total Claim Count': 'claim_count',
                        'NPPES Provider State': 'state',})


# In[175]:


#Only selecting the columns I want 
df_clean = df_clean[['NPI','state','claim_count','specialty','opioid_count','Year']]
df_clean.to_csv('C:\\Users\\btm9355\\Desktop\\script\\medicareappended.csv')


# In[104]:


df_clean.count()
#Beautiful isnt she


# In[178]:


#Group by Year
#Reset the dataframes for both...column is not callable until you do so
claims_year = df_clean[['Year','claim_count']]
opioids_year = df_clean[['Year','opioid_count']]
grouped_cyears = claims_year.groupby('Year').sum().reset_index()
grouped_oyears = opioids_year.groupby('Year').sum().reset_index()


# In[181]:


year_merge = pd.merge(grouped_cyears, grouped_oyears)
year_merge.head()
#Create a column to show the percentage of opioids by overall drugs perscribed 
year_merge['opioid_year'] = year_merge['opioid_count'] / year_merge['claim_count']
year_merge.head()


# In[182]:


#Group by Specialty
#Reset the dataframes for both...column is not callable until you do so
claims_special = df_clean[['specialty','claim_count']]
opioids_special = df_clean[['specialty','opioid_count']]
grouped_claims = claims_special.groupby('specialty').sum().reset_index()
grouped_opioid = opioids_special.groupby('specialty').sum().reset_index()


# In[183]:


#Merge the datasets together...BOOM
special_merge = pd.merge(grouped_claims, grouped_opioid)
special_merge.head()


# In[184]:


#Create a column to show the percentage of opioids by overall drugs perscribed 
special_merge['opioid_amount'] = special_merge['opioid_count'] / special_merge['claim_count']
special_merge.head()


# In[174]:


#Sort by the opioid percentage and cut the data off by 30 subspecialites 
df = special_merge.sort_values(by = 'opioid_amount', ascending = False)
df.to_csv('C:\\Users\\btm9355\\Desktop\\script\\subbreakdown1.csv')


# In[169]:


#Create a sepreate dataframe that only take that column 
df = df[['specialty', 'opioid_amount']]
df


# In[170]:


df['Opioid Percentage'] = df['opioid_amount'] *100
df.to_csv('C:\\Users\\btm9355\\Desktop\\script\\subbreakdown.csv')


# In[143]:


df.plot.barh()


# In[ ]:




