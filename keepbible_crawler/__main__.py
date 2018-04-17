from fuctions import *
from variables import *

bible_info_dict = {
    'bible_name': 'hkjv',
    'book_id': 1,
}
chapter_list = []

for book_id in range(1, 67):
    bible_info_dict['book_id'] = book_id
    chapter_list = crawl_chapters(**bible_info_dict)

    file_path = PROJECT_DIR + f'{BOOK_NAMES[book_id-1]}(흠정역).txt'
    with open(file_path, 'wt') as bookfile:
        for chapter in chapter_list:
            for verse in chapter.verse_list:
                line = f'{BOOK_NAMES_ABBR[book_id-1]}{chapter.number}:{verse.number} {verse.content}\n'
                append_file(bookfile, line)

    print(f'phase#{book_id}')
