#!/usr/bin/python3
import requests
import re
import os
import time

DATADIR='/tmp/book'

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1"
}
class Book:

    def get_cookie(self):
        cookies = {}
        cookie = '''用浏览器登陆后把cookies 整行填到这里'''
        for line in cookie.split(";"):
            k,v = line.split("=")
            cookies[k] = v
        self.cookies = cookies
        return cookies
    def __init__(self):
        self.get_cookie()
    
    def getBookList(self):
        bookListUrl = 'http://www.ituring.com.cn/user/shelf'
        r = requests.get(bookListUrl,headers= headers,cookies=self.cookies)
        regx = '<h4 class="name"><a href="/book/(\d+)" title'
        bookIdList = re.findall(regx,r.text)
        return bookIdList
    
    def getBookName(self,bookId):
        url = 'http://www.ituring.com.cn/book/{0}'.format(bookId)
        r = requests.get(url,headers=headers)
        regx = u'<title>(.*)</title>'
        bookName = re.findall(regx,r.text)[0].replace('-图书-图灵社区','')
        print(bookName)
        return bookName

    def getBookPdfId(self,bookId):
        bookPage = 'http://www.ituring.com.cn/book/'+str(bookId)
        r = requests.get(bookPage,headers= headers,cookies=self.cookies)
        regx = '<a href="/file/ebook/(\d+)\?type=PDF">'
        pdfId = re.findall(regx,r.text)
        return pdfId[0]
    
    def downloadBook(self,bookId):
        bookName = self.getBookName(bookId)
        bookName = bookName.split(":")[0]
        filePath = os.path.join(DATADIR,bookName+".pdf")
        if os.path.exists(filePath):
            print(filePath)
            print("文件已存在，跳过")
            return
        pdfId = self.getBookPdfId(bookId)
        url = 'http://www.ituring.com.cn/file/ebook/{0}?type=PDF'.format(pdfId)
        f = open(filePath,'wb+')
        try:
            print("正在下载")
            r = requests.get(url,headers= headers,cookies=self.cookies)
            for chunk in r.iter_content(1024):
                f.write(chunk)
            f.close()
        except Exception as ex:
            print("下载失败,sleep 5秒下一个")
            time.sleep(5)
            os.remove(filePath) 
            

    def downloadAll(self):
        bookList = self.getBookList()
        for bookId in bookList:
            self.downloadBook(bookId)
    
    
b = Book()
b.downloadAll()
