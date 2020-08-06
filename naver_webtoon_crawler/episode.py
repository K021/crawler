import os
import requests
import re

from bs4 import BeautifulSoup
from urllib.parse import urlencode


class Episode:
    def __init__(self, webtoon=None, no='', title_id='', thumbnail_url='', title='', rating='', created_date=''):
        self._webtoon = webtoon
        self._no = no
        self._title_id = title_id
        self._thumbnail_url = thumbnail_url
        self._title = title
        self._rating = rating
        self._created_date = created_date

        self.webtoon_dir = f'webtoon/{self.title_id}'
        self.thumb_dir = f'webtoon/{self.title_id}/{self.title_id}_thumbnail'
        self.contents_dir = f'webtoon/{self.title_id}/{self.title_id}_images/{self.no}'
        self.html_path = f'webtoon/{self.title_id}/{self.title_id}.html'
        self.num_of_imgtags = 0

    def __str__(self):
        string = [
            f'.webtoon = {self.webtoon}',
            f'.no = {self.no}',
            f'.title_id = {self.title_id}',
            f'.thumbnail_url = {self.thumbnail_url}',
            f'.title = {self.title}',
            f'.rating = {self.rating}',
            f'.created_date = {self.created_date}',
            f'.thumb_dir = {self.thumb_dir}',
            f'.contents_dir = {self.contents_dir}'
        ]
        return '\n'.join(string)

    @property
    def webtoon(self):
        return self._webtoon

    @webtoon.setter
    def webtoon(self, input):
        self._webtoon = input

    @property
    def no(self):
        return self._no

    @property
    def title_id(self):
        return self._title_id

    @property
    def thumbnail_url(self):
        return self._thumbnail_url

    @property
    def title(self):
        return self._title

    @property
    def rating(self):
        return self._rating

    @property
    def created_date(self):
        return self._created_date

    @property
    def has_thumbnail(self):
        return os.path.exists(self.thumb_dir + f'/{self.no}.jpg')

    def save_all(self):
        self.save_thumbnail_images()
        self.save_contents_images()
        self.save_as_html()

    def save_thumbnail_images(self, force_update=False):
        # thumbnail이 없거나 강제 업데이트를 할 경우만 실행
        if not self.has_thumbnail or force_update:
            # 강제 업데이트의 경우, 원래 thumbnail을 path_alt에 보존.
            i = 1
            path = f'{self.thumb_dir}/{self.no}.jpg'
            path_alt = f'{self.thumb_dir}/{self.no}' + '_{}.jpg'

            # 디렉토리 만들고
            os.makedirs(self.thumb_dir, exist_ok=True)
            # 이미지 요청
            response = requests.get(self.thumbnail_url)

            # 기존 thumbnail이 존재하지 않을 경우 바로 이미지 저장
            if not os.path.exists(path):
                with open(path, 'wb') as f:
                    f.write(response.content)
            # 존재한다면
            else:
                # path_alt 마저 존재한다면 몇 번까지 존재하는지 검사. 3번까지 존재할 경우 i = 4로 종료
                while os.path.exists(path_alt.format(i)):
                    i += 1
                # i = 4에 원래 thumbnail 저장 (파일 이름 변경)
                os.rename(path, path_alt.format(i))
                # 공식 thumbnail path에 새로운 썸네일 저장
                with open(path, 'wb') as f:
                    f.write(response.content)

    def save_contents_images(self):
        # 해당 episode의 링크 문자열
        episode_link_body = 'http://comic.naver.com/webtoon/detail.nhn?'
        params = {"titleId": self._title_id, "no": self.no}
        episode_link = episode_link_body + urlencode(params)

        # 묻지도 따지지도 않고 이미지 디렉토리 생성
        os.makedirs(self.contents_dir, exist_ok=True)

        # 링크 접속
        response = requests.get(episode_link)
        soup = BeautifulSoup(response.text, 'lxml')

        # html 비트수프 파헤치기: 만화 이미지 태그만 골라냄 (img_tags 리스트)
        contents_link_list = list()
        img_div = soup.select_one('div.wt_viewer')
        img_tags = img_div.find_all('img', recursive=False)
        self.num_of_imgtags = len(img_tags)
        # 만화 이미지 태그에서 이미지 소스 뽑아냄 (contents_link_list 리스트)
        for img_tag in img_tags:
            contents_link_list.append(img_tag.get('src'))
        # 그 이미지 소스에 이미지 요청
        for index, url in enumerate(contents_link_list):
            headers = {'Referer': episode_link}
            response = requests.get(url, headers=headers)
            with open(f'{self.contents_dir}/{index + 1}.jpg', 'wb') as f:
                f.write(response.content)

    # 저장된 이미지 파일을 html의 형식으로 편집해 저장
    def save_as_html(self):
        # 이미지 소스의 기본 틀
        imgtag = f'<img src="./{self.title_id}_images/{self.no}/' + '{}.jpg">'
        # 이미지 갯수 만큼 이미지 태그를 담고 있는 문자열 생성
        body_string = imgtag.format('1')
        for img_num in range(2, self.num_of_imgtags + 1):
            body_string = body_string + '\n    ' + imgtag.format(img_num)
        # html 문서 제목
        document_title = self.webtoon.name + ': ' + self.title
        # html 파일을 저장할 디렉토리 생성
        os.makedirs(self.webtoon_dir, exist_ok=True)
        with open(self.html_path, 'wt') as f:
            with open('html_body.html', 'rt') as html:
                html_body = html.read()
                html_body_with_title = re.sub('752TITLE752', document_title, html_body)
                f.write(re.sub('752CONTENTS752', body_string, html_body_with_title))


if __name__ == '__main__':
    ep = Episode()
