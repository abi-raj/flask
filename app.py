from flask import Flask,request
from bs4 import BeautifulSoup as bs
import requests



app = Flask(__name__)

@app.route('/api')

def hello_world():
    url="http://gen.lib.rus.ec/"
    #query = str(request.args['query'])
    #srch="search.php?req="+query+"&lg_topic=libgen&open=0&view=simple&res=100&phrase=1&column=def"
    #srch_url=url+srch
    #hdrs = {'User-Agent': 'Mozilla / 5.0 (X11 Linux x86_64) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 52.0.2743.116 Safari / 537.36'}
    resp = requests.get(url).content
    bsa=bs(resp,'html.parser')
    return str(bsa)
if __name__ == '__main__':
    app.run()
