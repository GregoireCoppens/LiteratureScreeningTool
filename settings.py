# -*- coding: utf-8 -*-
# git update-index --assume-unchanged settings.py
# git fetch origin master
# git reset --hard

# LST Requirements:
Article_Table = "Article_Table.xlsx"  # columns: ID, Title, Text, pdf_name
screeners = "test, experiment"  # Elements to highlight in the text
filters_all = ["criteria 1", "criteria 2", "criteria 3", "criteria 4"]

# Display Settings
message_display = True
title_display = True
pdf_display = True

# Pubmed Requirements:
mail = '###'
pubmed_searchterm = '"Medical Informatics"[Mesh]'

# Web Of Science Requirements:
wos_auth_search = '###'
wos_auth_retrieve = '###'
wos_username = '###'
wos_pass = '###'
wos_query = 'TS=("Medical Informatics")'

# SCOPUS Requirements:
SCOPUS_apikey = '###'
SCOPUS_institutionkey = '###'
SCOPUS_query = 'TITLE-ABS-KEY ("Medical Informatics")'
