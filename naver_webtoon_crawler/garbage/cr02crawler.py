import requests
from bs4 import BeautifulSoup

webtoon_url = 'http://comic.naver.com/webtoon/list.nhn?titleId=651673&weekday=sat'

response = requests.get(webtoon_url)
source = response.text
soup = BeautifulSoup(source,'html.parser')
pre_soup = soup.prettify()

img_url = []
for l in soup.table.find_all('img'):
    img_url.append(str(l.get('src')))



# for child in soup.table.children:
#     print(child)

with open('sample.txt','wt') as f:
    f.write(soup.prettify())
