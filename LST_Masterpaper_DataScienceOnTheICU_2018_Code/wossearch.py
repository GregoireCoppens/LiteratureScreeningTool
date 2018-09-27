# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 16:08:57 2018

@author: grego
"""
import requests
import xml.etree.ElementTree as ET
import time
import pandas as pd
import settings
###########


#Authenticate with server to get cookie
auth_url = "http://search.webofknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl"

auth_headers_search = {'Content-Type': 'text/xml',
           'charset': 'UTF-8',
           'Authorization':settings.wos_auth_search}
           
auth_headers_retrieve = {'Content-Type': 'text/xml',
           'charset': 'UTF-8',
           'Authorization':settings.wos_auth_retrieve}

auth_body = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
xmlns:auth="http://auth.cxf.wokmws.thomsonreuters.com">
  <soapenv:Header/>
  <soapenv:Body>
    <auth:authenticate/>
  </soapenv:Body>
</soapenv:Envelope>"""

auth_response = requests.post(auth_url, data=auth_body, headers=auth_headers_search)
#Only 5 requests in 5 minutes
#################


# Get ID's
cookie = auth_response.cookies.get_dict(domain='search.webofknowledge.com')  # cookie from authentication
url = "http://search.webofknowledge.com/esti/wokmws/ws/WokSearchLite?wsdl"
headers = {'Content-Type': 'text/xml',
               'charset': 'UTF-8'}
query = 'TS=(("Medical Informatics" OR "Algorithms" OR "Data Collection" OR "Automatic Data Processing") AND ("Intensive Care Units" OR "Critical Care"))'


full_id_list = list()
for i in range(0,5):  # in steps of 100, do to throtlling
    body = """<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
       xmlns:woksearchlite="http://woksearchlite.v3.wokmws.thomsonreuters.com">
       <soapenv:Header/>
       <soapenv:Body>
          <woksearchlite:search>
             <queryParameters>
                <databaseId>WOS</databaseId>
                <userQuery>TS=(("Medical Informatics" OR "Algorithms" OR "Data Collection" OR "Automatic Data Processing") AND ("Intensive Care Units" OR "Critical Care"))</userQuery>
                <timeSpan>
                   <begin>2014-01-01</begin>
                   <end>2018-12-31</end>
                </timeSpan>
                <queryLanguage>en</queryLanguage>
             </queryParameters>
             <retrieveParameters>
                <firstRecord>"""+ str(1+i*100) +"""</firstRecord>
                <count>100</count>
             </retrieveParameters>
          </woksearchlite:search>
       </soapenv:Body>
    </soapenv:Envelope>"""
    response = requests.post(url, data=body, headers=headers, cookies=cookie) #  request search results
    root = ET.fromstring(response.text) #  make elementree from response
    id_object_list = [item.find('uid') for item in root.findall('.//records')]  # get objects
    id_list = [item.text for item in id_object_list]  # get contents from objects
    full_id_list.extend(id_list)  # add to list
    time.sleep(5)

##################
# Retrieve abstracts
#http://ipscience-help.thomsonreuters.com/LAMRService/WebServiceOperationsGroup/requestAPIWoS/sampleRequestWoSCCCidentifiers.html
url_lamr = "https://ws.isiknowledge.com/cps/xrpc"
data_list = list()
totalcount = len(full_id_list)
count = 0
for i in full_id_list:
    count += 1
    body = """<?xml version="1.0" encoding="UTF-8" ?>
    <request xmlns="http://www.isinet.com/xrpc42" src="app.id=LST">
      <fn name="LinksAMR.retrieve">
        <list>
          <!-- WHO'S REQUESTING -->
          <map>   
            <val name="username">"""+settings.wos_username+"""</val>       
            <val name="password">"""+settings.wos_pass+"""</val>            
          </map>
          <!-- WHAT'S REQUESTED -->
          <map>
            <list name="WOS">
              <val>ut</val>
              <val>doi</val>
              <val>pmid</val>
              <val>sourceURL</val>
            </list>
          </map>
          <!-- LOOKUP DATA -->
          <map>
            <map name="cite_1">
              <val name="ut">"""+str(i)+"""</val>
            </map>      
          </map>
        </list>
      </fn>
    </request>"""

    lamr_response = requests.post(url_lamr, data=body)

    lamr_root = ET.fromstring(lamr_response.text) #  make elementree from
    ns = {'lamr' : 'http://www.isinet.com/xrpc42'}
    response
    article_data_dict = dict()
    for item in lamr_root.findall('.//lamr:val',ns):#define namespace
        article_data_dict[item.get('name')] = item.text
    data_list.append(article_data_dict)
    #get all elements into data table
        #https://docs.python.org/2/library/xml.etree.elementtree.html
    #add sleep function and remove dict limitation in for loop
    #Change app id
    print(str(round(count/totalcount*100,2))+'%')
    time.sleep(1)
df = pd.DataFrame.from_dict(data_list)

 # export
df.to_csv("Article_Table_WOS.csv", encoding='utf-8')
df.to_pickle("Article_Table_WOS.pkl")