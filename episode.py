
from utils import Webtoon,
from urllib.parse import urlencode

class Episode:
    def __init__(self,webtoon=Webtoon(),no='',title_id='',img_url='',title='',rating='',created_date=''):
        self._webtoon = webtoon
        self._no = no
        self._title_id = title_id
        self._img_url = img_url
        self._title = title
        self._rating = rating
        self._created_date = created_date

    @property
    def has_thumbnail(self):
        path = f'./webtoon/{self.webtoon.title_id}/{self.webtoon.title_id}_thumbnail/{self.no}.jpg'
        if os.path.exists(path):
            return True
        else:
            return False

    def _save_images(self):
        episode_link_body = 'http://comic.naver.com/webtoon/detail.nhn?'
        params = {
            "titleId":self._title_id,
            "no":self.no
        }
        episode_link = episode_link_body + urlencode(params)

        response = requests.get(episode_link)
        soup = BeautifulSoup(response.text, 'lxml')
        # 필요한 데이터들 (img_url, title, rating, created_date)추출
        contents_link_list = list()
        img_div = soup.select_one('div.wt_viewer')   # class = 'viewList'인 '첫번째' <table> 태그 안의 html 반환
        img_tags = img_div.find_all('img', recursive=False) # 그 안에서 모든 <tr> 태그의 html 반환. recursive=False 설정은 자식 태그만 반환
        for img_tags in img_tags:
            contents_link_list.append(img_tag.get('src'))

        for url in contents_link_list:
            # img에 대한 각 requests.get에는 url_contents가 Referer인 header가 필요
            headers = {'Referer': episode_link}
            # requests.get요청을 보냄
            response = requests.get(url, headers=headers)
            # 파일을 저장
            with open(f'{self.image_dir}/{index + 1}.jpg', 'wb') as f:
                f.write(response.content)




        headers = {'Referer': episode_link}
        image_data = requests.get(image_file_url, headers=headers).content
