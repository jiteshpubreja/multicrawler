from flask.templating import render_template
from .cleaner import clean_en_pa
from nltk import sent_tokenize
from .crawler import singleCrawl, Crawl
from .script_scrapper2 import crawler, crawl_links
from dotenv import find_dotenv, load_dotenv
import os
import sqlite3
import uuid
import shutil
import time

load_dotenv(find_dotenv())

# window testing
import io
from flask import (Flask, jsonify, request, session, g, redirect,
                   url_for, abort, render_template, flash)


app = Flask(__name__)  # create the application instance


app.config.from_object(__name__)  # load config from this file , flaskr.py
app.config.update(
    # In order to use session in flask you need to set the secret key in your application settings.
    # Secret key is a random key used to encrypt your cookies and save, send them to the browser.
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
    # User Name and Password for Login Page saved then as session variale
    USERNAME='admin',
    PASSWORD='default',
    # EMAIL SETTINGS
)



# Crawler's Route Function
@app.route('/crawler', methods=['GET', 'POST'])
def crawler_fucroute():
    lang_tags = "af, ar, bg, bn, ca, cs, cy, da, de, el, en, es, et, fa, fi, fr, gu, he,hi, hr, hu, id, it, ja, kn, ko, lt, lv, mk, ml, mr, ne, nl, no, pa, pl, pt, ro, ru, sk, sl, so, sq, sv, sw, ta, te, th, tl, tr, uk, ur, vi, zh-cn, zh-tw"
    lang_tags = lang_tags.replace(" ",'')
    lang_tags = lang_tags.split(",")
    primary_lang = "primary_language"
    secondary_lang = "secondary_language"
    if request.method == 'POST':
        primary_lang = request.form["primary_lang"]
        secondary_lang = request.form['secondary_lang']
        link = request.form['link']
        if link == 'Link':
            link = request.form['choose']
    
        secondary_out, primary_out = crawler(link,primary_lang,secondary_lang)
        
        primary_out = sent_tokenize(primary_out)
        primary_out, secondary_out = clean_en_pa(primary_out, secondary_out.split('\n'),primary_lang,secondary_lang)
        # print(primary_out)
        web_links = crawl_links(link)
        
        # return render_template('input.html', link='link', web_links=web_links, pa_out=pa_out.split('\n'), en_out=en_out)
        return render_template('crawler.html', link='Link', web_links=web_links, secondary_out=lang_tags, primary_out=lang_tags, primary_langs = lang_tags, secondary_langs = lang_tags,primary_lang = primary_lang,secondary_lang=secondary_lang)
    return render_template('crawler.html', link='Link', secondary_langs = lang_tags, primary_langs = lang_tags, secondary_out='', primary_out='', web_links=['none'],primary_lang=primary_lang,secondary_lang=secondary_lang)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/single-crawl',methods = ['GET','POST'])
def single_crawler():
    if request.method == "POST":
        link = request.form["link"]
        if link == "Link":
            link = request.form["choose"]
        weblinks = Crawl(link).fetch_links()
        scrap = singleCrawl(link=link)
        return render_template('single-crawler.html',data = scrap, web_links = weblinks,link = "Link")

    return render_template('single-crawler.html',data="",web_links = ['none'],link = "Link")



@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


app.register_error_handler(500, internal_error)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

