import re
import requests
from bs4 import BeautifulSoup

url = requests.get('http://comic.naver.com/webtoon/list.nhn?titleId=651673&weekday=sat')
data = url.text
bs = BeautifulSoup(data,'html.parser')
title_list = bs.find_all('td', class_='title')
print(data)
# f = open('./webtoon.txt','r')

# pattern = re.compile(r'''<td class=['"]title['"].*?>.*?<a.*?>(.*?)</a>.*?</td>''',re.DOTALL)

# m = re.findall(pattern,data)

# for i in reversed(m):
    # print(i)

# for i in title_list:
#    print(i.a.text)
