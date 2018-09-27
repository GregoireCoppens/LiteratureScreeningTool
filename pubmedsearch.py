# Source/inspiration : https://marcobonzanini.com/2015/01/12/searching-pubmed-with-python/

import pandas as pd
from Bio import Entrez
import settings
retmax = 9999  # Maximum articles retrieved
searchterm = settings.pubmed_searchterm


def search(query):
    Entrez.email = settings.mail
    handle = Entrez.esearch(db='pubmed',  # database
                            sort='pub+date',  # sort on publication date instead of 'relevance' 
                            retmax=retmax,  # max retrieved results
                            retmode='xml',  # retrieved type
                            term=query,  # search term
                            datetype='pdat')  # publication date
    results = Entrez.read(handle)
    return results


def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = settings.mail
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results


if __name__ == '__main__':
    # Define Variables:
    df = pd.DataFrame(columns=["PMID", 'DOI', 'ID_List', 'Title', 'abstract'])  # iniate the dataframe

    results = search(searchterm)  # search
    results_id_list = results['IdList']  # get ids from search results
    papers = fetch_details(results_id_list)  # get details from id list

    NoDoiCount = 0
    PMIDCount = 0
    NoTitleCount = 0
    NoAbstractCount = 0

    # Run Through articles and get Title, Abstract and DOI:
    for i in range(len(papers["PubmedArticle"])):
        # define variables
        title = Entrez.Parser.StringElement()
        abstract = Entrez.Parser.StringElement()  # abstract can also be multiple stringElements in a list
        NoDoi = True
        doi = str()
        pmid = str()
        doiList = list()
        
        #try to get the title and abstract from the article
        try:
            title = papers["PubmedArticle"][i]['MedlineCitation']['Article']['ArticleTitle']
        except KeyError:
##            print("Title not available.")
            NoTitleCount += 1

        try:
            abstract = papers["PubmedArticle"][i]['MedlineCitation']['Article']['Abstract']["AbstractText"]
        except KeyError:
##            print("Abstract not available.")
            NoAbstractCount += 1

        # Run through the list with IDTypes to find a DOI and the PMID.
        for j in range(len((papers["PubmedArticle"][i]['PubmedData']['ArticleIdList']))):
            doiList = papers["PubmedArticle"][i]['PubmedData']['ArticleIdList']
            if(papers["PubmedArticle"][i]['PubmedData']['ArticleIdList'][j].attributes['IdType']=="doi"):  # DOI
                doi = papers["PubmedArticle"][i]['PubmedData']['ArticleIdList'][j].strip()
                NoDoi = False
            elif(papers["PubmedArticle"][i]['PubmedData']['ArticleIdList'][j].attributes['IdType']=="pubmed"):#PMID
                PMIDCount += 1
                pmid = papers["PubmedArticle"][i]['PubmedData']['ArticleIdList'][j].strip()

        # If no doi is available take the first one from the list and make a unique id.
        if(NoDoi):
            ##print(title+"\n")
            NoDoiCount += 1
            #doi = "NoDOI/"+papers["PubmedArticle"][i]['PubmedData']['ArticleIdList'][0].attributes['IdType'] +"/"+ papers["PubmedArticle"][i]['PubmedData']['ArticleIdList'][0].strip()
##            print("No DOI found: " + str(doi))

        # Put information of article in data frame
        df.loc[i] = [pmid, doi, doiList, title, abstract]

    # Report
    print("The search term was: " + searchterm)
    print("There are " + str(len(papers["PubmedArticle"])) + " Articles found (max:"+str(retmax)+")")
    print("There are "+str(NoDoiCount)+" articles without a DOI")
    print(str(PMIDCount) + " Articles do have a PMID")
    print("There are "+str(NoTitleCount)+" articles without a Title")
    print("There are "+str(NoAbstractCount)+" articles without a Abstract")

    # export
    df.to_csv("Article_Table_Pubmed.csv", encoding='utf-8')
    df.to_pickle("Article_Table_Pubmed.pkl")
