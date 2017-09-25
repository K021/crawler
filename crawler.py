import requests, os, pickle
from utils import Webtoon, get_webtoon_episode_list, get_total_webtoon_list
from utils import html_head, html_body, html_bottom

class NaverWebtoonCrawlar():
    def __init__(self, webtoon_name=None):
        # 한 웹툰을 골라 그 정보를 네임드 튜플로 저장 (이름, id, 썸네일 소스)
        self.webtoon = self._webtoon_id_init(webtoon_name)
        # 저장된 episode_list 있으면 불러옴
        self.episode_list = list()
        self.load(init=True)

    # 문자열로 출력시 웹툰 정보 제공
    def __str__(self):
        return self.webtoon

    # NaverWebtoonCrawlar 클래스 하나가 한 웹툰 정보를 가지도록 초기화하는 내부함수
    def _webtoon_id_init(self,webtoon_name=None):
        # 웹툰 이름을 인자로 주지 않았을 경우, 입력 요구
        if not webtoon_name:
            webtoon_name = input('Type any name of webtoon: ')
        # 입력된 문자열과 일치하는 웹툰을 찾아서 리스트로 저장. 없을 경우 빈 리스트.
        webtoon = self.find_webtoon(webtoon_name)
        # 일치하는 웹툰이 없거나, 둘 이상일 때 무한 반복
        while len(webtoon) != 1:
            # 없으면 재입력
            if not webtoon:
                print(f"There's no webtoon named '{webtoon_name}'. Try again: ")
                webtoon_name = input('Type any name of webtoon: ')
                webtoon = self.find_webtoon(webtoon_name)
            print('==================================')
            # 여러 개면 보여주고 하나 고르라고 하자
            for wt in webtoon:
                print(wt.name)
            webtoon_name = input('You can choose one of these: ')
            webtoon = self.find_webtoon(webtoon_name)
        # 리스트가 아닌 네임드 튜플(Webtoon)로 반환
        webtoon = webtoon[0]
        return webtoon

    @property
    # 최신 에피소드까지 몇화인가? (휴재 및 프롤로그 포함)
    def total_episode_count(self):
        # 첫 페이지의 episode_list 받아옴
        el = get_webtoon_episode_list(self.webtoon.title_id)
        # 그 마지막 에피소드의 no 값 출력
        return int(el[0].no)

    @property
    # 내 episode_list에 최신화가 있는가? ( True / False )
    def is_up_to_date(self):
        return len(self.episode_list) == self.total_episode_count
        # ------------------------------------------------
        # cur_episode_count = len(self.episode_list)
        # cur_episode_count = int(self.episode_list[0].no if self.episode_list != [] else 0)
        # total_episode_count = self.total_episode_count
        # return cur_episode_count == total_episode_count
        # ------------------------------------------------

    # 내 episode_list 업데이트
    def update_episode_list(self, force_update=False):
        # force_update인 경우 기존 episode_list 비우기
        if force_update:
            self.episode_list = list()
        # 아닌 경우 최신화가 있으면 업데이트 중단
        elif self.is_up_to_date:
            return
        # 최신 episode를 담을 그릇
        new_episode_list = []
        # 내가 가진 최신 episode 넘버
        recent_episode_no = int(self.episode_list[0].no if self.episode_list != [] else 0)
        # 그 값과 최신화의 차이를 10으로 나눈 몫 + 1
        # 에피소드를 가져오려면, 해당 웹툰 목록 페이지에서 긁어와야 하는데, 네이버 웹툰 페이지가 10화씩 보여주기 때문
        delta_no = (self.total_episode_count - recent_episode_no)//10 +1
        # 각 페이지에서 에피소드 긁어옴
        for i in range(1,delta_no+1):
            # 마지막 페이지에서 '내가 가진 최신화' 바로 전까지만 가져옴
            new_episode_list.extend(get_webtoon_episode_list(self.webtoon.title_id,i,recent_episode_no+1))
        # 새 episode_list를 기존 episode_list 앞에 저장
        self.episode_list = new_episode_list + self.episode_list
        # ------------------------------------------------
        # for i in self.episode_list:
        #     print(i)
        # ------------------------------------------------
        # episode_list를 pickle로 저장저장
        self.save()
        # 딱히 리턴할 게 없으니 몇개나 업데이트 했는지 알려주자
        return len(new_episode_list)

    @staticmethod
    # 문자열을 입력하면, 해당 문자열을 가진 웹툰 리스트를 반환
    def find_webtoon(user_input):
        webtoon_list = get_total_webtoon_list()
        user_webtoon = [ webtoon for webtoon in webtoon_list if user_input in webtoon.name ]
        return user_webtoon

    # episode_list pickle로 저장
    def save(self, path=None):
        # episode_list 디렉토리가 없으면 만들고
        if not os.path.isdir('./episode_list'):
            os.mkdir('./episode_list')
        path = './episode_list/{}.txt'.format(self.webtoon.title_id)
        # pickle로 저장
        pickle.dump(self.episode_list,open(path,'wb'))  # 참조되는 곳이 없는 파일 객체는 닫힌다.

    # episode_list pickle 불러오기
    def load(self, path=None, init=False):
        try:
            path = './episode_list/{}.txt'.format(self.webtoon.title_id)
            self.episode_list = pickle.load(open(path,'rb'))
        # 파일이 없을 때 에러 처리
        except FileNotFoundError:
            if not init:
                print('There no file on the path:{}'.format(path))
        return self.episode_list

    # 해당 webtoon의 전체 episode thumbnail을 저장
    def save_all_thumbnail_in_episode_list(self):
        # webtoon_id 폴더 안에 webtoon_id_thumbnail 폴더 생성. 이미 있어도 괜춘
        os.makedirs(f'./webtoon/{self.webtoon.title_id}/{self.webtoon.title_id}_thumbnail', exist_ok=True)
        for ep in self.episode_list:
            response = requests.get(ep.thumbnail_url)
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



# html_body = html_body.format(
#     img_url=item.img_url,
#     title=item.title,
#     rating=item.rating,
#     created_date=item.created_date
#     )

# 선천적 얼간이들 http://comic.naver.com/webtoon/list.nhn?title_id=697680&weekday=mon

# nwc = NaverWebtoonCrawlar()


# l = nwc.episode_list
# for i in nwc.episode_list:
#     print(i)

# payload = {'title_id':self.webtoon.title_id}
# response = requests.get('http://comic.naver.com/webtoon/list.nhn', params=payload)
# soup = BeautifulSoup(response.text, 'html.parser')
# webtoon_table = soup.select_one('table.viewList')
# tr_list = webtoon_table.find_all('tr', recursive=False)
