# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 22:05:28 2018

@author: grego
"""
# Setup
import pandas as pd
from os import walk

# Define data frames
df_screened_output = pd.DataFrame(columns=['index', 'criterea', 'comments'])

df_all = pd.read_pickle("Article_Table.pkl")

# import all datasets
# http://www.martinbroadhurst.com/listing-all-files-in-a-directory-with-a-certain-extension-in-python.html
for (dirpath, dirnames, filenames) in walk('./backup'):
    for f in filenames:
        if f.endswith('.pkl'):
            df_screened_output = df_screened_output.append(
                    pd.read_pickle("./backup/"+f).reset_index(),
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

# add readmitted articles from second screening and remove 'not specific'
df_screened_output2 = pd.DataFrame(columns=['index', 'criterea', 'comments'])
for (dirpath, dirnames, filenames) in walk('./backup2'):
    for f in filenames:
        if f.endswith('.pkl'):
            df_screened_output2 = df_screened_output2.append(
                    pd.read_pickle("./backup2/"+f).reset_index(),
                    ignore_index=True)

matches2 = df_screened_output2.loc[
        df_screened_output2["criterea"].astype(str) == '[]',
        'index']

for i in df_screened_output.loc[df_screened_output['index'].isin(matches2),"index"]:
    j = list(df_screened_output.loc[df_screened_output['index'] == i,"criterea"])[0]
    j = [x for x in j if "Not Specific" not in x]
    df_screened_output.loc[
            df_screened_output['index'] == i,
            "criterea"]\
        = set(j)

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

# output new pickle for new screening round
df.to_pickle("Article_Table_Postscreening2.pkl")
df.to_excel("Article_Table_Postscreening2.xlsx")
df_screened_output.to_pickle("Output_Table_Postscreening2.pkl")
df_screened_output.to_excel("Output_Table_Postscreening2.xlsx")

df_screened_output.loc[df_screened_output['index'].isin(matches), :]\
.to_excel("Output_Table_Postscreening2_selection.xlsx")
