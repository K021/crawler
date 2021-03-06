from typing import NamedTuple


__all__ = (
    'Book',
    'Chapter',
    'Verse',
    'PROJECT_DIR',
    'KEEPBIBLE_URL',
    'BOOK_NAMES',
    'BOOK_NAMES_ABBR',
)


class Book(NamedTuple):
    book: str
    book_id: int
    chapter_list: list


class Chapter(NamedTuple):
    book: str
    book_id: int
    number: int
    verse_list: list


class Verse(NamedTuple):
    number: int
    content: str


PROJECT_DIR = '/Users/ElohimAwmar/python/Crawler/keepbible_crawler/'

KEEPBIBLE_URL = 'http://keepbible.com/html/bible_list.html'

BOOK_NAMES = (
    '창세기',
    '출애굽기',
    '레위기',
    '민수기',
    '신명기',
    '여호수아',
    '사사기',
    '룻기',
    '사무엘상',
    '사무엘하',
    '열왕기상',
    '열왕기하',
    '역대상',
    '역대하',
    '에스라',
    '느헤미야',
    '에스더',
    '욥기',
    '시편',
    '잠언',
    '전도서',
    '아가',
    '이사야',
    '예레미야',
    '예레미야 애가',
    '에스겔',
    '다니엘',
    '호세아',
    '요엘',
    '아모스',
    '오바댜',
    '요나',
    '미가',
    '나훔',
    '하박국',
    '스바냐',
    '학개',
    '스가랴',
    '말라기',
    '마태복음',
    '마가복음',
    '누가복음',
    '요한복음',
    '사도행전',
    '로마서',
    '고린도전서',
    '고린도후서',
    '갈라디아서',
    '에베소서',
    '빌립보서',
    '골로새서',
    '데살로니가전서',
    '데살로니가후서',
    '디모데전서',
    '디모데후서',
    '디도서',
    '빌레몬서',
    '히브리서',
    '야고보서',
    '베드로전서',
    '베드로후서',
    '요한1서',
    '요한2서',
    '요한3서',
    '유다서',
    '요한계시록',
)

BOOK_NAMES_ABBR = (
    '창',
    '출',
    '레',
    '민',
    '신',
    '수',
    '삿',
    '룻',
    '삼상',
    '삼하',
    '왕상',
    '왕하',
    '대상',
    '대하',
    '스',
    '느',
    '에',
    '욥',
    '시',
    '잠',
    '전',
    '아',
    '사',
    '렘',
    '애',
    '겔',
    '단',
    '호',
    '욜',
    '암',
    '옵',
    '욘',
    '미',
    '나',
    '합',
    '습',
    '학',
    '슥',
    '말',
    '마',
    '막',
    '눅',
    '요',
    '행',
    '롬',
    '고전',
    '고후',
    '갈',
    '엡',
    '빌',
    '골',
    '살전',
    '살후',
    '딤전',
    '딤후',
    '딛',
    '몬',
    '히',
    '약',
    '벧전',
    '벧후',
    '요일',
    '요이',
    '요삼',
    '유',
    '계',
)
