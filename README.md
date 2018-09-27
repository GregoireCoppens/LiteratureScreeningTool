# LiteratureScreeningTool 

## Goal 

The Literature Screening Tool (LST) is a set of tools that can be helpful to screen academic literature for literature studies in a systematic and reproducible way.

## Branches 

The tool consists of 3 branches:  
- the first branch ("Retrieval") retrieves all the articles 
  - pubmedsearch.py
  - SCOPUSsearch.py
  - wossearch.py
  - merging_article_tables.py
- the second branch ("Screening") screens the articles in a flask app.
  - LST.py (screening flask app)
  - output_manager (saves output from LST.py into backup, needs to be run every time LST.py is stopped)
  - Article_Table.xlsx (Example file that could come out of the retrieval branch)
- the last branch ("Analysis") analyses the output from the screening process and outputs the results as pkl files or xlsx tables 
  - Article_Selection_Postcreening.py (aggregates all the files in backup and removes duplicate values.)

It is possible to add your own "Article_Table.xlsx" file, by default it should have the following columns: "ID, Title, Text" .

## Settings 

To retrieve the articles, you'll need specific API codes. These are not provided and can be required by contacting the corresponding customer services. 

An empty settings file will be provided where "###" needs to substituted with the corresponding values.

All values (search queries, filenames, screening criterea, ...) can be adjusted in the settings file.

## Python Libraries
Python libraries that need to be installed are:
- flask, pandas, numpy, Bio, requests, regex
- itertools, xml.etree.ElementTree, time, os 
