
import subprocess
from crawler import NaverWebtoonCrawlar
from utils import Webtoon, get_webtoon_episode_list, get_total_webtoon_list


def choose_episode(nwc):
    chosen_episode_list = list()
    user_input_episode = input('Choose one of these episodes: ')
    num_of_corresponding_episode = 0
    for ep in nwc.episode_list:
        if user_input_episode in ep.title:
            print(ep.title)
            chosen_episode_list.append(ep)
    return chosen_episode_list


def webtoon_crawler(webtoon_name=None):
    # 네이버 웹툰 크롤러 클래스 생성
    nwc = NaverWebtoonCrawlar(webtoon_name)

    nwc.update_episode_list()
    for ep in nwc.episode_list:
        print(ep.title)

    chosen_episode_list = list()
    while len(chosen_episode_list) != 1:
        chosen_episode_list = choose_episode(nwc)
        if len(chosen_episode_list) == 0:
            print('No corresponding episode. Try again.')
            continue
        elif len(chosen_episode_list) > 10:
            print('You cannot load more than 10 episodes.')
            continue
        elif len(chosen_episode_list) != 1:
            print("Corresponding episodes are more than one.")
            user_input = input('Type 1 to proceed or any keys to choose again: ')
            if user_input == '1':
                break

    for ep in chosen_episode_list:
        ep.webtoon = nwc.webtoon
        ep.save_all()

    path = f'./webtoon/{nwc.webtoon.title_id}/{nwc.webtoon.title_id}.html'
    subprocess.call(['open', path])

    return nwc


if __name__ == '__main__':
    keep_going = True
    webtoon_name = None
    while keep_going:
        wc = webtoon_crawler(webtoon_name)
        keep_going = input('Type 1 to choose another episode, 2 for another webtoon, or any keys to stop: ')
        if keep_going == '1':
            webtoon_name = wc.webtoon.name
        elif keep_going == '2':
            webtoon_name = None
        else:
            break
