# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 22:32:07 2018

@author: gregoire
"""
# Set-up
import pandas as pd

# Create general data frame
df = pd.DataFrame(columns=['ID', 'PMID', 'DOI',
                           'Title', 'abstract',
                           'Pubmed', 'SCOPUS', 'WOS'])

# Import article databases
df_Pubmed = pd.read_pickle("Article_Table_Pubmed.pkl")
df_SCOPUS = pd.read_pickle("Article_Table_SCOPUS.pkl")
df_WOS = pd.read_pickle("Article_Table_WOS.pkl")

# extract all identifiers to memory (lowers computational cost)
Pubmed_PMID = list(df_Pubmed.loc[:, 'PMID'])
Pubmed_DOI = list(df_Pubmed.loc[:, 'DOI'])
SCOPUS_PMID = list(df_SCOPUS.loc[:, 'PMID'])
SCOPUS_DOI = list(df_SCOPUS.loc[:, 'DOI'])
WOS_PMID = list(df_WOS.loc[:, 'pmid'])
WOS_DOI = list(df_WOS.loc[:, 'doi'])

# Pubmed
for i in range(len(df_Pubmed)):
    # Get Data from db
    PMID = df_Pubmed.loc[i, 'PMID']
    DOI = df_Pubmed.loc[i, 'DOI']
    Title = df_Pubmed.loc[i, 'Title']
    abstract = df_Pubmed.loc[i, 'abstract']

    # Reset Booleans
    Pubmed = True
    SCOPUS = False
    WOS = False
    DOI_State = False
    PMID_State = False

    # Check if DOI or Pubmed ID is not n/a and define unique_ID
    if len(DOI) > 4:
        DOI_State = True
        ID = DOI
    if len(PMID) > 4:
        PMID_State = True
        if not DOI_State:
            ID = PMID
    if not (PMID_State or DOI_State):
        ID = 1 + len(df)

    # Check in what other databases the PMID or the DOI are present
    if (PMID in SCOPUS_PMID) and PMID_State:
        SCOPUS = True
    if (DOI in SCOPUS_DOI) and DOI_State:
        SCOPUS = True

    if (PMID in WOS_PMID) and PMID_State:
        WOS = True
    if (DOI in WOS_DOI) and DOI_State:
        WOS = True

    # Write data to dataframe
    df.loc[i] = [ID, PMID, DOI, Title, abstract, Pubmed, SCOPUS, WOS]

# SCOPUS
for i in range(len(df_SCOPUS)):
    # Get Data from db
    PMID = df_SCOPUS.iloc[i, 1]
    DOI = df_SCOPUS.iloc[i, 0]
    Title = df_SCOPUS.iloc[i, 3]
    abstract = df_SCOPUS.iloc[i, 4]

    # Reset Booleans
    Pubmed = False
    SCOPUS = True
    WOS = False
    DOI_State = False
    PMID_State = False

    # Check if DOI or Pubmed ID is not n/a and define unique_ID
    if len(DOI) > 4:
        DOI_State = True
        ID = DOI
    if len(PMID) > 4:
        PMID_State = True
        if not DOI_State:
            ID = PMID
    if not (PMID_State or DOI_State):
        ID = 1 + len(df)

    # Check duplicates in other databases and write to dataframe.
    if(
       ((PMID not in Pubmed_PMID) and PMID_State) and
       ((DOI not in Pubmed_DOI) and DOI_State)):
        if (PMID in WOS_PMID) and PMID_State:
            WOS = True
        if (DOI in WOS_DOI) and DOI_State:
            WOS = True
        df.loc[len(df)] = [ID, PMID, DOI, Title, abstract, Pubmed, SCOPUS, WOS]
    if (not PMID_State) and ((DOI not in Pubmed_DOI) and DOI_State):
        if (DOI in WOS_DOI) and DOI_State:
            WOS = True
            df.loc[len(df)] = [ID, PMID, DOI, Title, abstract, Pubmed, SCOPUS, WOS]
    if ((PMID not in Pubmed_PMID) and PMID_State) and (not DOI_State):
        if (PMID in WOS_PMID) and PMID_State:
            WOS = True
        df.loc[len(df)] = [ID, PMID, DOI, Title, abstract, Pubmed, SCOPUS, WOS]
    if (not PMID_State) and (not DOI_State):
        df.loc[len(df)] = [ID, PMID, DOI, Title, abstract, Pubmed, SCOPUS, WOS]

# WOS
for i in range(len(df_WOS)):
    PMID = str(df_WOS.loc[i, 'pmid'])
    DOI = str(df_WOS.loc[i, 'doi'])
    Title = "not applicalbe"
    abstract = df_WOS.loc[i, 'sourceURL']

    Pubmed = False
    SCOPUS = False
    WOS = False
    DOI_State = False
    PMID_State = False

    if len(DOI) > 4:
        DOI_State = True
        ID = DOI
    if len(PMID) > 4:
        PMID_State = True
        if not DOI_State:
            ID = PMID
    if not (PMID_State or DOI_State):
        ID = len(df)

    # Check duplicates in other databases
    if (PMID not in Pubmed_PMID) and (PMID not in SCOPUS_PMID) and PMID_State:
        if (DOI not in Pubmed_DOI) and (DOI not in SCOPUS_DOI) and DOI_State:
            WOS = True
    if not PMID_State:
        if (DOI not in Pubmed_DOI) and (DOI not in SCOPUS_DOI) and DOI_State:
            WOS = True
    if not DOI_State:
        if (PMID not in Pubmed_PMID) and (PMID not in SCOPUS_PMID) and PMID_State:
            WOS = True
    if (not PMID_State) and (not DOI_State):
        WOS = True

    # Write to dataframe if article is unique to WOS
    if WOS:
        df.loc[len(df)] = [ID, PMID, DOI, Title, abstract, Pubmed, SCOPUS, WOS]

#Convert Abstracts from lists to texts
def text_concat(list_text):
    list_text_new = list()
    for text in list_text:
        if len(text) > 1:
            text_conc = str()
            for i in text:
                try:
                    attr_i = i.attributes["Label"]
                    text_conc += attr_i + ": " + i + "<br><br>"
                except AttributeError:
                    text_conc += i
                text = text_conc
        elif len(text) == 1:
            text = text[0]
        if text[:4] == "http":  # If text is a link
            text = '<a href="'+text+'"target="_blank">Link</a>'
        list_text_new.append(text)
    return list_text_new

df["abstract"] = text_concat(df["abstract"])

# export
df.to_pickle("Article_Table.pkl")
df.to_excel("Article_Table.xlsx")

# Bell sound to notify when script is ready
print('\007')
