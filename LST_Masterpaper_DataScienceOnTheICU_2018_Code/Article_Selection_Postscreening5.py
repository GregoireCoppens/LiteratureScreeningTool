# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 22:05:28 2018

@author: grego
"""
# Setup
import pandas as pd
from os import walk

from itertools import chain
import numpy as np


# Define data frames
df_screened_output = pd.DataFrame(columns=['index', 'criterea', 'comments'])

df_all = pd.read_pickle("Article_Table.pkl")

# import all datasets
# http://www.martinbroadhurst.com/listing-all-files-in-a-directory-with-a-certain-extension-in-python.html
for (dirpath, dirnames, filenames) in walk('./backup5'):
    for f in filenames:
        if f.endswith('.pkl'):
            df_screened_output = df_screened_output.append(
                    pd.read_pickle("./backup5/"+f).reset_index(),
                    ignore_index=True)

# extend all screener lists
for i in df_screened_output.loc[
        df_screened_output["index"].duplicated(),
        "index"]:
    all_screeners = list()
    for j in list(df_screened_output.loc[
            df_screened_output['index'] == i,
            "criterea"]):
        all_screeners.extend(j)
    df_screened_output.loc[
            df_screened_output['index'] == i,
            "criterea"]\
        = set(all_screeners)

# remove duplicates from screener list
df_screened_output.drop_duplicates(subset="index", inplace=True)

# Change all sets back into lists
crits = list(df_screened_output["criterea"])
for i in range(len(crits)):
    if type(crits[i]) == set:
        crits[i] = list(crits[i])
df_screened_output["criterea"] = crits

# select articles that don't contain exclusion criteria or are empty
matches = df_screened_output.loc[
        (df_screened_output["criterea"].astype(str) != '[]')
        & ~(df_screened_output["criterea"].
            astype(str).str.contains("Not Specific"))
        & ~(df_screened_output["criterea"].
            astype(str).str.contains("No ICU"))
        & ~(df_screened_output["criterea"].
            astype(str).str.contains("Different Language")),
        'index']

# create final dataframe with the selection of IDs in matches
df = df_all.loc[df_all['ID'].isin(matches), :]

# Append selection criteria to text
# =============================================================================
# for i in df.ID:
#     df.loc[df['ID'] == i, 'Title'] += \
#         str(
#                 df_screened_output.loc[
#                         df_screened_output['index'] == i,
#                         "criterea"]
#                 .item()
#                 )
#
# =============================================================================

# Get all criterea in a list
crit_lst_ex = ["Telemedecine", "Arden Syntax",
               "Clinical Decision Support System", "Monitors", "Alarm Fatigue",
               "EEG", "Glucose Monitoring", "Scoring Systems",
               "Multi-Parameter Monitoring"]

crit_lst = list(set(
        chain.from_iterable(
            df_screened_output.loc[
                df_screened_output['index'].isin(matches),
                'criterea']
            )))
crit_lst = [item for item in crit_lst if item not in crit_lst_ex]
# Merge 2 dataframes to include criteria into df
df = pd.merge(df, df_screened_output,
              how="left", left_on=["ID"], right_on=["index"])
# Make a column vor every criterea
for i in crit_lst:
    df[i] = np.where(df['criterea'].astype(str).str.contains(i), True, False)

# Remove unused columns
df = df.drop(columns=["index", "criterea", "comments"])

# Select articles that have at least one of the included criteria
df = df.loc[df.iloc[:, 8:].any(axis=1)].reset_index(drop=True)

# Make summary dataframe of results:
total = list()
for i in list(df.iloc[:, 8:].columns):
    total.append(sum(df.loc[:, i]))

df_analysis = pd.DataFrame(
        total,
        index=list(df.iloc[:, 8:].columns),
        columns=["total"])

# Remove spelling error
df_screened_output["criteria"] = df_screened_output["criterea"]
df_screened_output = df_screened_output.drop(columns=["criterea"])

# output new pickle for new screening round
df.to_pickle("Article_Table_Postscreening5.pkl")
df.to_excel("Article_Table_Postscreening5.xlsx")
df_analysis.to_pickle("Analysis_Table_Postscreening5.pkl")
df_analysis.to_excel("Analysis_Table_Postscreening5.xlsx")
df_analysis.to_html("Analysis_Table_Postscreening5.html")
df_screened_output.to_pickle("Output_Table_Postscreening5.pkl")
df_screened_output.to_excel("Output_Table_Postscreening5.xlsx")

