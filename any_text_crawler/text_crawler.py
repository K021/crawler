import requests
from bs4 import BeautifulSoup


def text_crawler(source_path):
    source = requests.get(source_path)
    soup = BeautifulSoup(source.text, 'lxml')
    wrap_tag = soup.select_one('section.m-b:7')
    target_tag = wrap_tag.find_all('a', class_='t-d:n')
    text = ''

    for tag in target_tag:
        text += tag.get_text()

    return text


if __name__ == '__main__':
    source_url = 'https://www.ted.com/talks/emily_esfahani_smith_there_s_more_to_life_than_being_happy/transcript#t-5001'
    print(text_crawler(source_url))
