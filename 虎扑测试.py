import re
import requests
import os
import time
from bs4 import BeautifulSoup

#帖子链接列表
html_list = []

#图片列表
wallpaper_list = []

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"}

#读取器网页内容
def Get_content(url):
    try:
        response = requests.get(url,headers = headers)
        response.encoding = response.apparent_encoding
        if (response.status_code ==200 ):
            return response.text
        else:
            print("获取网页失败")
            print("错误代码："+str(response.status_code))
    except:
        print("获取网页内容异常")

def Get_binary(url):
    try:
        response = requests.get(url,headers = headers)
        response.encoding = response.apparent_encoding
        if (response.status_code ==200 ):
            return response.content
        else:
            print("获取网页失败")
            print("错误代码："+str(response.status_code))
            return 0
    except:
        print("获取图片网页内容异常")

#获取网页链接
#获取的帖子链接形式  /21494000.html
def Get_url(content):
    try:
        url_bsobj = BeautifulSoup(content,'html.parser')
        for url in url_bsobj.find_all('a',{"class":"truetit"}):
            htmlurl = url.get('href')
            #获取的href为  /21494000.html  形式
            if htmlurl not in html_list: #去重
                html_list.append(htmlurl)#将帖子url放进列表
    except:
        print("解析网页标签异常")

#获取帖子最大页码数
#带上页码的连接形式  https://bbs.hupu.com/19630769-2.html
def Get_page(content):
    #直接匹配href里的信息
    try:
        page_bsobj = BeautifulSoup(content,'html.parser')
        max_page = page_bsobj.find('div',{"id":"bbstopic_set"}).get("data-maxpage")
        return max_page
    except:
        print("获取帖子最大页码数异常")

#获取图片链接
def Get_Image(content):
    pattern = re.compile(r'data-original="(.*?)"')
    #未处理的wallpaper链接
    #未处理的wallpaper链接形式
    #https://i1.hoopchina.com.cn/hupuapp/bbs/385/218545349185385/thread_218545349185385_20180211091047_s_52711_h_256px_w_384px1813139458.jpeg?x-oss-process=image/resize,w_800/format,webp
    complete_list = re.findall(pattern,content)
    for url in complete_list:
        #处理wallpaper连接形式
        temp = url.split('?')
        url = temp[0]
        if url not in wallpaper_list:
            wallpaper_list.append(url)

'''
#获取title从而创建文件夹
def Get_title(content):
    try:
        title_bsobj = BeautifulSoup(content,'html.parser')
        title_tag = title_bsobj.find('title')
        pattern = re.compile(r'\n([\u4e00-\u9fa5].*?) ')
        title = re.findall(pattern,title_tag.text)[0]
        #创建文件夹
        path = 'F:\\temp\\'+title
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
        return title
    except:
        print("获取title标签异常")
'''

#写入文件
def Write(titlename,postfix,words):
    f = open('F:\\temp\\'+titlename+'.'+postfix,'wb')
    f.write(words)
    f.close()

#爬取的起始页
start_url = "https://bbs.hupu.com/wallpaper-"
#循环爬取的链接形式  https://bbs.hupu.com/wallpaper-X

for i in range(1,2):
    #填充帖子链接列表   html_list
    request_url = start_url+str(i)
    print(request_url)
    text = Get_content(request_url)
    Get_url(text)

print('填充html_list完毕')
#html_list里面的格式为/21494000.html
#要求的链接格式为https://bbs.hupu.com+/XXXXX.html
#处理帖子链接格式
for html in html_list:
    complete_html = 'https://bbs.hupu.com'+html
    #print(complete_html)
    text = Get_content(complete_html)
    #title = Get_title(text)
    #获取帖子中的页码总数
    max_page = Get_page(text)
    #print(max_page)
    for i in range(1,int(max_page)+1):
        #处理连接格式a
        page_html = complete_html.split('.html')[0]+'-'+str(i)+'.html'
        #print(page_html)
        #填充wallpaper_list
        Get_Image(Get_content(page_html))

i = 1
print("正在下载图片")
#下载图片
for img in wallpaper_list:
    postfix = img.split('.')[-1]
    picture = Get_binary(img)
    if picture != 0:
        Write(str(i),postfix,picture)
        print("下载第"+str(i)+"张图片成功！")
        i = i+1
    else:
        print("下载第"+str(i)+"张图片未成功！")
