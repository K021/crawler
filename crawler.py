import requests, os, pickle
from utils import Webtoon, get_webtoon_episode_list, get_webtoon_list
from utils import html_head, html_body, html_bottom

class NaverWebToonCrawlar():
    def __init__(self, webtoon_name=None):
        self.webtoon = self._webtoon_id_init(webtoon_name)
        self.episode_list = list()
        self.load(init=True)
        print(self.webtoon)

    def _webtoon_id_init(self,webtoon_name=None):
        if not webtoon_name:
            webtoon_name = input('Type any name of webtoon: ')
        webtoon = self.find_webtoon(webtoon_name)
        while len(webtoon) != 1:
            if not webtoon:
                print(f"There's no webtoon named '{webtoon_name}'. Try again: ")
                webtoon_name = input('Type any name of webtoon: ')
                webtoon = self.find_webtoon(webtoon_name)
            print('==================================')
            for wt in webtoon:
                print(wt.name)
            webtoon_name = input('You can choose one of these: ')
            webtoon = self.find_webtoon(webtoon_name)
        webtoon = webtoon[0]
        return webtoon

    @property
    def total_episode_count(self):
        el = get_webtoon_episode_list(self.webtoon.title_id)
        return int(el[0].no)

    @property
    def up_to_date(self):
        return len(self.episode_list) == self.total_episode_count
        # cur_episode_count = len(self.episode_list)
        # cur_episode_count = int(self.episode_list[0].no if self.episode_list != [] else 0)
        # total_episode_count = self.total_episode_count
        # return cur_episode_count == total_episode_count

    def update_episode_list(self, force_update=False):
        if force_update:
            self.episode_list = list()
        new_episode_list = []
        recent_episode_no = int(self.episode_list[0].no if self.episode_list != [] else 0)
        delta_no = (self.total_episode_count - recent_episode_no)//10 +1
        for i in range(1,delta_no+1):
            new_episode_list.extend(get_webtoon_episode_list(self.webtoon.title_id,i,recent_episode_no+1))
        self.episode_list = new_episode_list + self.episode_list
        for i in self.episode_list:
            print(i)
        self.save()
        return len(new_episode_list)

    @staticmethod
    def find_webtoon(user_input):
        webtoon_list = get_webtoon_list()
        user_webtoon = [ webtoon for webtoon in webtoon_list if user_input in webtoon.name ]
        return user_webtoon

    def find_webtoon_search(user_input):
        pass

    def save(self, path=None):
        if not os.path.isdir('./episode_list'):
            os.mkdir('./episode_list')
        path = './episode_list/{}.txt'.format(self.webtoon.title_id)
        pickle.dump(self.episode_list,open(path,'wb'))  # 참조되는 곳이 없는 파일 객체는 닫힌다.

    def load(self, path=None, init=False):
        try:
            path = './episode_list/{}.txt'.format(self.webtoon.title_id)
            self.episode_list = pickle.load(open(path,'rb'))
        except FileNotFoundError:
            if not init:
                print('There no file on the path:{}'.format(path))
        return self.episode_list

    def save_list_thumbnail(self):
        os.makedirs(f'./webtoon/{self.webtoon.title_id}_thumbnail', exist_ok=True)
        for ep in self.episode_list:
            response = requests.get(ep.img_url)
            path = f'./webtoon/{self.webtoon.title_id}/{self.webtoon.title_id}_thumbnail/{ep.no}.jpg'
            if not os.path.exists(path):
                with open(path,'wb') as f:
                    f.write(response.content)

    def make_html(self):
        if not os.path.isdir('./webtoon'):
            os.mkdir('./webtoon')
        path = './webtoon/%s.html'% self.webtoon.title_id
        with open(path,'wt') as f:
            f.write(html_head)
            for ep in self.episode_list:
                img_path = f'./{self.webtoon.title_id}_thumbnail/{ep.no}.jpg'
                f.write(html_body.format(img_path,ep.title,ep.rating,ep.created_date))
            f.write(html_bottom)
        return path

    def get_episode_detail(self, episode):
        pass



# html_body = html_body.format(
#     img_url=item.img_url,
#     title=item.title,
#     rating=item.rating,
#     created_date=item.created_date
#     )

# 선천적 얼간이들 http://comic.naver.com/webtoon/list.nhn?title_id=697680&weekday=mon

nwc = NaverWebToonCrawlar()


# l = nwc.episode_list
# for i in nwc.episode_list:
#     print(i)

# payload = {'title_id':self.webtoon.title_id}
# response = requests.get('http://comic.naver.com/webtoon/list.nhn', params=payload)
# soup = BeautifulSoup(response.text, 'html.parser')
# webtoon_table = soup.select_one('table.viewList')
# tr_list = webtoon_table.find_all('tr', recursive=False)
