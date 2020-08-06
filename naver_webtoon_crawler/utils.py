
import requests
from bs4 import BeautifulSoup
# from collections import namedtuple
from typing import NamedTuple
from urllib.parse import urlparse, parse_qs
from episode import Episode


# NamedTuple(Episode) 을 사용해서
#   썸네일 이미지 주소(thumbnail_url)
#   에피소드 제목(title)
#   에피소드 별점(rating)
#   에피소드 등록일(created_date)
# 를 가지는 NamedTuple의 리스트를 생성
# Episode = namedtuple('Episode', ['no','title_id', 'thumbnail_url', 'title', 'rating', 'created_date'])
# Webtoon = namedtuple('Webtoon', ['name', 'title_id', 'thumbnail_src'])
class Webtoon(NamedTuple):
    name: str
    title_id: str
    thumbnail_src: str


html_head = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>webtoon</title>
</head>
<body>
  <table>'''
html_body = '''<tr>
  <td><img src='{}'</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
</tr>
'''
html_bottom = '''  </table>
</body>
</html>
'''


def get_total_webtoon_list():
    """
    네이버에 등재된 모든 웹툰 정보 리스트를 가져온다.
    """
    response = requests.get('http://comic.naver.com/webtoon/weekday.nhn')
    soup = BeautifulSoup(response.text, 'lxml')
    entire_webtoonlist = soup.select_one('div.daily_all')
    ul_list = entire_webtoonlist.find_all('ul')

    webtoon_list = set()

    for ul in ul_list:
        li_list = ul.find_all('li')
        for li in li_list:
            li_a = li.find_all('a', recursive=False)
            name = li_a[0].get_text(strip=True)  # 양쪽에 공백 있으면 잘라내는 것

            webtoon_url = li_a[0].get('href')
            # url 쪼개기 (6개 항목의 namedtuple 반환.
            # 그러나 그 외의 다른 속성도 참조할 수 있음. 예를 들어 port, geturl(url전체 반환))
            parsed_url = urlparse(webtoon_url)
            queryset = parse_qs(parsed_url.query)  # query 쪼개기 (string:[string]구조의 딕셔너리로 반환)
            title_id = queryset['titleId'][0]

            thumbnail_src = li.div.a.img.get('src')

            webtoon = Webtoon(
                name=name,
                title_id=title_id,
                thumbnail_src=thumbnail_src
            )
            webtoon_list.add(webtoon)

    webtoon_list = sorted(list(webtoon_list), key=lambda x: x.name)
    return webtoon_list


def get_webtoon_episode_list(title_id, page=1, min_no=1):
    payload = {'titleId': title_id, 'page': page}
    response = requests.get('http://comic.naver.com/webtoon/list.nhn', params=payload)
    source = response.text
    soup = BeautifulSoup(source, 'lxml')
    # 필요한 데이터들 (thumbnail_url, title, rating, created_date)추출
    episode_list = list()
    webtoon_table = soup.select_one('table.viewList')   # class = 'viewList'인 '첫번째' <table> 태그 안의 html 반환
    tr_list = webtoon_table.find_all('tr', recursive=False)  # 그 안에서 모든 <tr> 태그의 html 반환. recursive=False 설정은 자식 태그만 반환

    for i, tr in enumerate(tr_list):
        td_list = tr.find_all('td')
        if len(td_list) < 4:        # 배너광고 차단
            continue
        td_thumbnail = td_list[0]
        thumbnail_url = td_thumbnail.a.img.get('src')  # td_thumbnail에 해당하는 Tag의 첫 번째 a tag의 첫 번째 img태그의 'src'속성값
        title_url = td_thumbnail.a.get('href')  # 웹툰 url
        # url 쪼개기 (6개 항목의 namedtuple 반환.
        # 그러나 그 외의 다른 속성도 참조할 수 있음. 예를 들어 port, geturl(url전체 반환))
        parsed_url = urlparse(title_url)
        queryset = parse_qs(parsed_url.query)   # query 쪼개기 (string:[string]구조의 딕셔너리로 반환)
        no = queryset['no']
        title_id = queryset['titleId']
        if int(no[0]) < min_no:
            break

        td_title = td_list[1]
        title = td_title.get_text(strip=True)               # td_title tag의 내용을 좌우여백 잘라냄

        td_rating = td_list[2]
        rating = td_rating.strong.get_text(strip=True)      # td_rating내의 strong태그내의 내용을 좌우여백 잘라냄

        td_created_date = td_list[3]
        created_date = td_created_date.get_text(strip=True)  # td_title과 같음

        episode = Episode(     # Episode형 namedtuple객체 생성, episode_list에 추가
            no=no[0],
            title_id=title_id[0],
            thumbnail_url=thumbnail_url,
            title=title,
            rating=rating,
            created_date=created_date
        )
        episode_list.append(episode)

    # for episode in episode_list:
    #     print('\n', episode)
    return episode_list
