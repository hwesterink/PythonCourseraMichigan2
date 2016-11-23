"""
In this file contains the functions written for project/assignment 4 of the
Introduction to Data Science with Python course of Coursera
"""

# Import modules used in the assignments
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind

#============================================================================================================

# =====> Function get_list_of_university_towns()

def get_list_of_university_towns():
    '''
    Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan","Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State","RegionName"]  )
    '''
    
    # Read the university towns list from the file university_towns.txt
    # and create a list of lines with states and towns from it
    fhandle = open('university_towns.txt')
    data = fhandle.read()
    lines = data.split('\n')
    fhandle.close()
    
    # Convert these lines in a list of lists with the format [ ['state', 'region'], ... ]
    university_towns_list = []
    line_counter = 0
    while line_counter < len(lines):
        if len(lines[line_counter]) == 0:
            # Skip empty lines
            line_counter += 1
            continue
        elif lines[line_counter].endswith('[edit]'):
            # State line found, replace the name of the state
            state = lines[line_counter][:-6]
            line_counter += 1
            continue
        elif lines[line_counter].find(' (') != -1:
            # Region line found, remove anything starting with ' (' from the name
            region = lines[line_counter][:lines[line_counter].index(' (')]
        else:
            # Other region line found which is not adapted
            region = lines[line_counter]
        university_towns_list.append( [state, region] )
        line_counter += 1
    
    # Convert the list of university towns into the dataframe requested
    university_towns_df = pd.DataFrame(university_towns_list, columns=['State', 'RegionName'])
    return university_towns_df
    
# =====> Function analyse_recession()

def analyse_recession():
    '''
    Helper function that returns the year and quarter of the recession
    start time, the recession end time and the recession bottom all as a 
    string value in a format such as 2005q3
    '''

    # Read the data needed from the file gdplev.xls
    col_names = ['col1', 'col2', 'col3', 'col4', 'quarter', 'col6', 'GDP 2009 dollars', 'col8']
    GDP_df = pd.read_excel('gdplev.xls', skiprows=219, names=col_names)
    cols_to_keep = ['quarter', 'GDP 2009 dollars']
    GDP_df = GDP_df[cols_to_keep]

    # Find the start quarter of the recession
    GDP_list = list(GDP_df['GDP 2009 dollars'])
    GDP_bottom = float('inf')
    for index in range(len(GDP_list)-2):
        if ( GDP_list[index+2] < GDP_list[index+1] and
            GDP_list[index+1] < GDP_list[index] ):
            ix_start = index+1
            break

    # When no recession found, return (-1, -1, -1)
    if index == len(GDP_list):
        return (-1, -1, -1)

    # Find the end quarter of the recession
    for index in range(ix_start, len(GDP_list)-2):
        if ( GDP_list[index+2] > GDP_list[index+1] and
            GDP_list[index+1] > GDP_list[index] ):
            ix_end = index+2
            break

    # Find the bottom quarter of the recession
    for index in range(ix_start, ix_end):
        if GDP_list[index] < GDP_bottom:
            GDP_bottom = GDP_list[index]
            ix_bottom = index
    return GDP_df.loc[ix_start, 'quarter'], GDP_df.loc[ix_end, 'quarter'], GDP_df.loc[ix_bottom, 'quarter']
    
# =====> Function get_recession_start()

def get_recession_start():
    '''
    Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3
    '''
    start, end, bottom = analyse_recession()
    return start    
    
# =====> Function get_recession_end()

def get_recession_end():
    '''
    Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3
    '''
    start, end, bottom = analyse_recession()
    return end    
    
# =====> Function get_recession_bottom()

def get_recession_bottom():
    '''
    Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3
    '''
    start, end, bottom = analyse_recession()
    return bottom    
    
# =====> Function convert_housing_data_to_quarters()

def convert_housing_data_to_quarters():
    '''
    Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    # Read the data needed from the file City_Zhvi_AllHomes.csv
    prices_df = pd.read_csv('City_Zhvi_AllHomes.csv')
    cols_to_keep = ['State', 'RegionName', 
                    '2000-01', '2000-02', '2000-03', '2000-04', '2000-05', '2000-06',
                    '2000-07', '2000-08', '2000-09', '2000-10', '2000-11', '2000-12',
                    '2001-01', '2001-02', '2001-03', '2001-04', '2001-05', '2001-06',
                    '2001-07', '2001-08', '2001-09', '2001-10', '2001-11', '2001-12',
                    '2002-01', '2002-02', '2002-03', '2002-04', '2002-05', '2002-06',
                    '2002-07', '2002-08', '2002-09', '2002-10', '2002-11', '2002-12',
                    '2003-01', '2003-02', '2003-03', '2003-04', '2003-05', '2003-06',
                    '2003-07', '2003-08', '2003-09', '2003-10', '2003-11', '2003-12',
                    '2004-01', '2004-02', '2004-03', '2004-04', '2004-05', '2004-06',
                    '2004-07', '2004-08', '2004-09', '2004-10', '2004-11', '2004-12',
                    '2005-01', '2005-02', '2005-03', '2005-04', '2005-05', '2005-06',
                    '2005-07', '2005-08', '2005-09', '2005-10', '2005-11', '2005-12',
                    '2006-01', '2006-02', '2006-03', '2006-04', '2006-05', '2006-06',
                    '2006-07', '2006-08', '2006-09', '2006-10', '2006-11', '2006-12',
                    '2007-01', '2007-02', '2007-03', '2007-04', '2007-05', '2007-06',
                    '2007-07', '2007-08', '2007-09', '2007-10', '2007-11', '2007-12',
                    '2008-01', '2008-02', '2008-03', '2008-04', '2008-05', '2008-06',
                    '2008-07', '2008-08', '2008-09', '2008-10', '2008-11', '2008-12',
                    '2009-01', '2009-02', '2009-03', '2009-04', '2009-05', '2009-06',
                    '2009-07', '2009-08', '2009-09', '2009-10', '2009-11', '2009-12',
                    '2010-01', '2010-02', '2010-03', '2010-04', '2010-05', '2010-06',
                    '2010-07', '2010-08', '2010-09', '2010-10', '2010-11', '2010-12',
                    '2011-01', '2011-02', '2010-03', '2011-04', '2011-05', '2011-06',
                    '2011-07', '2011-08', '2011-09', '2011-10', '2011-11', '2011-12',
                    '2012-01', '2012-02', '2012-03', '2012-04', '2012-05', '2012-06',
                    '2012-07', '2012-08', '2012-09', '2012-10', '2012-11', '2012-12',
                    '2013-01', '2013-02', '2013-03', '2013-04', '2013-05', '2013-06',
                    '2013-07', '2013-08', '2013-09', '2013-10', '2013-11', '2013-12',
                    '2014-01', '2014-02', '2014-03', '2014-04', '2014-05', '2014-06',
                    '2014-07', '2014-08', '2014-09', '2014-10', '2014-11', '2014-12',
                    '2015-01', '2015-02', '2015-03', '2015-04', '2015-05', '2015-06',
                    '2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12',
                    '2016-01', '2016-02', '2016-03', '2016-04', '2016-05', '2016-06',
                    '2016-07', '2016-08'
                   ]
    prices_df = prices_df[cols_to_keep]
    # Create a DataFrame to build the resulting output in
    results_df = pd.DataFrame(prices_df['State'])
    results_df['RegionName'] = prices_df['RegionName']
    # Replace the two letter acronims with the state names by the full state names in
    # the new DataFrame
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada',
              'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland',
              'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana',
              'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia',
              'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine',
              'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan',
              'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam',
              'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina',
              'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands',
              'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia',
              'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York',
              'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California',
              'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico',
              'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands',
              'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia',
              'ND': 'North Dakota', 'VA': 'Virginia'
             }    
    results_df.replace(states, inplace=True)
    # Group the columns by quarters, compute the mean house prices and add quarter columns
    # to the results DataFrame
    mnth_to_qtr = {'01': 'q1', '02': 'q1', '03': 'q1',
                   '04': 'q2', '05': 'q2', '06': 'q2',
                   '07': 'q3', '08': 'q3', '09': 'q3',
                   '10': 'q4', '11': 'q4', '12': 'q4',}
    qtr_months = {}
    for col in prices_df.columns:
        if col.startswith('20'):
            quarter = col[:4] + mnth_to_qtr[col[-2:]]
            qtr_months[quarter] = qtr_months.get(quarter, []) + [col]
    for key,value in qtr_months.items():
        results_df[key] = prices_df[value].mean(axis=1)
    return results_df.set_index(['State', 'RegionName'])
    
# =====> Function run_ttest()

def run_ttest():
    '''
    First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).
    '''
    # Find the recesion start and bottom quarters
    start, dummy_end, bottom = analyse_recession()
    
    # Read the house pricing data for the recession start and recession bottom needed for the ttest
    house_pricings_df = convert_housing_data_to_quarters()
    cols_to_keep = [start, bottom]
    house_pricings_df = house_pricings_df[cols_to_keep]
    house_pricings_df['mean_price_ratio'] = house_pricings_df[start] / house_pricings_df[bottom]
    house_pricings_df = pd.DataFrame(house_pricings_df['mean_price_ratio'])

    # Read the collection of university towns
    university_towns_df = get_list_of_university_towns()
    university_towns_df.set_index(['State', 'RegionName'], inplace=True)
    
    # Prepare the data for the ttest
    ## > Create the list of house pricings for the univerity regions
    pricings_univ_df = pd.merge(university_towns_df, house_pricings_df,
                                how='inner', left_index=True, right_index=True)
    ## > Create the list of house pricings for the non-university regions
    ### - Convert the list of house prices to a separate single index list 
    univ_st_reg_df = pricings_univ_df.copy().reset_index()
    univ_st_reg_df['st-reg'] = univ_st_reg_df['State'] + '/' + univ_st_reg_df['RegionName']
    univ_st_reg_df.set_index('st-reg', inplace=True)
    ### - Convert the complete list of house pricings to a separate single index list
    non_univ_st_reg_df = house_pricings_df.copy().reset_index()
    non_univ_st_reg_df['st-reg'] = non_univ_st_reg_df['State'] + '/' + non_univ_st_reg_df['RegionName']    
    non_univ_st_reg_df.set_index('st-reg', inplace=True)
    ### - Remove the items that are from the university regions for the complete list of
    ###   house pricings to leave a set of non-university region pricings
    for index, value in univ_st_reg_df['mean_price_ratio'].iteritems():
        non_univ_st_reg_df.drop(index, inplace=True)

    ## > Remove all NaN values from the univ_st_reg_df and non_univ_st_reg_df DataFrames
    univ_st_reg_df = pd.DataFrame(univ_st_reg_df['mean_price_ratio'])
    univ_st_reg_df.dropna(inplace=True)
    non_univ_st_reg_df = pd.DataFrame(non_univ_st_reg_df['mean_price_ratio'])
    non_univ_st_reg_df.dropna(inplace=True)
        
    # Run the ttest
    statistic, pvalue = ttest_ind(univ_st_reg_df['mean_price_ratio'], non_univ_st_reg_df['mean_price_ratio'])
    
    # Translate the results of the ttest into the functions output
    if pvalue < 0.01:
        different = True
    else:
        different = False
    if statistic < 0:
        better = 'university town'
    else:
        better = 'non-university town'
    
    return different, pvalue, better
