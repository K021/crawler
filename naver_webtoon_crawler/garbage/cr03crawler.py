
import requests
import re

from collections import namedtuple
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from utils import Episode



# <유미의 세포들>
# webtoon_url = 'http://comic.naver.com/webtoon/list.nhn?titleId=651673&weekday=sat'
# titleId = 651673
# weekday = 'sat'


def save_episode_list_to_file(episode_list):
    no_last = episode_list[0].no
    no_first = episode_list[-1].no
    titleId = episode_list[0].titleId
    filename = f'{titleId}_{no_last}_{no_first}.txt'
    with open(filename,'wt') as f:
        for episode in episode_list:
            f.write('|'.join(episode)+'\n')

def load_episode_list_from_file(path):
    Episode = namedtuple('Episode', ['no','titleId', 'img_url', 'title', 'rating', 'created_date'])
    with open(path, 'rt') as file:
        episode_list = [Episode._make(line.split('|')) for line in file]
    return episode_list


def get_webtoon_episode_list(titleId,weekday,page=1):
    payload = {'titleId':titleId , 'weekday':weekday, 'page':page }
    response = requests.get('http://comic.naver.com/webtoon/list.nhn', params=payload)
    source = response.text
    soup = BeautifulSoup(source, 'lxml')

    # 필요한 데이터들 (img_url, title, rating, created_date)추출
    episode_list = list()
    webtoon_table = soup.select_one('table.viewList')   # class = 'viewList'인 '첫번째' <table> 태그 안의 html 반환
    tr_list = webtoon_table.find_all('tr', recursive=False) # 그 안에서 모든 <tr> 태그의 html 반환. recursive=False 설정은 자식 태그만 반환

    for i, tr in enumerate(tr_list):
        td_list = tr.find_all('td')
        if len(td_list) < 4:        # 배너광고 차단
            continue
        td_thumbnail = td_list[0]   # td_thumbnail에 해당하는 Tag의 첫 번째 a tag의 첫 번째 img태그의 'src'속성값
        img_url = td_thumbnail.a.img.get('src')
        title_url = td_thumbnail.a.get('href')
        parsed_url = urlparse(title_url)    # url 쪼개기 (6개 항목의 namedtuple 반환. 그러나 그 외의 다른 속성도 참조할 수 있음. 예를 들어 port, geturl(url전체 반환))
        queryset = parse_qs(parsed_url.query)   # query 쪼개기 (string:[string]구조의 딕셔너리로 반환)
        no = queryset['no']
        titleId = queryset['titleId']

        td_title = td_list[1]
        title = td_title.get_text(strip=True)               # td_title tag의 내용을 좌우여백 잘라냄

        td_rating = td_list[2]
        rating = td_rating.strong.get_text(strip=True)      # td_rating내의 strong태그내의 내용을 좌우여백 잘라냄

        td_created_date = td_list[3]
        created_date = td_created_date.get_text(strip=True) # td_title과 같음

        episode = Episode(     # Episode형 namedtuple객체 생성, episode_list에 추가
            no=no[0],
            titleId=titleId[0],
            img_url=img_url,
            title=title,
            rating=rating,
            created_date=created_date
        )
        episode_list.append(episode)

    # for episode in episode_list:
    #     print('\n', episode)
    return episode_list

episode_list = get_webtoon_episode_list(651673,'sat',1)
save_episode_list_to_file(episode_list)
eplist = load_episode_list_from_file("./651673_251_242.txt")
for ep in eplist:
    print(ep)

# for i in range(86,89):
#     br_bool = False
#     episode_list = get_webtoon_episode_list(651673,'sat',i)
#     print('=============================================')
#     print(f'                   {i}번                    ')
#     print('=============================================')
#     for k in range(len(episode_list)):
#         m = re.match('^1화',episode_list[k][3])
#         if m:
#             br_bool = True
#             break
#     if br_bool:
#         break
