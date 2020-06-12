from flask import Flask,request
from bs4 import BeautifulSoup as bs
import requests



app = Flask(__name__)



@app.route('/api',methods=['GET'])
def api():
    url="http://gen.lib.rus.ec/"
    query = str(request.args['query'])
    if " " in query:
        query = str(query).replace(" ","+")
    else: 
        pass
    srch="search.php?req="+query+"&lg_topic=libgen&open=0&view=simple&res=100&phrase=1&column=def"
    srch_url=url+srch
    return getbooklinks(srch_url)

def getbooklinks(srch_url):
    cont=requests.get(str(srch_url)).content
    bcont=bs(cont,'html.parser')
    l=[]
    a=0
    for i in bcont.find_all('tr'):
       l.append(i)
    return str(l)

        
if __name__ == '__main__':
    app.run()
