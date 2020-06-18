from flask import Flask,request,jsonify
from bs4 import BeautifulSoup as bs
import requests as rq
app = Flask(__name__)


@app.route('/api',methods=['GET'])
def libgen():
    url="http://gen.lib.rus.ec/"
    qgiven = str(request.args['query'])
    if " " in qgiven:
        qgiven = str(qgiven).replace(" ","+")
    else:
        pass
    srch="search.php?req="+qgiven+"&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def"
    srch_url=url+srch
    return getbooklinks(srch_url)    
def getbooklinks(srch_url):
    cont=rq.get(str(srch_url)).content
    l=[]
    pcont=bs(cont,'html.parser')
    a=0
    count=0
    for i in pcont.find_all('tr'):
        if a==0 or a==1 or a==2 :
            a=a+1
            pass
        else:
            b=0
            for g in i.find_all('td'):
                #1st 'td' has the ARTHOR
                if b==1:
                    arthr=g.text
                #2nd 'td' has the BOOK TITLE
                if b==2:
                    btitl=g.text
                    btitle="".join(filter(lambda x: not x.isdigit(), btitl))
                    btitle=btitle.replace(",","")
                    btitle=btitle.replace("-"," ")
                    btitle=btitle.replace("  ","")
                    
                if b==3:
                    bpub=g.text
                    if len(bpub)==0:
                        bpub='NA'
                if b==4:
                    byear=g.text
                if b==5:
                    bpages=g.text
                if b==6:
                    blan=g.text
                if b==7:
                    bsize=g.text
                if b==8:
                    bformat=g.text
                #9th 'td' has the LINK
                if b==9:
                    for h in g.find_all('a',href=True):
                        count=count+1
                        c={}
                        c['index']=len(l)
                        c['Arthor']=arthr
                        c['link']=h['href']
                        #dd=c['link']
                        #c['image']= img(dd)
                        c['Title']=btitle
                        c['Publisher']=bpub
                        c['Year']=byear
                        c['Total Pages']=bpages
                        c['Language']=blan
                        c['Size']=bsize
                        c['Format']=bformat
                        #print(c)
                        l.append(c)
                    #print("total",count)    
                    b=b+1
                else:
                    b=b+1
                    pass

    data={}
    data['data']=l
    return jsonify(data)

@app.route('/book',methods=['GET'])

def book():
    link = str(request.args['link'])
    lis=[]
    icnt=0
    b=0
    cont=rq.get(link).content
    bcont=bs(cont,'html.parser')
    
    for i in bcont.find_all('div'):
        if icnt == 0:
            for j in i.find_all('img',src=True):
                imgli="http://93.174.95.29"+j['src']
            break

    c=0
    for w in bcont.find_all('p'):
        if c==2:
            isbn=w.text
            break
        c=c+1
    for a in bcont.find_all('td'):
        if b==1:
            for ab in (a.find_all('h2')):
                for abc in ab.find_all('a',href=True):
                    fileLink={}
                    fileLink['File']=abc['href']
                    fileLink['Image']=imgli
                    fileLink['ISBN']=isbn
                    
            break
        b=b+1
    book={}
    book["data"]=fileLink
    return jsonify(book)

#BookFi Sources
@app.route('/bookfi/image',methods=['GET'])
def getimage():
    image={}
    link=str(request.args['link'])
    imgCont=rq.get("http://m.bookfi.net/"+ link).content
    imgBscnt=bs(imgCont,'html.parser')
    for img in imgBscnt.find_all('img') :
        image['jpg']=img['src']
    if len(image) ==0:
        image['jpg']="https://cdn.bookauthority.org/dist/images/book-cover-not-available.6b5a104fa66be4eec4fd16aebd34fe04.png"
    return jsonify(image)

@app.route('/bookfi',methods=['GET'])
def bookfi():
    query=str(request.args['query'])
    bookLink=[]
    bookTitle=[]
    bookArthur=[]
    bookLanguage=[]
    bookDownload=[]
    
    data=[]
    
    if " " in query:
        query = str(query).replace(" ","+")
    cont=rq.get("http://en.bookfi.net/s/?q="+query+"&t=0").content
    bscnt=bs(cont,'html.parser')
   
    a=0

    id=bscnt.find(id="searchResultBox")
    for i in id.find_all('div',style="width:650px; float:left;"):
        for ii in i.find_all('a',href=True):
            #if a%5==0 :
            if ii['href'].startswith("book"):
                stringLink = "http://m.bookfi.net/" + ii["href"]
                #print(stringLink)
                bookLink.append(stringLink)
            a=a+1

    for j in bscnt.find_all('h3'):
        #print(j.text)
        bookTitle.append(j.text)
        
    for k in bscnt.find_all('a',target="_blank",href=True):
        if k['href'].startswith("http://book"):
            bookDownload.append(k['href'])

    for l in bscnt.find_all('span',itemprop='inLanguage'):
        #print(l.text)
        bookLanguage.append(l.text)

    for m in bscnt.find_all('a',itemprop="author"):
        if m.text != "" and m.text != "img":
            bookArthur.append(m.text)
  
    for c in range(90):
        books={}
        books['Title']=bookTitle[c]
        books['Arthur']=bookArthur[c]
        books['Language']=bookLanguage[c]
        books['Link']=bookLink[c]
        books['Download']=bookDownload[c]
        data.append(books)
            

    bookFi={}
    bookFi["books"]=data
    return jsonify(bookFi)

#Z-Library Popular
@app.route('/zlib/popular')
def popularImages():
    popImage=[]
    popLink=[]
    jsonArray=[]
    count=0
    cont=rq.get("https://b-ok.asia/popular.php").content
    bsc=bs(cont,'html.parser')
    for i in bsc.find_all('img',src=True):
        popImage.append(i['src'])  
    for i in bsc.find_all('a',href=True):
        if i['href'].startswith('/book/'):
            popLink.append("https://b-ok.asia"+i['href'])
    for index in range(len(popImage)):
        popBooks={}
        popBooks['images']=popImage[index]
        popBooks['link']=popLink[index]
        jsonArray.append(popBooks)
    data={}
    data['data']=jsonArray
    return jsonify(data)


if __name__ == "__main__":
    app.run()
