#coding:utf-8
import re
import requests
import json
import os
from bs4 import BeautifulSoup


def get_page_content(url):
    # headers = {
    #     'Referer': ' https: // www.google.com.hk /',
    #     'Upgrade - Insecure - Requests': '1',
    #     'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8',
    #     'Accept - Encoding': 'gzip, deflate, sdch',
    #     'Accept - Language': 'zh - CN, zh;q = 0.8',
    #     'Cache - Control': 'max - age = 0',
    #     'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 51.0.2704.84Safari / 537.36'
    # }
    html = requests.get(url)
    print (html.status_code)
    return html.content

def get_book_page(home_html_content):
    html = re.findall('class=\"nbg\" href=\"(.*?)\"',home_html_content)
    return html

def get_book_info(book_page_content):
    book_info = {'title':"",
                 'author':"",
                 'press':"",
                 'translator':"",
                 'ISBN':"",
                 'publicationDate':"",
                 'pages':"",
                 'price':"",
                 'briefIntroduction':"",
                 'authorIntroduction':""
                 }
    try:
        book_info['title'] = re.findall("title=\"点击看大图\" alt=\"(.*?)\"",book_page_content)[0]
    except:
        book_info['title'] = re.findall("<title>(.*?)(豆瓣)</title>",book_page_content)[0]
    try:
        book_info['author'] = re.findall("<a class=\"\" href=\"/search/.*?>(.*?)</a>",book_page_content)[0]
    except:
        book_info['author'] = None
    try:
        book_info['press'] = re.findall("<span class=\"pl\">出版社:</span> (.*?)<br/>",book_page_content)[0]
    except:
        book_info['press'] = None
    try:
        book_info['translator'] = re.findall("<a class=\"\" href=\"/search/.*?>(.*?)</a>",book_page_content)[1]
    except:
        book_info['translator'] = None
    try:
        book_info['ISBN'] = re.findall("<span class=\"pl\">ISBN:</span>(.*?)<br/>",book_page_content)[0]
    except:
        book_info['ISBN'] = None
    try:
        book_info['publicationDate'] = re.findall("<span class=\"pl\">出版年:</span> (.*?)<br/>",book_page_content)[0]
    except:
        book_info['publicationDate'] = None
    try:
        book_info['pages'] = re.findall("<span class=\"pl\">页数:</span> (.*?)<br/>",book_page_content)[0]
    except:
        book_info['pages'] = None
    try:
        book_info['price'] = re.findall("<span class=\"pl\">定价:</span> (.*?)<br/>",book_page_content)[0]
    except:
        book_info['price'] = None
    introduction = re.findall('''<div class="intro">
    <p>(.*?)</p></div>''',book_page_content)
    if(introduction.__len__() == 2):
        if "内容简介" in book_page_content:
            if "作者简介" in book_page_content:
                book_info['briefIntroduction'] = introduction[0]
                book_info['authorIntroduction'] = introduction[1]
                book_info['authorIntroduction'] = book_info['authorIntroduction'].replace("</p>    <p>", "\n")
                book_info['briefIntroduction'] = book_info['briefIntroduction'].replace("</p>    <p>", "\n")
                book_info['authorIntroduction'] = book_info['authorIntroduction'].replace(" ", "")
                book_info['briefIntroduction'] = book_info['briefIntroduction'].replace(" ", "")
            else:
                book_info['briefIntroduction'] = introduction[1]
                book_info['authorIntroduction'] = None
                book_info['briefIntroduction'] = book_info['briefIntroduction'].replace("</p>    <p>", "\n")
                book_info['briefIntroduction'] = book_info['briefIntroduction'].replace(" ", "")
        else:
            book_info['authorIntroduction'] = introduction[1]
            book_info['briefIntroduction'] = None
            book_info['authorIntroduction'] = book_info['authorIntroduction'].replace("</p>    <p>", "\n")
            book_info['authorIntroduction'] = book_info['authorIntroduction'].replace(" ", "")

    elif(introduction.__len__() == 3):
        if '展开全部' in introduction[0] :
            book_info['briefIntroduction'] = introduction[1]
            book_info['authorIntroduction'] = introduction[2]
            book_info['authorIntroduction'] = book_info['authorIntroduction'].replace("</p>    <p>", "\n")
            book_info['briefIntroduction'] = book_info['briefIntroduction'].replace("</p>    <p>", "\n")
            book_info['authorIntroduction'] = book_info['authorIntroduction'].replace(" ", "")
            book_info['briefIntroduction'] = book_info['briefIntroduction'].replace(" ", "")
        else:
            book_info['briefIntroduction'] = introduction[0]
            book_info['authorIntroduction'] = introduction[2]
            book_info['authorIntroduction'] = book_info['authorIntroduction'].replace("</p>    <p>", "\n")
            book_info['briefIntroduction'] = book_info['briefIntroduction'].replace("</p>    <p>", "\n")
            book_info['authorIntroduction'] = book_info['authorIntroduction'].replace(" ", "")
            book_info['briefIntroduction'] = book_info['briefIntroduction'].replace(" ", "")
    elif(introduction.__len__() == 4):
        book_info['briefIntroduction'] = introduction[1]
        book_info['authorIntroduction'] = introduction[3]
        book_info['authorIntroduction'] = book_info['authorIntroduction'].replace("</p>    <p>", "\n")
        book_info['briefIntroduction'] = book_info['briefIntroduction'].replace("</p>    <p>", "\n")
        book_info['authorIntroduction'] = book_info['authorIntroduction'].replace(" ", "")
        book_info['briefIntroduction'] = book_info['briefIntroduction'].replace(" ", "")
    elif(introduction.__len__() == 0):
        book_info['briefIntroduction'] = None
        book_info['authorIntroduction'] = None
    elif(introduction.__len__() == 1):
        if "内容简介" in  book_page_content:
            book_info['briefIntroduction'] = introduction[0]
            book_info['briefIntroduction'] = book_info['briefIntroduction'].replace("</p>    <p>", "\n")
            book_info['briefIntroduction'] = book_info['briefIntroduction'].replace(" ", "")
            book_info['authorIntroduction'] = None
        elif "作者简介" in book_page_content:
            book_info['briefIntroduction'] = None
            book_info['authorIntroduction'] = introduction[0]
            book_info['authorIntroduction'] = book_info['authorIntroduction'].replace("</p>    <p>", "\n")
            book_info['authorIntroduction'] = book_info['authorIntroduction'].replace(" ", "")
    return book_info

def save_book_file(book_info,file_name):
    file_name = str(file_name)
    file_address = "文学/"+file_name+".txt"
    file_address = file_address.decode('utf-8')
    f = open(file_address,"w")
    f.write(str("title:"+book_info['title']+'\n'))
    f.write(str("author:"+book_info['author']+'\n'))
    f.write(str("press:"+book_info['press']+'\n'))
    try:
        f.write(str("translator:"+book_info['translator']+'\n'))
    except:
        f.write("translator:NULL"+'\n')
    f.write(str("ISBN:"+book_info['ISBN']+'\n'))
    f.write(str("publicationDate:"+book_info['publicationDate']+'\n'))
    f.write(str("pages:"+book_info['pages']+'\n'))
    f.write(str("price:"+book_info['price']+'\n'))
    f.write(str("briefIntroduction:"+book_info['briefIntroduction']+'\n'))
    f.write(str("authorIntroduction:"+book_info['authorIntroduction']))
    f.close()
    return True

def save_book_info_json(book_info,file_name):
    book_info = json.dumps(book_info,sort_keys=True,ensure_ascii=False,indent = 2)
    file_name = str(file_name)
    file_address = "科普/" + file_name + ".json"
    file_address = file_address.decode('utf-8')
    f = open(file_address, "w")
    f.write(book_info,ignore)
    f.close()
    return True

def save_book_cover(book_page_content,cover_name):
    cover_url = re.findall('''<a class="nbg"
      href="(.*?)" title=".*?">''',book_page_content)[0]
    cover_name = str(cover_name)
    cover_address = "科普/"+cover_name+".jpg"
    cover_address = cover_address.decode('utf-8')
    f = open(cover_address,"wb")
    cover = requests.get(cover_url).content
    f.write(cover)
    f.close()
    return True


if __name__ == "__main__":
    # book_page_content = get_page_content('http://book.douban.com/tag/%E6%96%87%E5%AD%A6?start=0&type=T')
    # book_page = get_book_page(book_page_content)
    # j = 1
    # for url in book_page:
    #     print str(j)+":正在下载信息："+url
    #     book_info_content = get_page_content(url)
    #     book_info = get_book_info(book_info_content)
    #     save_book_info_json(book_info,j)
    #     print str(j)+":正在下载图片："+url
    #     save_book_cover(book_info_content,j)
    #     j = j + 1
    # book_info_content = get_page_content('https://book.douban.com/subject/4820710/')
    # print get_book_info(book_info_content)
    home_page = 'https://book.douban.com/tag/%E7%A7%91%E6%99%AE?start='
    page = 0
    for page in range(30,50):
        book_home_page = home_page+str(page*20)+'&type=T'
        book_page_content = get_page_content(book_home_page)
        book_page = get_book_page(book_page_content)
        j = 1
        for url in book_page:
            print (str(page*20+j)+":正在下载信息："+url)
            book_info_content = get_page_content(url)
            book_info = get_book_info(book_info_content)
            save_book_info_json(book_info, page*20+j)
            print (str(page*20+j) + ":正在下载图片：" + url)
            save_book_cover(book_info_content, page*20+j)
            j = j + 1