
# -------------------------------------------------------------------------------------

# import subprocess
#
# path = './webtoon/697680/697680.html'
# subprocess.call(['open',path])

# -------------------------------------------------------------------------------------

# i = 1
# test = '---'
# path = f'{test}/asdf_'+'{}.jpg'
#
# for i in range(10):
#     print(path.format(i))

# -------------------------------------------------------------------------------------

# import requests, re, os, pickle
# from collections import namedtuple
# from bs4 import BeautifulSoup
# from urllib.parse import urlparse, parse_qs
# from utils import Episode, Webtoon, get_webtoon_episode_list
# from utils import html_head, html_body, html_bottom
#
# def find_webtoon(user_input):
#     webtoon_list = get_webtoon_list()
#     user_webtoon = [ webtoon for webtoon in webtoon_list if user_input in webtoon.name ]
#     return user_webtoon


# def get_webtoon_list():
#     """
#     네이버 웹툰의 모든 정보를 가져온다.
#     """
#     response = requests.get('http://comic.naver.com/webtoon/weekday.nhn')
#     soup = BeautifulSoup(response.text,'lxml')
#     entire_webtoonlist = soup.select_one('div.daily_all')
#     ul_list = entire_webtoonlist.find_all('ul')
#
#     webtoon_list = set()
#
#     for ul in ul_list:
#         li_list = ul.find_all('li')
#         for li in li_list:
#             li_a = li.find_all('a',recursive=False)
#             name = li_a[0].get_text(strip=True)     # 양쪽에 공백 있으면 잘라내는 것
#
#             webtoon_url = li_a[0].get('href')
#             parsed_url = urlparse(webtoon_url)    # url 쪼개기 (6개 항목의 namedtuple 반환. 그러나 그 외의 다른 속성도 참조할 수 있음. 예를 들어 port, geturl(url전체 반환))
#             queryset = parse_qs(parsed_url.query)   # query 쪼개기 (string:[string]구조의 딕셔너리로 반환)
#             titleId = queryset['titleId'][0]
#
#             thumbnail_src = li.div.a.img.get('src')
#
#             webtoon = Webtoon(name = name, titleId = titleId, thumbnail_src = thumbnail_src)
#             webtoon_list.add(webtoon)
#
#     webtoon_list = sorted(list(webtoon_list), key=lambda x:x.name)
#     return webtoon_list

#
# user_input = input('Type any name of webtoon: ')
# print(find_webtoon(user_input))
