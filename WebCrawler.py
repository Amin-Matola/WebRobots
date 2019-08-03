#--------------------------Module for scraping the Web ---------------------------------|
#--------------------------Last Touched By: Amin Matola---------------------------------|
#--------------------------Last Touched On: 03/08/2019 ---------------------------------|

from flask import Flask, render_template,request,send_file
import urllib3 as urllib
#import urllib
import socket
from socket import *
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.config          = {"DEBUG":False,"UPLOAD_FOLDER":"path/to/uploads"}
app.secret_key      = "secret"


@app.route('/')
def hello_world():
    return render_template("Crawler.html")


@app.route('/scrape',methods=['GET','POST'])
def scrape():
    if request.method=='GET':
        return render_template('scraper.html')
    
    #------------------------------------No more in use ------------------------------------
        #cj          = CookieJar()
        # opener      = urllib.request.build_opener()
        # opener.addheaders=[('User-agent','Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]
    #----------------------------------------------------------------------------------------
    link        = request.form['location']
    links       = []
    divs        = []
    images      = []
    videos      = []
    audios      = []
    tag         = request.form['tag'].lower()
    try:
        html        = requests.get(link).text
    except Exception as e:
        error       = 'Sorry, error %s'%e
        return render_template('scraper.html',error=error,url=link)
    try:
        soup        = BeautifulSoup(html,'html')
        #return str([a.get('href') for a in soup.findAll('a')])
    except Exception as e:
        return "Error <hr>%s"%e
    if tag=='a':
        for a in soup.findAll('a'):
            data    = a.get('href')
            if data[0:3].lower() != 'http':
                if data[0] != r'/':
                    lin=link.split('/')
                    data = '%s/%s'%(lin[0]+'//'+lin[2],data)
                else:
                    data = '%s%s'%(lin[0]+'//'+lin[2],data)
            if data not in links:
                links.append(data)


        return render_template('scraper.html',data=links,url=link,choice=tag,name="Links")

    elif tag=='div':
        for d in soup.findAll('div'):
            divs.append(d.text)
        return render_template('scraper.html',divs=divs,url=link,choice=tag,name='Paragraphs')

    elif tag=='img':
        for a in soup.findAll('img'):
            data    = a.get('src')
            if data[0:3].lower() != 'http':
                if data[0] != r'/':
                    lin=link.split('/')
                    data = '%s/%s'%(lin[0]+'//'+lin[2],data)
                else:
                    lin=link.split('/')
                    data = '%s%s'%(lin[0]+'//'+lin[2],data)
            images.append(data)
        return render_template('scraper.html',images=images,url=link,choice=tag,name="Images")

    elif tag=='audio':
        for a in soup.findAll('audio'):
            data    = a.get('src')
            if data[0:3].lower() != 'http':
                if data[0] != r'/':
                    lin=link.split('/')
                    data = '%s/%s'%(lin[0]+'//'+lin[2],data)
                else:
                    lin=link.split('/')
                    data = '%s%s'%(lin[0]+'//'+lin[2],data)
            audios.append(data)
        return render_template('scraper.html',audios=audios,url=link,choice=tag,name="Music")

    elif tag=='video':
        for a in soup.findAll('video'):
            data    = a.get('src')
            if data[0:3].lower() != 'http':
                if data[0] != r'/':
                    lin=link.split('/')
                    data = '%s/%s'%(lin[0]+'//'+lin[2],data)
                else:
                    lin=link.split('/')
                    data = '%s%s'%(lin[0]+'//'+lin[2],data)
            videos.append(data)
        return render_template('scraper.html',videos=images,choice=tag,name="Videos")

    error='The thing you are looking for is not implemented yet!'
    return render_template('scraper.html',error=error,url=link)
