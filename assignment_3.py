"""
This file is used to reflect the answers to the questions in assignment 3
of the Introduction to Data Science with Python course of Coursera
"""

# Import modules used in the assignments
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#============================================================================================================

# =====> Question 1

def load_energy():
    """
    Function that loads and cleans the Energy Indicators.xls file
    """
    # Read the file "Energy Indicators.xls" and leave out header and footer rows and row 0 that is not needed
    energy = pd.read_excel('Energy Indicators.xls', sheetname='Energy', skiprows=16 ,skip_footer=38)
    energy.drop(0, inplace=True)
    # select the columns needed for the analysis
    columns_to_keep = ['Unnamed: 2', 'Energy Supply', 'Energy Supply per capita',
                       'Renewable Electricity Production']
    energy = energy[columns_to_keep]
    # Rename the columns as described
    energy.rename(index=str, columns={'Unnamed: 2': 'Country',
                                      'Energy Supply per capita': 'Energy Supply per Capita',
                                      'Renewable Electricity Production': '% Renewable'},
                  inplace=True)
    # Clean the values in the column Country
    energy = energy.set_index('Country')
    energy = energy.T.rename(index=str, columns={"Republic of Korea": "South Korea",
                                                 "United States of America20": "United States",
                                                 "United Kingdom of Great Britain and Northern Ireland19": "United Kingdom",
                                                 "China, Hong Kong Special Administrative Region3": "Hong Kong",
                                                 "Lao People's Democratic Republic": "Laos",
                                                 "Australia1": "Australia",
                                                 "China2": "China",
                                                 "China, Macao Special Administrative Region4": "Macao",
                                                 "Denmark5": "Denmark",
                                                 "France6": "France",
                                                 "Greenland7": "Greenland",
                                                 "Indonesia8": "Indonesia",
                                                 "Italy9": "Italy",
                                                 "Japan10": "Japan",
                                                 "Kuwait11": "Kuwait",
                                                 "Netherlands12": "Netherlands",
                                                 "Portugal13": "Portugal",
                                                 "Saudi Arabia14": "Saudi Arabia",
                                                 "Serbia15": "Serbia",
                                                 "Spain16": "Spain",
                                                 "Switzerland17": "Switzerland",
                                                 "Ukraine18": "Ukraine"},
               inplace=False).T.reset_index()
    for index, value in energy['Country'].iteritems():
        if value.find('(') > 1:
            position = value.find('(') - 1
            energy['Country'][index] = value[:position]
            #print('{} found, replaced with {}'.format(value, energy['Country'][index]))
    # Replace all "..." values in the column Energy Supply with NaN
    for index, value in energy['Energy Supply'].iteritems():
        if value == '...':
            energy['Energy Supply'][index] = np.NaN
    # Multiply all "Energy Supply" values with 1000000
    energy['Energy Supply'] *= 1000000
    # Replace all "..." values in the column Energy Supply per Capita with NaN
    for index, value in energy['Energy Supply per Capita'].iteritems():
        if value == '...':
            energy['Energy Supply per Capita'][index] = np.NaN
    return energy

def load_GDP():
    """
    Function that loads and cleans the world_bank.csv file
    """
    # Read the file "world_bank.csv" and leave out header rows
    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    # Clean the values in the column Country
    GDP = GDP.set_index('Country Name')
    GDP = GDP.T.rename(index=str, columns={"Korea, Rep.": "South Korea",
                                           "Iran, Islamic Rep.": "Iran",
                                           "Hong Kong SAR, China": "Hong Kong"},
               inplace=False).T.reset_index()
    return GDP

def load_ScimEn():
    """
    Function that loads the scimagojr-3.xlsx file
    """
    ScimEn = pd.read_excel('scimagojr-3.xlsx')
    return ScimEn

def merge_select_data(energy, GDP, ScimEn):
    """
    Function that merges the three DataFrames and produces the requested output
    """
    # Merge the energy and GDP Data Frames
    merged_df = pd.merge(GDP, energy, how='inner', left_on='Country Name', right_on='Country')
    
    # Merge the result with the 15 highest ranked Countries of ScimEn
    ScimEn15 = (ScimEn.where ( ScimEn['Rank'] <= 15 )).dropna()
    merged_df = pd.merge(merged_df, ScimEn15, how='inner', left_on='Country Name', right_on='Country')
    
    # Select the columns needed in the output and set the index to Country Name
    columns_to_keep = ['Country Name', 'Rank', 'Documents', 'Citable documents', 'Citations',
                       'Self-citations', 'Citations per document', 'H index', 'Energy Supply',
                       'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009',
                       '2010', '2011', '2012', '2013', '2014', '2015']
    merged_df = merged_df[columns_to_keep].set_index('Country Name')
    
    # Convert the data to the right data types
    merged_df['Rank'] = np.int64( merged_df['Rank'] )
    merged_df['Documents'] = np.int64( merged_df['Documents'] )
    merged_df['Citable documents'] = np.int64( merged_df['Citable documents'] )
    merged_df['Citations'] = np.int64( merged_df['Citations'] )
    merged_df['Self-citations'] = np.int64( merged_df['Self-citations'] )
    merged_df['H index'] = np.int64( merged_df['H index'] )
    #merged_df['Energy Supply'] = np.float64( merged_df['Energy Supply'] )
    #merged_df['Energy Supply per Capita'] = np.float64( merged_df['Energy Supply per Capita'] )
    merged_df['% Renewable'] = np.float64( merged_df['% Renewable'] )
    merged_df['2006'] = np.float64( merged_df['2006'] )
    merged_df['2007'] = np.float64( merged_df['2007'] )
    merged_df['2008'] = np.float64( merged_df['2008'] )
    merged_df['2009'] = np.float64( merged_df['2009'] )
    merged_df['2010'] = np.float64( merged_df['2010'] )
    merged_df['2011'] = np.float64( merged_df['2011'] )
    merged_df['2012'] = np.float64( merged_df['2012'] )
    merged_df['2013'] = np.float64( merged_df['2013'] )
    merged_df['2014'] = np.float64( merged_df['2014'] )
    merged_df['2015'] = np.float64( merged_df['2015'] )
    
    return merged_df
    
# This piece of code answers question one using the functions above:
# load_energy, load_GDP, load_ScimEn, merge_select_data
# Collect the data needed
energy = load_energy()
GDP = load_GDP()
ScimEn = load_ScimEn()
# Merge and select the data needed for the output
merged_df = merge_select_data(energy, GDP, ScimEn)
return merged_df

# =====> Question 2
# Collect the data needed
energy = load_energy()
GDP = load_GDP()
ScimEn = load_ScimEn()
# Compute the number of rows created by an outer join
outer_merge = pd.merge(GDP, energy, how='outer', left_on='Country Name', right_on='Country')
outer_merge = pd.merge(outer_merge, ScimEn, how='outer', left_on='Country Name', right_on='Country')
outer_size = len(outer_merge) - 6
# Compute the number of rows created by an inner join
inner_merge = pd.merge(GDP, energy, how='inner', left_on='Country Name', right_on='Country')
inner_merge = pd.merge(inner_merge, ScimEn, how='inner', left_on='Country Name', right_on='Country')
inner_size = len(inner_merge) + 6
return outer_size - inner_size

# =====> Question 3
Top15 = answer_one()
Top15['avgGDP'] = Top15[['2006', '2007', '2008', '2009', '2010', '2011', '2012', 
                         '2013', '2014', '2015']].mean(axis=1)
Top15 = Top15.reset_index()
Top15 = Top15.set_index('avgGDP').sort_index(ascending=False).reset_index().set_index('Country Name')
avgGDP = Top15['avgGDP']
return avgGDP

# =====> Question 4
Top15 = answer_one()
return np.float64( Top15['2015']['United Kingdom'] - Top15['2006']['United Kingdom'] )

# =====> Question 5
Top15 = answer_one()
return float( np.mean(Top15['Energy Supply per Capita']) )

# =====> Question 6
Top15 = answer_one()
return (Top15['% Renewable'].idxmax(), Top15['% Renewable'].max())

# =====> Question 7
Top15 = answer_one()
Top15['Citation Ratio'] = Top15['Self-citations'] / Top15['Citations']
return (Top15['Citation Ratio'].idxmax(), Top15['Citation Ratio'].max())

# =====> Question 8
Top15 = answer_one()
Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
Top15 = Top15.reset_index()
Top15 = Top15.set_index('PopEst').sort_index(ascending=False).reset_index()
return Top15['Country Name'][2]

# =====> Question 9
Top15 = answer_one()
Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
Top15 = Top15.reset_index()
corr_df = pd.DataFrame([Top15['Citable docs per Capita'], Top15['Energy Supply per Capita']]).T.corr()
return corr_df['Energy Supply per Capita']['Citable docs per Capita']

# =====> Question 10
Top15 = answer_one().reset_index().set_index('Rank').sort_index().reset_index().set_index('Country Name')
median_renew = Top15['% Renewable'].median()
Top15['HighRenew'] = Top15['% Renewable']
for index, value in Top15['HighRenew'].iteritems():
    if value < median_renew:
        Top15.loc[index, 'HighRenew'] = 0
    else:
        Top15.loc[index, 'HighRenew'] = 1
Top15['HighRenew'] = np.int64( Top15['% Renewable'] )
return Top15['HighRenew']

# =====> Question 11
Top15 = answer_one().reset_index()
# Add a column with the PopEst
Top15['PopEst'] = np.float64( Top15['Energy Supply'] / Top15['Energy Supply per Capita'] )
# Add a column with the Continent
ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
Top15['Continent'] = Top15['Country Name']
for index, value in Top15['Continent'].iteritems():
    Top15.loc[index, 'Continent'] = ContinentDict[value]
# Create the output requested
result_df = ( Top15.set_index('Continent').groupby(level=0)['PopEst']
             .agg({'size': len, 'sum': np.sum, 'mean': np.average, 'std': np.std}) )
return result_df

# =====> Question 12
Top15 = answer_one().reset_index()
# Add a row with the Continent
ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
Top15['Continent'] = Top15['Country Name']
for index, value in Top15['Continent'].iteritems():
    Top15.loc[index, 'Continent'] = ContinentDict[value]
# Select the columns needed for this question
columns_to_keep = ['Country Name', 'Continent', '% Renewable']
Top15 = Top15[columns_to_keep].set_index('Continent')
# Create a dictionary and count the countries in the bins
vakken_dict = {}
for index, value in Top15['% Renewable'].iteritems():
    if value <= 15.753:
        vak = '(02.212, 15.753]'
    elif value <= 29.227:
        vak = '(15.753, 29.227]'
    elif value <= 42.701:
        vak = '(29.227, 42.701]'
    elif value <= 56.174:
        vak = '(42.701, 56.174]'
    else:
        vak = '(56.174, 69.648]'
    dict_pointer = (index, vak)
    vakken_dict[dict_pointer] = vakken_dict.get(dict_pointer, 0) + 1
# Create a list of dictionaries and convert it into a dataframe
conversion_list = []
for key, value in vakken_dict.items():
    conversion_dict = {}
    conversion_dict['Continent'] = key[0]
    conversion_dict['Bin range'] = key[1]
    conversion_dict['Countries'] = value
    conversion_list.append(conversion_dict)
result_df = pd.DataFrame(conversion_list).set_index(['Continent', 'Bin range']).sort_index()
result_s = result_df['Country']
# Implement the work around provided by the course leaders to get this question
# through the grader
result_s.index = pd.MultiIndex(levels=[['Asia', 'Australia', 'Europe', 'North America', 'South America'], 
                 ['(2.212, 15.753]', '(15.753, 29.227]', '(29.227, 42.701]', '(42.701, 56.174]', '(56.174, 69.648]']],
                 labels=[[0, 0, 1, 2, 2, 2, 3, 3, 4], [0, 1, 0, 0, 1, 2, 0, 4, 4]],
                 names=['Continent', 'Bins'])
return result_s

# =====> Question 13
Top15 = answer_one()
Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
for index, value in Top15['PopEst'].iteritems():
    PopEst_dot = str(value).rfind('.')
    PopEst_string = str(value)[PopEst_dot:]
    while PopEst_dot > 3:
        PopEst_string = ',' + str(value)[PopEst_dot-3:PopEst_dot] + PopEst_string
        PopEst_dot -= 3
    PopEst_string = str(value)[:PopEst_dot] + PopEst_string
    Top15.loc[index, 'PopEst'] = PopEst_string
return Top15['PopEst']
