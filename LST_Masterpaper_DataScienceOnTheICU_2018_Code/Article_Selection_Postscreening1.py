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

# Change sets back into lists
crits = list(df_screened_output["criterea"])
for i in range(len(crits)):
    if type(crits[i]) == set:
        crits[i] = list(crits[i])
df_screened_output["criterea"] = crits

# remove duplicates from screener list
df_screened_output.drop_duplicates(subset="index", inplace=True)

# select articles that don't contain "not specific" or len>0
matches = df_screened_output.loc[
        (df_screened_output["criterea"].astype(str) != '[]')
        & (
                #(df_screened_output["criterea"].
           #astype(str).str.contains("Not Specific"))
        #| \
        (df_screened_output["criterea"].
           astype(str).str.contains("No ICU"))
        | (df_screened_output["criterea"].
           astype(str).str.contains("Different Language"))),
        'index']

df = df_all.loc[df_all['ID'].isin(matches), :]
# output new pickle for new screening round
df.to_pickle("Article_Table_Postscreening1.pkl")
df.to_excel("Article_Table_Postscreening1.xlsx")
df_screened_output.to_pickle("Output_Table_Postscreening1.pkl")
df_screened_output.to_excel("Output_Table_Postscreening1.xlsx")

df_screened_output_selection = df_screened_output\
    .loc[df_screened_output['index'].isin(matches), :]
