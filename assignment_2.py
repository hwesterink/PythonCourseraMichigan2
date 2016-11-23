"""
This file is used to reflect the answers to the questions in assignment 2
of the Introduction to Data Science with Python course of Coursera
"""
# Import modules used in the assignments
import numpy as np
import pandas as pd

########################################
# Preparation of the data for part one #
########################################
#
# Read the data from file
df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

# Adapt the data to the questions to andwer
for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

# Make the index more readable by splitting it and adding an ID column
names_ids = df.index.str.split('\s\(') # split the index by '('
df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

# Drop lines not needed for the analysis
df = df.drop('Totals') # Delete the last line with the overall totals

############################################
# The answers to the questions of part one #
############################################
#===> Question 0 (given)
return df.iloc[0]
#===> Question 1
return df['Gold'].argmax()
#===> Question 2
return abs(df['Gold'] - df['Gold.1']).argmax()
#===> Question 3
only_gold_SW = (df.where ( (df['Gold'] >= 1) & (df['Gold.1'] >= 1) )).dropna()
return (abs(only_gold_SW['Gold'] - only_gold_SW['Gold.1'])/only_gold_SW['Gold.2']).argmax()
#===> Question 4
df['Points'] = 3*df['Gold.2'] + 2*df['Silver.2'] + df['Bronze.2']
return df['Points']

########################################
# Preparation of the data for part two #
########################################
#
# Read the data from file
census_df = pd.read_csv('census.csv')
############################################
# The answers to the questions of part two #
############################################
#===> Question 5
only_sumlev_50 = (census_df.where ( census_df['SUMLEV'] == 50 )).dropna()
count_counties = {}
for state in only_sumlev_50['STNAME']:
    count_counties[state] = count_counties.get(state, 0) + 1
max_state = ""; max_count = 0
for key,value in count_counties.items():
    if value > max_count:
        max_count = value; max_state = key
return max_state

#===> Question 6
# Select the rows needed for the analysis
only_sumlev_50 = (census_df.where ( census_df['SUMLEV'] == 50 )).dropna()
# Select the columns needed for the analysis
columns_to_keep = ['STNAME', 'CENSUS2010POP']
only_sumlev_50 = only_sumlev_50[columns_to_keep]
only_sumlev_50.head()
# Sort the data as needed for the analysis
only_sumlev_50 = only_sumlev_50.set_index(['STNAME', 'CENSUS2010POP'])
only_sumlev_50 = only_sumlev_50.sort_index(ascending=False)
only_sumlev_50 = only_sumlev_50.reset_index()
# Compute the population per state based on the three most populous counties
state_pop = {}
state = ""
for index in range(len(only_sumlev_50)):
    counted = False
    if state != only_sumlev_50.iloc[index]['STNAME']:
        state = only_sumlev_50.iloc[index]['STNAME']
        state_pop[state] = only_sumlev_50.iloc[index]['CENSUS2010POP']
        counted = True
        counter = 1
    if not(counted) and counter < 3:
        state_pop[state] = state_pop[state] + only_sumlev_50.iloc[index]['CENSUS2010POP']
        counter += 1
# Select the three most populated states from the dictionary
most_populated = []
for dummy_index in range(3):
    max_pop = 0
    for key, value in state_pop.items():
        if value > max_pop:
            max_pop = value
            max_state = key
    most_populated.append(max_state)
    dummy_removed = state_pop.pop(max_state)
return most_populated

#===> Question 7
# Select the rows needed for the analysis
only_sumlev_50 = (census_df.where ( census_df['SUMLEV'] == 50 )).dropna()
# Select the columns needed for the analysis
columns_to_keep = ['CTYNAME',
                   'POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012',
                   'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015']
only_sumlev_50 = only_sumlev_50[columns_to_keep]
# Add columns HIGHEST, LOWEST and POP_DIFF
only_sumlev_50['HIGHEST'] = only_sumlev_50[['POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012',
                   'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015']].max(axis=1)
only_sumlev_50['LOWEST'] = only_sumlev_50[['POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012',
                   'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015']].min(axis=1)
only_sumlev_50['POP_DIFF'] = abs( only_sumlev_50['HIGHEST'] - only_sumlev_50['LOWEST'] )
# Now sort the DataFrame on accending POP_DIFF
only_sumlev_50 = only_sumlev_50.set_index(['POP_DIFF'])
only_sumlev_50 = only_sumlev_50.sort_index(ascending=False)
return only_sumlev_50.iloc[0]['CTYNAME']

#===> Question 8
# Select the rows with SUMLEV 50 (rows with data on the county level)
only_sumlev_50 = (census_df.where ( census_df['SUMLEV'] == 50 )).dropna()
# Select the columns needed for the analysis
columns_to_keep = ['REGION', 'STNAME', 'CTYNAME',
                   'POPESTIMATE2014', 'POPESTIMATE2015']
only_sumlev_50 = only_sumlev_50[columns_to_keep]
# Select the counties with region codes 1 or 2
only_sumlev_50 = (only_sumlev_50.where ( (only_sumlev_50['REGION'] == 1) | (only_sumlev_50['REGION'] == 2) )).dropna()
# Select the rows where CTYNAME starts with 'Washington'
only_sumlev_50 = (only_sumlev_50.where ( only_sumlev_50['CTYNAME'].str.contains('Washington') )).dropna()
# Select the counties whose POPESTIMATE2015 > POPESTIMATE2014
only_sumlev_50 = (only_sumlev_50.where ( only_sumlev_50['POPESTIMATE2015']
                                        > only_sumlev_50['POPESTIMATE2014'] )).dropna()
# Drop the columns not needed in the final result
columns_to_keep = ['STNAME', 'CTYNAME']
only_sumlev_50 = only_sumlev_50[columns_to_keep]
return only_sumlev_50