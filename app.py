from flask import Flask,request,jsonify,Response
from bs4 import BeautifulSoup as bs
import requests as rq
import numpy as np
import cv2
import os
app = Flask(__name__)
baseUrl = "https://www.unblockweb.uno/?cdURL="
#LIBGEN
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
    for i in bscnt.find_all('div',{'class':'resItemBox exactMatch'}):
        for ii in i.find_all('a',href=True):
            
            if ii['href'].startswith("book"):
                stringLink = "http://m.bookfi.net/" + ii["href"]
                #print(stringLink)
                bookLink.append(stringLink)
          

    for j in bscnt.find_all('div',{'class':'resItemBox exactMatch'}):
        for k in j.find_all('h3'):
            bookTitle.append(j.text)

    for j in bscnt.find_all('div',{'class':'resItemBox exactMatch'}): 
        for k in j.find_all('a',target="_blank",href=True):
            if k['href'].startswith("http://book"):
                bookDownload.append(k['href'])
            
    
    for j in bscnt.find_all('div',{'class':'resItemBox exactMatch'}):
        if not j.find_all('span',itemprop='inLanguage'):
            lang="NA"
            
        else:
            for k in j.find_all('span',itemprop='inLanguage'):
                lang=k.text
        bookLanguage.append(lang)
   
                
        

    for j in bscnt.find_all('div',{'class':'resItemBox exactMatch'}):
        if not j.find_all('a',itemprop="author"):
            art="NA"
            
        else:
            for k in j.find_all('a',itemprop="author"):
                art=j.text
                pass
        bookArthur.append(art)
        
    
    #print(bookTitle)
    #print(bookLanguage)
    
    print(len(bookLink))
    print(len(bookTitle))
    print(len(bookArthur))
    print(len(bookLanguage))
    print(len(bookDownload))
    
    
    for c in range(len(bookTitle)):
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



#Tamil Yogi API
@app.route('/tyS',methods=['GET'])

def f():
    query=str(request.args['q'])
    if " " in query:
        query = str(query).replace(" ","+")
    url="http://tamilyogi.cool/?s="+query
    cont=rq.get(url).content
    bscnt=bs(cont,'html.parser')

    imgL=[]
    titL=[]
    linkL=[]
    tit=[]
    vidL=[]
    
    for div in bscnt.find_all('div',id='archive'):
        img=div.find_all('img')
        for im in img:
            imgL.append(str(im['src']))
      
        an=div.find_all('a')
        prev=""
        for anc in div.find_all('a'):
            if prev!=anc['href']:
                linkL.append(anc['href'])
                prev=(anc['href'])
        for anc in div.find_all('a'):
            tit.append(anc.text)
    while("" in tit):
        tit.remove("")
    for t in tit:
        last=t.find(')')
        titL.append((t[:(last+1)]))
        
        
    vidL=video(linkL)
    lis=[]
    for i in range(len(imgL)):
        movies={}
        movies['title']=titL[i]
        movies['image']=imgL[i]
        #movies['link']=linkL[i]
        movies['video']=vidL[i]
        
        lis.append(movies)

    mlist={}
    mlist['movies']=lis
    return jsonify(mlist)

def video(link):
    mlis=[]
    for lin in link:
        
        url=lin
        headers_mobile = { 'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}
        cont=rq.get(url,headers=headers_mobile).content
        bscnt=bs(cont,'html.parser')
        ifr=bscnt.find_all('iframe')[1]
        mlis.append(ifr['src'])
    #print(ifr['src'])
    #vid={}
    #vid['link']=(ifr['src'])
    #print(mlis)
    return mlis

@app.route('/tyD',methods=['GET'])
def download():
    url=str(request.args['q'])
    if url.startswith('http://vidorg.net/'):
        headers_mobile = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'}
        ca=rq.get(url,headers=headers_mobile).content
        cc=bs(ca,'html.parser')
        c = cc.find_all('script')[7]
        
        cha=(str(c)[91:700])

        cha="".join(cha.split())
    

        fi=cha.find('{')
        li=cha.rfind(']')


        var=cha[fi:(li+1)].split('"')

        lis1=[a for a in var if a.endswith('.mp4')]
        lis2=[a for a in var if a.endswith('p') and len(a)<5]
    
        formT = {lis2[i]: lis1[i] for i in range(len(lis1))}
        
        
    else:
        formT={}
        formT['noVid']="No Links"
            
    form=[]
    form.append(formT)
    forn={}
    forn["link"]=form
    #print(form)
    return jsonify(forn)


#YTSwrapper

def ytsEncode(url):
    if '?' in url:
        url = url.replace('?', '%3F')
    if '&' in url:
        url = url.replace('&', '%26')
    if '/' in url:
        url = url.replace('/', '%2F')
    if ':' in url:
        url = url.replace(':', '%3A')
    if '=' in url:
        url = url.replace('=', '%3D')

    # print(url)

    return url
@app.route("/yts/movie_suggestions")
def suggestions():
    movie_id = request.args.get('movie_id')

    url = "https://yts.mx/api/v2/movie_suggestions.json?movie_id=" + str(movie_id)
    url = baseUrl + str(ytsEncode(url))

    response = rq.request("GET", url)
    data = response.json()

    return data


@app.route("/yts/movie_details")
def detail():
    movie_id = request.args.get('movie_id')
    with_cast = request.args.get('with_cast')
    with_images = request.args.get('with_images')

    with_cast = 'true' if (with_cast is not None and with_cast == 'true') else 'false'
    with_images = 'true' if (with_images is not None and with_images == 'true') else 'false'

    url = "https://yts.mx/api/v2/movie_details.json?movie_id=" + movie_id + "&with_cast=" + with_cast + "&with_images=" + with_images
    

    url = baseUrl + str(ytsEncode(url))
    response = rq.request("GET", url)
    data = response.json()

    return data


@app.route("/yts/list_movies")
def lists():
    limit = request.args.get('limit')
    page = request.args.get('page')
    quality = request.args.get('quality')
    minimum_rating = request.args.get('minimum_rating')
    query_term = request.args.get('query_term')
    genre = request.args.get('genre')
    sort_by = request.args.get('sort_by')
    order_by = request.args.get('order_by')
    with_rt_ratings = request.args.get('with_rt_ratings')

    # check

    limit = '20' if limit is None else limit
    page = '1' if page is None else page
    quality = 'all' if quality is None else quality
    minimum_rating = '0' if minimum_rating is None else minimum_rating
    query_term = '0' if query_term is None else query_term
    genre = 'all' if genre is None else genre
    sort_by = 'date_added' if sort_by is None else sort_by
    order_by = 'desc' if order_by is None else order_by
    with_rt_ratings = 'true' if (with_rt_ratings is not None and with_rt_ratings == 'true') else 'false'

    url = "https://yts.mx/api/v2/list_movies.json?limit=" + (
        limit) + "&page=" + page + "&minimum_rating=" + minimum_rating + "&query_term=" + query_term + "&quality=" + quality + "&genre=" + genre + "&sort_by=" + sort_by + "&order_by=" + order_by + "&with_rt_ratings=" + with_rt_ratings
    
    url = baseUrl + str(ytsEncode(url))
    response = rq.request("GET", url)
    data = response.json()

    return data

@app.route("/yts/img")
def movieimg():

    imgURL = request.args.get('imgURL')
    url = baseUrl + str(ytsEncode(imgURL))
    cont = rq.get(url).content
    return cont,{"Content-Type":"image/jpeg"}



def image_from_buffer(file_buffer):
    '''
    If we don't save the file locally and just want to open
    a POST'd file. This is what we use.
    '''
    bytes_as_np_array = np.frombuffer(file_buffer.read(), dtype=np.uint8)
    flag = 1
    # flag = 1 == cv2.IMREAD_COLOR
    # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
    frame = cv2.imdecode(bytes_as_np_array, flag)
    return frame

def get_face_cascade(cascade='haarcascade_frontalface_default.xml'):
    #print(os.path.join(cv2.data.haarcascades, cascade))
    return os.path.join(cv2.data.haarcascades, cascade)

def faces_from_frame(frame, save=True, destination=None):
    '''
    This is will extract all faces found in an image
    And save the faces (just the face) as a unique file
    in our destination folder.
    '''
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cascade_xml = get_face_cascade()
    cascade = cv2.CascadeClassifier(cascade_xml)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=4)
    return len(faces)

@app.route('/api/face', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return {"detail": "No file found"}, 400
        file = request.files['file']
        if file.filename == '':
            return {"detail": "Invalid file or filename missing"}, 400
        frame = image_from_buffer(file)
        l=faces_from_frame(frame)
        return {"faces":l}

if __name__ == "__main__":
    app.run()
