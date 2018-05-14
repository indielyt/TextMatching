#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 10:57:38 2017

@author: Daniel
"""
# Documentation
# http://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/

# Installation
# https://anaconda.org/conda-forge/fuzzywuzzy
# https://anaconda.org/conda-forge/python-levenshtein

import pandas as pd
import numpy as np

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

outpath = r'R:\161485_Boulder Room For River\13-Working\Phase 1-Kickoffs & Data Collection\data\NFIP CLaims\NFIP_Claims_Matched.csv'

NFIP_csv = r'R:\161485_Boulder Room For River\13-Working\Phase 1-Kickoffs & Data Collection\data\NFIP CLaims\NFIP_CLaims.csv'
Owner_Addresses_csv = r'R:\161485_Boulder Room For River\10_GIS\02_Source\New_BoulderCountyData\Assessor_Tables\Owner_Address.csv'

df1 = pd.read_csv(NFIP_csv)
df2 = pd.read_csv(Owner_Addresses_csv)


#### Preprocessing the NFIP data

# convert all zip codes to 5 digit rather than 9 digit
df1['zip'] = df1['Zip Code'].astype(str)
df1['zip'] = df1['zip'].apply(lambda x: x[0:5])

# Concatenate the address, convert to all lower case 
df1['concat1'] = (df1['Address Line 2'] + " " + df1['City']).str.lower()

#print (df1.head())



#### Preprocessing the Owner Address data

# convert street numbers to string, then remove decimals (quirk of str method)
df2['str_num'] = df2['str_num'].astype(str)
df2['str_num'] = df2['str_num'].apply(lambda x: x.split('.')[0])

# Remove nan where there is no street prefix
df2['str_pfx'] = df2['str_pfx'].astype(str)
df2['str_pfx'] = df2['str_pfx'].replace('nan', "")

# Remove nan where there is no street suffix
df2['str_sfx'] = df2['str_sfx'].astype(str)
df2['str_sfx'] = df2['str_sfx'].replace('nan', "")



#### Concatentate the address fields

# conctatenate and convert to lower case
df2['concat2'] = (df2['str_num'] + " " + df2['str_pfx'] + " " + df2['str'] + " " + \
   df2['str_sfx'] + " " + df2['city']).str.lower()

# Strip trailing white spaces 
df2['concat2'] = df2['concat2'].str.strip()

#print (df1.head(), '\n')
#print (df2.head())




#### Match and score the concatenated addresses

## Create three new columns to track results of the test
df1['best_match'] = np.zeros
df1['best_score'] = np.zeros
df1['best_score_ID'] = np.zeros

#print (len(df1))
#print (len(df2))
#print (df1.info())
df1 = df1.astype(str)
df2 = df2.astype(str)
#print (df1.info())

 
print ('matching fuzzy text')
# Step through each feature of the first dataframe
for i in range(len(df1)):
    # Initiate the best score variable to zero
    best_score = 0
    # Step through each feature of the second dataframe
    for j in range (len(df2)):
        print (j, 'of df2 ', len(df2), (i, 'of df1 ', len(df1)))
        # Score the comparison by token set ratio method
#        score = fuzz.partial_ratio(df1['concat1'].iloc[i], df2['concat2'].iloc[j])
        score = fuzz.partial_ratio(df1.loc[i, 'concat1'], df2.loc[j, 'concat2'])
        # If the score is better than any of the previous comparisons, update
        if score >= best_score:
            best_score = score
            df1['best_score'].iloc[i] = best_score
            df1['best_score_ID'].iloc[i] = df2['strap'].iloc[j]
            df1['best_match'].iloc[i] = df2['concat2'].iloc[j]

print ('match complete')
print (df1.head())

df1.to_csv(outpath, sep = ",")

    





## SIMPLE RATIO, utilizes the difflib package's SequenceMatcher to produce ratio of equality
#print (fuzz.ratio("this is a test", "this is a test!"))
#
## PARTIAL RATIO, compares shorter string to pieces of longer string
#print (fuzz.partial_ratio("this is a test", "this is a test!"))
#
## TOKEN SORT RATIO, handles out of order strings by ordering alphabetically before comparing
#print (fuzz.ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear"))
#print (fuzz.token_sort_ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear"))
#
## TOKEN SET RATIO, before token sort, computes the intersection of terms, then 
## compares the intersection plus remainder to find score
#print (fuzz.token_sort_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear"))
#print (fuzz.token_set_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear"))
#
## PROCESS
#choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]
#print (process.extract("new york jets", choices, limit=2))
#print (process.extractOne("cowboys", choices))



# Create two dataframes to test
#data1 = {'address': ['234 First avenue', '17 fourmile cnyd', '1234 mason street'], \
#         'person': ['bob', 'mary', 'jill']}
#df1 = pd.DataFrame(data1)
#
#data2 = {'address': ['234 first Ave', '17 fourmile canyon drive', '1234 mason street'], \
#         'person': ['Bob', 'Mary', 'Jill'], 'ID': [10021,10031,10041]}
#df2 = pd.DataFrame(data2)