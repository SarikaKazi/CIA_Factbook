#!/usr/bin/env python
# coding: utf-8

# # CIA Factbook Analysis

# ## Introduction
# 
# The World Factbook (published by the CIA) provides information on the history, people and society, government, economy, energy, geography, communications, transportation, military, and transnational issues for 267 world entities.
# 
# The dataset is available to the public.
# 
# FYI: Data Analytics Project #1

# In[1]:


# Connect to SQLite database, run query, and display results as a DataFrame

import sqlite3
import pandas as pd

conn = sqlite3.connect("factbook.db")
cursor = conn.cursor()

q1 = "SELECT * FROM sqlite_master WHERE type='table';"
cursor.execute(q1).fetchall()

pd.read_sql_query(q1, conn)


# ### Column Descriptions for 'facts' table
# 
# name - The name of the country.
# 
# area - The total land and sea area of the country.
# 
# population - The country's population.
# 
# population_growth- The country's population growth as a percentage.
# 
# birth_rate - The country's birth rate, or the number of births a year per 1,000 people.
# 
# death_rate - The country's death rate, or the number of death a year per 1,000 people.
# 
# area- The country's total area (both land and water).
# 
# area_land - The country's land area in square kilometers.
# 
# area_water - The country's waterarea in square kilometers.

# In[2]:


# Query of the first 10 rows of the 'facts' table

q2 = "select * from facts limit 10;"
pd.read_sql_query(q2, conn)


# ## Summary Statistics

# In[3]:


q3 = '''
        SELECT 
            MIN(population),
            MAX(population),
            MIN(population_growth),
            MAX(population_growth) 
        FROM facts;
     '''   
pd.read_sql_query(q3, conn)


# #### Notice: Oddly, the minimum population is 0 and the maximum population is about 7.2 billion. These outliers are skewing the results of the Summary Statistics.

# ## Dataset Outliers

# In[4]:


q4 = '''
        SELECT * FROM facts
        WHERE population = 0;
     '''
pd.read_sql_query(q4, conn)


# In[5]:


q5 = '''
        SELECT * FROM facts
        WHERE population = 7256490011;
     '''
pd.read_sql_query(q5, conn)


# ### Culprits behind skewed Summary Statistics results:
# ###        - Antartica has a population of 0
# ###        - The World population is 7,256,490,011
# 
# ### Therefore, they should be removed from the queries

# ## Revised Summary Statistics

# In[6]:


q3_edit1 = '''
            SELECT
                name Country,
                MIN(population) Smallest_Population
            FROM facts
            WHERE population >0 AND population <7256490011;
            '''
q3_edit2 = '''         
            SELECT
                name Country,
                MAX(population) Largest_Population
            FROM facts
            WHERE population >0 AND population <7256490011;
            '''
q3_edit3 = '''
            SELECT
                name Country,
                MIN(population_growth) Lowest_Population_Growth
            FROM facts
            WHERE population >0 AND population <7256490011;
           '''
q3_edit4 = '''
            SELECT
                name Country,
                MAX(population_growth) Highest_Population_Growth
            FROM facts
            WHERE population >0 AND population <7256490011;
     '''   
pd.read_sql_query(q3_edit1, conn)


# In[7]:


q3_edit2 = '''         
            SELECT
                name Country,
                MAX(population) Largest_Population
            FROM facts
            WHERE population >0 AND population <7256490011;
            '''
pd.read_sql_query(q3_edit2, conn)


# In[8]:


q3_edit3 = '''
            SELECT
                name Country,
                MIN(population_growth) Lowest_Population_Growth
            FROM facts
            WHERE population >0 AND population <7256490011;
           '''
pd.read_sql_query(q3_edit3, conn)


# In[9]:


q3_edit4 = '''
            SELECT
                name Country,
                MAX(population_growth) Highest_Population_Growth
            FROM facts
            WHERE population >0 AND population <7256490011;
     '''
pd.read_sql_query(q3_edit4, conn)


# In[10]:


# Select Columns from the 'facts' table

q6 = '''
        SELECT 
            population,
            population_growth,
            birth_rate,
            death_rate
        FROM facts
        WHERE population >0 AND population <7256490011;
     '''
pd.read_sql_query(q6, conn)


# ## Data Visualization: Histograms

# In[11]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().magic('matplotlib inline')

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)

pd.read_sql_query(q6, conn).hist(ax=ax)


# ## Which countries have the highest population density?

# In[12]:


q7 = '''
        SELECT 
        name Country,
        population/area_land Population_Density
        FROM facts
        WHERE population >0 AND population <7256490011
        ORDER BY 2 DESC
        LIMIT 10;
     '''
pd.read_sql_query(q7,conn)


# ### Macau, Monaco, Singapore, Hong Kong, and Gaza Strip have the highest population densities.
