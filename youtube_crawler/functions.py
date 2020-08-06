import os
from pprint import pprint

import pafy
from time import time
from pytube import YouTube
from bs4 import BeautifulSoup
import requests


DOWNLOAD_DIR = os.path.expanduser('~') + '/Downloads/'


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


def download_video_pafy(*urls, download_dir=DOWNLOAD_DIR):
    n = len(urls)
    print(f'Start to download {n} videos')
    for i, url in enumerate(urls):
        vid = pafy.new(url)
        stream = vid.getbest()
        print(f'Title: {vid.title},  Res.: {stream.quality}, Size: {stream.get_filesize()/1000000:.2f}MB')
        stream.download(filepath=download_dir)
        print()
        print(f'process #{i+1} completed. ({i+1}/{n})')
        print()


def download_audio_pafy(*urls, type='m4a', download_dir=DOWNLOAD_DIR):
    def best_in_type(streams, type):
        streams_with_type = list(filter(lambda x: x.extension == type, streams))
        return max(streams_with_type, key=lambda x: x.bitrate)

    n = len(urls)
    print(f'Start to download {n} audios (m4a)')
    for i, url in enumerate(urls):
        vid = pafy.new(url)
        streams = vid.audiostreams
        stream = best_in_type(streams, type)
        print(f'Title: {vid.title},  Res.: {stream.quality}, Size: {stream.get_filesize()/1000000:.2f}MB')
        print(f'Possible files to download: {streams}')
        print(f'Downloading: {stream}')
        stream.download(filepath=download_dir)
        print()
        print(f'process #{i+1} completed. ({i+1}/{n})')
        print()


if __name__ == '__main__':
    start = time()

    urls = [
        'https://www.youtube.com/watch?v=qx7KPg7qn28',
    ]
    download_video_pafy(*urls)
    # download_audio_pafy(*urls)

    # urls_in_playlists = get_vid_link('https://www.youtube.com/playlist?list=PLR9rKiVA8K5wQh2RWVJY2IQexIwdusG3a')
    # download_audio_pafy(*urls_in_playlists)

    end = time() - start
    if end > 60:
        end = f'{end/60:.2f} 분'
    print(end)
