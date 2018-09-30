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
- the last branch ("Analysis") analyses the output from the screening process and outputs the results as pkl files and xlsx tables 
  - Article_Selection_Postcreening.py (aggregates all the files in backup and removes duplicate values.)

It is possible to add your own "Article_Table.xlsx" file, by default it should have the following columns: "ID, Title, Text" .
It is also possible to change the provided "Article_Table.xlsx" file.

## PDFs

PDFs are accepted. You'll need to add them into the "pdf" folder and their names (without '.pdf') schould be added to the input table in the "pdf_file" column.

## Settings 

To retrieve the articles, you'll need specific API codes. These are not provided and can be required by contacting the corresponding customer services. 

The display settings can be adjusted in the settings.py file. By setting a display to True, it will be showed.

The name of an input file can be changed in the settings.py file, possible extensions are: ".xlsx", ".csv", ".pkl". The following column names are by default expected: ID, Title, Text, pdf_file ('pdf_file' is not required).

An empty settings file is provided where "###" needs to substituted with the corresponding values.

**All values (search queries, filenames, screening criterea, ...) can be adjusted in the settings file.**

## Python Libraries
Python libraries that need to be installed are:
- flask, pandas, numpy, Bio, requests, regex
- itertools, xml.etree.ElementTree, time, os 
