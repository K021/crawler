
import os, requests
from urllib.parse import urlencode

class Episode:
    def __init__(self,webtoon=None,no='',title_id='',thumbnail_url='',title='',rating='',created_date=''):
        self._webtoon = webtoon
        self._no = no
        self._title_id = title_id
        self._thumbnail_url = thumbnail_url
        self._title = title
        self._rating = rating
        self._created_date = created_date

        self.thumb_path = f'webtoon/{self.title_id}/{self.title_id}_thumbnail'
        self.contents_dir = f'webtoon/{self.title_id}/{self.title_id}_images/{self.no}'

    @property
    def webtoon(self):
        return self._webtoon

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
        return os.path.exists(thumb_dir + f'/{self.no}.jpg')

    def save_all(self):
        self.save_thumbnail()
        self.save_images()

    def save_thumbnail(self,force_update=False):
        if not self.has_thumbnail or force_update==True:
            i = 1
            path = f'{self.thumb_dir}/{self.no}.jpg'
            path_alt = f'{self.thumb_dir}/{self.no}_{i}.jpg'
            os.makedirs(self.thumb_dir,exist_ok=True)
            response = requests.get(self.thumbnail_url)
            if not os.path.exists(path):
                with open(path,'wb') as f:
                    f.write(response.content)
            else:
                path_before = path
                while os.path.exist(path_alt):
                    path_before = path_alt
                    i += 1
                os.rename(path_before,path_alt)
                with open(path,'wb') as f:
                    f.write(response.content)

    def save_images(self):
        episode_link_body = 'http://comic.naver.com/webtoon/detail.nhn?'
        params = {
            "titleId":self._title_id,
            "no":self.no
        }
        episode_link = episode_link_body + urlencode(params)

        response = requests.get(episode_link)
        soup = BeautifulSoup(response.text, 'lxml')

        contents_link_list = list()
        img_div = soup.select_one('div.wt_viewer')
        img_tags = img_div.find_all('img', recursive=False)
        for img_tag in img_tags:
            contents_link_list.append(img_tag.get('src'))

        for index, url in enumerate(contents_link_list):
            headers = {'Referer': episode_link}
            response = requests.get(url, headers=headers)
            with open(f'{self.contents_dir}/{index + 1}.jpg', 'wb') as f:
                f.write(response.content)

if __name__ == '__main__':
    pass
