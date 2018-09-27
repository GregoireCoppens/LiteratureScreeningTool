# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 19:59:08 2018

@author: gregoire
"""

import requests
import pandas as pd
import settings

count = 25
totalCount = 2527
NoTitleCount = 0
NoAbstractCount = 0
NoDoiCount = 0
NoPMIDCount = 0
NoPiiCount = 0

df = pd.DataFrame(columns=['DOI', 'PMID', 'PII',
                           'Title', 'abstract', 'link', 'Date',
                           'citedbycount'])
baseurl = "https://api.elsevier.com/content/search/scopus?"
api_key = settings.SCOPUS_apikey
insttoken = settings.SCOPUS_institutionkey
query = 'TITLE-ABS-KEY (("Medical Informatics" OR  "Algorithms"  OR  "Data Collection"  OR  "Automatic Data Processing" )  AND  ( "Intensive Care Units"  OR  "Critical Care" ) ) AND  PUBYEAR  >  2013  AND  PUBYEAR  <  2019'
for articleCount in range(0, totalCount, count):
    r = requests.get(baseurl +
                     "apikey=" + api_key +
                     "&insttoken=" + insttoken +
                     "&query=" + query +
                     "&httpaccept=application/json" +
                     "&count="+str(count) +
                     "&sort=coverDate" +
                     "&start=" + str(articleCount) +
                     "&view=COMPLETE"
                     )
    j_data = r.json()
    j_entry = j_data['search-results']["entry"]
    for i in j_entry:
        try:
            title = i["dc:title"]
        except KeyError:
            title = "n/a"
            NoTitleCount += 1

        try:
            abstract = i["dc:description"]
        except KeyError:
            abstract = "n/a"
            NoAbstractCount += 1

        try:
            link = i["link"][2]["@href"]
        except KeyError:
            link = "n/a"

        try:
            date = i["prism:coverDate"]
        except KeyError:
            date = "n/a"

        try:
            doi = i["prism:doi"]
        except KeyError:
            doi = "n/a"
            NoDoiCount += 1

        try:
            pmid = i["pubmed-id"]
        except KeyError:
            pmid = "n/a"
            NoPMIDCount += 1

        try:
            pii = i["pii"]
        except KeyError:
            pii = "n/a"
            NoPiiCount += 1

        try:
            citedbycount = i["citedby-count"]
        except KeyError:
            citedbycount = "n/a"

        df.loc[i["eid"]] = [
                doi, pmid, pii, title, abstract, link, date, citedbycount
                ]
print("\n", NoTitleCount, NoAbstractCount, "\n",
      NoDoiCount, NoPMIDCount, NoPiiCount, "\n",)
print("Total Results:", j_data["search-results"]["opensearch:totalResults"])


df.to_csv("Article_Table_SCOPUS.csv", encoding='utf-8')
df.to_pickle("Article_Table_SCOPUS.pkl")
