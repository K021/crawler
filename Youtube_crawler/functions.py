from pprint import pprint

import pafy
from time import time
from pytube import YouTube
from bs4 import BeautifulSoup
import requests


def get_vid_link(url, playlist=True):
    # with open('./jfla.html', 'rt') as f:
    #     html = f.read()
    # soup = BeautifulSoup(html, 'lxml')

    class_playlist = 'pl-video-title-link'
    class_videolist = 'yt-simple-endpoint style-scope ytd-grid-video-renderer'

    class_type = class_playlist if playlist else class_videolist
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'lxml')
    a_tags = soup.find_all('a', class_=class_type)

    a_list = list()
    for a in a_tags:
        url = a.get('href')
        a_list.append('https://www.youtube.com' + url[:url.index('&')])

    return a_list


# links = get_vid_link()
#
# for i, link in enumerate(links):
#     print('{:<3d} : {}'.format(i+1, link))


def download_video(*urls, download_path):
    for url in urls:
        youtube = YouTube(url)
        youtube.streams.first().download(download_path)


def vid_data(link):
    youtube = YouTube(link)
    print(youtube.title)
    pprint(youtube.streams.all())


def download_video_pafy(*urls, download_path=''):
    n = len(urls)
    print(f'Start to download {n} videos')
    for i, url in enumerate(urls):
        vid = pafy.new(url)
        stream = vid.getbest()
        print(f'Title: {vid.title},  Res.: {stream.quality}, Size: {stream.get_filesize()/1000000:.2f}MB')
        stream.download(download_path)
        print()
        print(f'process #{i+1} completed. ({i+1}/{n})')
        print()


if __name__ == '__main__':
    start = time()

    # urls = [
    #     'https://www.youtube.com/watch?v=Qm0jWj35L4U',  # 빌버 안 처맞는 아이들 1/2
    #     'https://www.youtube.com/watch?v=ogYPOH6USZM',  # 빌버 안 처맞는 아이들 2/2
    #     'https://www.youtube.com/watch?v=8xY12Jno_qA',  # 빌버 싸이코 로봇 같은 여자들
    #     'https://www.youtube.com/watch?v=mipejBRi8T4',  # 조던 피터슨, 앉아서 공부하거나 일하는게 힘든 이유
    #     'https://www.youtube.com/watch?v=9nXlSr_2pE4',  # 벤 샤피로, 팩트는 너의 기분 따윈 상관하지 않는다
    #     'https://www.youtube.com/watch?v=NO8Fz6gGOus',  # Nir Eyal, HOW TO BREAK THE BAD HABITS
    #     'https://www.youtube.com/watch?v=gPgTvUooENY',  # 드웨인 존슨, 차 선물하는 취미
    #     'https://www.youtube.com/watch?v=sxBfKYH96Vo',  # 빌 버, 타이타닉의 페미니스트들
    # ]

    urls = [
        'https://www.youtube.com/watch?v=rgky6-CqbpQ',
        'https://www.youtube.com/watch?v=U-kxdyJs6y8',
    ]

    download_video_pafy(*urls)

    end = time() - start
    if end > 60:
        end = f'{end/60:.2f} 분'
    print(end)
