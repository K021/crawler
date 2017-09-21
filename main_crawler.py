import requests, re, os, pickle
from collections import namedtuple
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from utils import Episode, get_webtoon_episode_list


class NaverWebToonCrawlar():
    def __init__(self,webtoon_id):
        self.webtoon_id = webtoon_id
        self.episode_list = list()
        self.load(init=True)

    @property
    def total_episode_count(self):
        el = get_webtoon_episode_list(self.webtoon_id)
        return int(el[0].no)

    @property
    def up_to_date(self):
                return len(self.episode_list) == self.total_episode_count

        # cur_episode_count = len(self.episode_list)
        # cur_episode_count = int(self.episode_list[0].no if self.episode_list != [] else 0)
        # total_episode_count = self.total_episode_count
        # return cur_episode_count == total_episode_count

    def update_episode_list(self, force_update=False):
        new_episode_list = []
        recent_episode_no = int(self.episode_list[0].no if self.episode_list != [] else 0)
        delta_no = (self.total_episode_count - recent_episode_no)//10 +1
        for i in range(1,delta_no+1):
            new_episode_list.extend(get_webtoon_episode_list(self.webtoon_id,i,recent_episode_no+1))
        self.episode_list = new_episode_list + self.episode_list
        for i in self.episode_list:
            print(i)
        return len(new_episode_list)


    def save(self, path=None):
        if not os.path.isdir('./episode_list'):
            os.mkdir('./episode_list')
        path = './episode_list/{}.txt'.format(self.webtoon_id)
        pickle.dump(self.episode_list,open(path,'wb'))  # 참조되는 곳이 없는 파일 객체는 닫힌다.

    def load(self, path=None, init=False):
        try:
            path = './episode_list/{}.txt'.format(self.webtoon_id)
            self.episode_list = pickle.load(open(path,'rb'))
        except FileNotFoundError:
            if not init:
                print('There no file on the path:{}'.format(path))
        return self.episode_list


# 선천적 얼간이들 http://comic.naver.com/webtoon/list.nhn?titleId=697680&weekday=mon

nwc = NaverWebToonCrawlar(697680)
for i in nwc.load():
    print(i)



# payload = {'titleId':self.webtoon_id}
# response = requests.get('http://comic.naver.com/webtoon/list.nhn', params=payload)
# soup = BeautifulSoup(response.text, 'html.parser')
# webtoon_table = soup.select_one('table.viewList')
# tr_list = webtoon_table.find_all('tr', recursive=False)
