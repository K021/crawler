import warnings
from typing import NamedTuple

import requests
from bs4 import BeautifulSoup

from variables import *


__all__ = (
    'get_vid_info',
    'download_vid',
)


class VidInfo(NamedTuple):
    key: str
    title: str


def get_page_urls_from_lecture_list(master_url):
    """
    academy.nomadcoder.com 의 강의 리스트 페이지에서 각 강의 영상 페이지 링크 리스트를 가져오는 함수
    :param master_url: 강의 리스트 페이지 url
    :return: 각 강의 영상 페이지의 url 리스트
    """
    pass


def get_vid_info(*urls):
    """
    강의 영상 페이지 url 에서, wistia 에서 강의 영상을 구분하는 고유 key 값과 영상 title 을 담은 VidInfo 리스트 추출
    :param urls: 강의 영상 페이지 url
    :return: VidInfo 객체 리스트
    """
    vid_infos = list()
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        vid_tags = soup.select('div.attachment-wistia-player')
        title_tags = soup.select('meta[property="og:title"]')

        if vid_tags:
            key = vid_tags[0]['data-wistia-id']
            if not title_tags:
                warnings.warn(f'No title for vid "{key}"')
                title = f'no-title-{key}'
            else:
                title = title_tags[0]['content']
            vid_infos.append(VidInfo(key=key, title=title))

    return vid_infos


def download_vid(*vid_infos, download_dir=''):
    """
    VidInfo 객체를 받아서 'title.mp4' 파일 저장
    :param vid_infos: VidInfo 객체
    :param download_dir: 다운로드 하려는 폴더의 하드링크로, 존재하는 디렉토리여야 한다.
    :return: download 한 영상 갯수
    """
    download_count = 0
    for vi in vid_infos:
        media_info_url = MEDIA_INFO_URL_BASE + vi.key + '.json'
        r = requests.get(media_info_url)

        vid_url = r.json()['media']['assets'][0][:-3] + 'mp4'  # 원본 비디오 파일 링크 .bin 확장자이나, .mp4 로 변경 가능
        vid_stream = requests.get(vid_url)

        download_path = download_dir + vi.title + '.mp4'
        with open(download_path, 'wb') as f:
            f.write(vid_stream.content)
            download_count += 1

    return download_count


