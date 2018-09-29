# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import re
import settings

if settings.Article_Table.split(".")[1] == "csv":
    feed = pd.read_csv(settings.Article_Table).reset_index(drop=True)
if settings.Article_Table.split(".")[1] == "xlsx":
    feed = pd.read_excel(settings.Article_Table).reset_index(drop=True)
if settings.Article_Table.split(".")[1] == "pkl":
    feed = pd.read_pickle(settings.Article_Table).reset_index(drop=True)

columnnames = ["selection_criteria"] + ["comments"]
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
    'message': feed.loc[:, 'Text'],
    'message_display': 'block' if settings.message_display else 'none',
    'title': feed.loc[:, 'Title'],
    'title_display': 'block' if settings.title_display else 'none',
    'id': feed.loc[:, 'ID'],
    'message_screened': str(),
    'max': len(feed.loc[:, 'ID'])
}

try:
    data['pdf_name'] = feed.loc[:, 'pdf_name']
    data['pdf_display'] = 'block' if settings.pdf_display else 'none'
except KeyError:
    data['pdf_name'] = ["nan"]*len(feed.loc[:, 'ID'])

screeners = settings.screeners
filters_all = settings.filters_all


@app.route('/')
@app.route('/article_screener/')
def article_redirect():
    return redirect('/article_screener/0')


@app.route('/pdf/<pdf_name>', methods=["GET"])
def show_static_pdf(pdf_name):
    if pdf_name == "nan":
        return "No PDF Found"
    return send_file("./pdf/" + pdf_name + ".pdf")


@app.route('/article_screener/<int:article_count>', methods=["POST", "GET"])
def article_screener(article_count):
    global screeners, filters_all
    if request.method == "POST":
        if request.form['submit'] == "Next":
            output[data['id'][article_count]] = {
                    'criteria': request.form.getlist("filters_selected"),
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
                    'criteria': request.form.getlist("filters_selected"),
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
