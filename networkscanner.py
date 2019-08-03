#--------------------------------------Urls And IP Scanning Module ----------------------------
#--------------------------------------Last Touched By: Amin Matola----------------------------
#--------------------------------------Last Touched On: 03/08/2019 ----------------------------


from flask import Flask, render_template,request,send_file
import urllib3 as urllib
import socket
from socket import *
from bs4 import BeautifulSoup
import requests
import time

app             = Flask(__name__)
app.secret_key  = "Non-seen"


def scan():
    if request.method=='GET':
        try:
            return render_template("scaner.html")
        except Exception as e:
            return "Error <hr>%s "%e
    area        = request.form['area']
    ip          = request.form['url']
    ports       = []
    f_ports     = [21,22,23,25,27,50,53,69,70,80,87, 88,109,110,113,143,1080,8080,8088]
    hosts       = []
    
    #------------------ No longer in use -----------------------------------
        # if ip[:4]   == 'http':
        #     parts   = ip.split('/')
        #     ip='www.%s'%parts[2]
    #-----------------------------------------------------------------------

    if ip[0].isdigit():
        addr    = 'ip'
    else:
        addr    = 'url'
    if area.lower()=='ip':
        if addr=='url':
            try:
                adr     = socket.gethostbyname(ip)
            except Exception as e:
                return render_template('scaner.html',error=True)
            return render_template('scaner.html', addr=addr,loc=ip,res=adr)
        else:
            try:
                adr     = socket.getfqdn(ip)
            except Exception as e:
                return render_template('scaner.html',error=True)
            return render_template('scaner.html', addr=addr,loc=ip,res=adr)

    elif area.lower()   =='name':
        try:
                adr     = socket.getfqdn(ip)
        except Exception as e:
                return render_template('scaner.html',error=True)
        return render_template('scaner.html', addr=addr,loc=ip,res=adr)

    elif area.lower()   == 'ports':
        s               = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        for port in f_ports:
            tes         = s.connect_ex((ip,port))
            if int(tes) == 0:
                hosts.append(port)
            time.sleep(0.001)
        if len(hosts)   <=  0:
            hosts       =  [0]
        return render_template('scaner.html',hosts = hosts)

    elif area.lower()   ==  'services':
        servs           = {}
        s               = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for port in f_ports:
            try:
                tes         = s.connect_ex((ip,port))
            except Exception as e:
                return "An error Occured:<hr>%s"%e
            try:
                serv        = socket.getservbyport(port)
            except:
                pass

            if int(tes)     ==  0:
                if not port in servs:
                    servs[port] = [serv,"running"]
            else:
                if not port in servs:
                    servs[port] = [serv,"not running"]

        return render_template('scaner.html',services=servs)




    return render_template('scaner.html',error=True)
