# -*- coding: utf-8 -*-
"""
Created on Sat May 26 20:52:18 2018

@author: gregoire
"""
from flask import Flask, render_template, request, redirect
import pandas as pd
import re

#feed = pd.read_pickle("Article_Table.pkl")
#feed = pd.read_pickle("Article_Table_Postscreening1.pkl").reset_index(drop=True)
#feed = pd.read_pickle("Article_Table_Postscreening2.pkl").reset_index(drop=True)
#feed = pd.read_pickle("Article_Table_Postscreening3.pkl").reset_index(drop=True)
#feed = pd.read_pickle("Article_Table_Postscreening4.pkl").reset_index(drop=True)
feed = pd.read_pickle("Article_Table_Postscreening5.pkl").reset_index(drop=True)

columnnames = ["selection_criterea"] + ["comments"]
output = dict()

app = Flask(__name__)


def text_screening(text, screeners_list):
    for s in screeners_list:
        if s != "" and s != " ":
            text = re.compile(re.escape(s), re.IGNORECASE).sub(
                    "<mark  style='background-color: yellow'>"+s+"</mark>",
                    text)
    return text


data = {
    'message': feed.iloc[:, 4],
    'title': feed.iloc[:, 3],
    'id': feed.iloc[:, 0],
    'message_screened': str(),
    'max': len(feed.iloc[:, 0])
}

screeners = "data, ICU , collect, analy, store, critical, intensive"

filters_all = ["Data Collection", "Data Storage", "Data Analyses",
               "No ICU", "Not Specific", "Different Language"]
filters_all = ["Waveform data", "Physiological Data", "EEG", "Multi-Parameter Monitoring", "Glucose Monitoring", "Monitors", "Administrative data", "Electronic Health Records", "Data Mining", "Smart devices", "Software", "Scoring Systems",
               "Databases",
               "Predictive Analytics", "Deep Learning", "Natural Language processing", "Adaptive Modeling", "Classification Algorithms", "Telemedecine", "Alarm Fatigue",  "Video Assisted", "Arden Syntax","Real Time Processing", "Clinical Decision Support System", 
               "Big Data",  "Data Quality", "Data Reporting", "General",
               "No ICU", "Not Specific", "Different Language"]


@app.route('/')
@app.route('/article_screener/')
def article_redirect():
    return redirect('/article_screener/0')


@app.route('/article_screener/<int:article_count>', methods=["POST", "GET"])
def article_screener(article_count):
    global screeners, filters_all
    if request.method == "POST":
        if request.form['submit'] == "Next":
            output[data['id'][article_count]] = {
                    'criterea': request.form.getlist("filters_selected"),
                    'comments': request.form["comments"]
                    }
            pd.DataFrame.from_dict(output, orient='index')\
                .to_pickle('output.pkl')
            screeners = request.form["screeners"]
            article_count += 1
        elif request.form['submit'] == "Refresh":
            screeners = request.form["screeners"]
        elif request.form['submit'] == "Back":
            output[data['id'][article_count]] = {
                    'criterea': request.form.getlist("filters_selected"),
                    'comments': request.form["comments"]}
            pd.DataFrame.from_dict(output, orient='index')\
                .to_pickle('output.pkl')
            screeners = request.form["screeners"]
            article_count -= 1

    if article_count <= (len(data['title'])-1):
        data['message_screened'] = text_screening(
                data['message'][article_count],
                screeners.split(", ")
                )
        return render_template(
                "article_screener.html",
                data=data, filters_all=filters_all,
                screeners=screeners,
                count=article_count,
                output=output
                )
    else:
        article_count = 0
        return "Finished"


if __name__ == "__main__":
    app.run(debug=False)
