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

outpath = r'R:\161485_Boulder Room For River\13-Working\Phase 1-Kickoffs & Data Collection\data\2013 Damage Estimates\2013_DamageEstimates_matched.csv'

#NFIP_csv = r'R:\161485_Boulder Room For River\13-Working\Phase 1-Kickoffs & Data Collection\data\NFIP CLaims\NFIP_CLaims.csv'
damageEstimates_csv = r'R:\161485_Boulder Room For River\13-Working\Phase 1-Kickoffs & Data Collection\data\2013 Damage Estimates\2013_DamageEstimates_tabular.csv'
Owner_Addresses_csv = r'R:\161485_Boulder Room For River\10_GIS\02_Source\New_BoulderCountyData\Assessor_Tables\Owner_Address.csv'

df1 = pd.read_csv(damageEstimates_csv)
df2 = pd.read_csv(Owner_Addresses_csv)


#### Preprocessing the NFIP data

# convert all zip codes to 5 digit rather than 9 digit
df1['Address'] = df1['Address'].astype(str)
df1['County'] = df1['County'].astype(str)


# Concatenate the address, convert to all lower case 
df1['concat1'] = (df1['Address']).str.lower()

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
   df2['str_sfx']).str.lower()

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