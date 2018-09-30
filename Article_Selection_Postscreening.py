# -*- coding: utf-8 -*-

# Setup
import pandas as pd
from os import walk

from itertools import chain
import numpy as np


# Define data frames
df_screened_output = pd.DataFrame(columns=['index', 'criteria', 'comments'])
df_screened_output['index'] = df_screened_output['index'].astype(str)

df_all = pd.read_excel("Article_Table.xlsx")
df_all["ID"] = df_all["ID"].astype(str)

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
            "criteria"]):
        all_screeners.extend(j)
    df_screened_output.loc[
            df_screened_output['index'] == i,
            "criteria"]\
        = set(all_screeners)
    all_comments = str()
    for j in list(df_screened_output.loc[
            df_screened_output['index'] == i,
            "comments"]):
        all_comments += j + "; "
    df_screened_output.loc[
            df_screened_output['index'] == i,
            "comments"]\
        = all_comments

# remove duplicates from screener list
df_screened_output.drop_duplicates(subset="index", inplace=True)

# Change all sets back into lists
crits = list(df_screened_output["criteria"])
for i in range(len(crits)):
    if type(crits[i]) == set:
        crits[i] = list(crits[i])
df_screened_output["criteria"] = crits
comments = list(df_screened_output["comments"])
for i in range(len(comments)):
    if type(comments[i]) == set:
        comments[i] = list(comments[i])
df_screened_output["comments"] = comments

# # select articles that don't contain exclusion criteria or are empty
# matches = df_screened_output.loc[
#         (df_screened_output["criteria"].astype(str) != '[]')
#         & ~(df_screened_output["criteria"].
#             astype(str).str.contains("Exclusion Criteria 1"))
#         & ~(df_screened_output["criteria"].
#             astype(str).str.contains("Exclusion Criteria 2"))
#         & ~(df_screened_output["criteria"].
#             astype(str).str.contains("Exclusion Criteria 3")),
#         'index']

# Bypass exclusion of articles
matches = list(df_screened_output.loc[:, 'index'])

# create final dataframe with the selection of IDs in matches
df = df_all.loc[df_all['ID'].isin(matches), :]

# Get all criteria in a list
crit_lst = list(set(
        chain.from_iterable(
            df_screened_output.loc[
                df_screened_output['index'].isin(matches),
                'criteria'])))

# Merge 2 dataframes to include criteria into df
df = pd.merge(df, df_screened_output,
              how="left", left_on=["ID"], right_on=["index"])
# Make a column vor every criteria
for i in crit_lst:
    df[i] = np.where(df['criteria'].astype(str).str.contains(i), True, False)

# Remove unused columns
df = df.drop(columns=["index", "criteria"])

# Select articles that have at least one of the included criteria
df = df.loc[df.iloc[:, 8:].any(axis=1)].reset_index(drop=True)

# output new pickle for new screening round
df.to_pickle("Article_Table_Postscreening.pkl")
df.to_excel("Article_Table_Postscreening.xlsx")
df_screened_output.to_pickle("Output_Table_Postscreening.pkl")
df_screened_output.to_excel("Output_Table_Postscreening.xlsx")
