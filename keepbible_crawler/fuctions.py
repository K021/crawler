import io
import time

import requests
from bs4 import BeautifulSoup

from variables import KEEPBIBLE_URL, BOOK_NAMES, PROJECT_DIR, BOOK_NAMES_ABBR
from variables import Book, Verse, Chapter


__all__ = (
    'crawl_books_and_write',
    'crawl_books',
    'crawl_chapters',
    'crawl_verses',
    'consumed_time',
    'append_file',
)


def crawl_books_and_write(separately=True):
    bible_info_dict = {
        'bible_name': 'hkjv',
        'book_id': 1,
    }

    for book_id in range(1, 67):
        bible_info_dict['book_id'] = book_id
        chapter_list = crawl_chapters(**bible_info_dict)

        file_path = PROJECT_DIR + f'{BOOK_NAMES[book_id-1]}(흠정역).txt' if separately else PROJECT_DIR + '신구약(흠정역).txt'
        for chapter in chapter_list:
            for verse in chapter.verse_list:
                line = f'{BOOK_NAMES_ABBR[book_id-1]}{chapter.number}:{verse.number} {verse.content}\n'
                append_file(file_path, line)

        print(f'phase#{book_id}')


def crawl_books(bible_name='hkjv'):
    bible_info_dict = {
        'bible_name': bible_name,
        'book_id': 1,
    }
    book_list = []
    for book_id in range(1, 67):
        bible_info_dict['book_id'] = book_id
        book_name = BOOK_NAMES[book_id - 1]
        book_list.append(
            Book(
                book=book_name,
                book_id=book_id,
                chapter_list=crawl_chapters(**bible_info_dict)
            )
        )
        if book_id % 3 == 2:
            time.sleep(5)
    return book_list


def crawl_chapters(bible_name='hkjv', book_id=1):
    bible_info_dict = {
        'bible_name': bible_name,
        'book_id': book_id,
        'chap_num': 1,
    }
    chapter_list = []
    book_name = BOOK_NAMES[book_id-1]

    for chapter_number in range(1, 151):
        bible_info_dict['chap_num'] = chapter_number
        verse_list = crawl_verses(**bible_info_dict)
        if not verse_list:
            break
        chapter_list.append(
            Chapter(
                book=book_name,
                book_id=book_id,
                number=chapter_number,
                verse_list=verse_list,
            )
        )
        if chapter_number in [50, 100, 150]:
            time.sleep(5)

    return chapter_list


def crawl_verses(bible_name='hkjv', book_id=1, chap_num=1):
    """
    keepbible 이 chapter 단위로 성경을 보여주는 것을 이용,
    chapter 단위로 verse 정보를 긁어서 Verse(NamedTuple) list 로 반환한다.

    :param bible_name: 성경 버전. 기본값은 흠정역('hkjv').
    :param book_id: 성경의 책 66권의 각 번호. 창세기는 1, 계시록은 66.
    :param chap_num: 각 책의 챕터.
    :return: 챕터 별 verse 정보를 담은 Verse(NamedTuple) list
    """

    bible_info_dict = {
        'bible_name': bible_name,
        'book_id': book_id,
        'chap_num': chap_num,
    }

    request = requests.get(KEEPBIBLE_URL, params=bible_info_dict)

    soup = BeautifulSoup(request.text, 'lxml')
    soup_list = soup.select('td.t5.b5')

    verse_list = []
    for tag in soup_list:
        verse_list.append(
            Verse(
                number=int(tag.parent.contents[0].text),
                content=tag.parent.contents[1].text,
            )
        )

    return verse_list


def consumed_time(func):
    start = time.time()
    func()
    end = time.time()
    return end - start


def append_file(file, string):
    if isinstance(file, str):  # file path 가 주어진 경우
        with open(file, 'a') as f:
            f.seek(0, 2)
            f.write(string)
    elif isinstance(file, io.TextIOBase):  # text file object 인 경우
        file.seek(0, 2)
        file.write(string)
    else:
        raise ValueError('append_file 함수에는 file path 또는 text file object 만을 매개변수로 받습니다.')
