import io

import requests
from bs4 import BeautifulSoup

language_dict = {0: 'all', 1: 'arabic', 2: 'german', 3: 'english', 4: 'spanish', 5: 'french', 6: 'hebrew',
                 7: 'japanese', 8: 'dutch', 9: 'polish', 10: 'portuguese', 11: 'romanian', 12: 'russian', 13: 'turkish'}


def print_v2(msg, **kwargs):
    print(msg, **kwargs)
    print(msg, file=stream, **kwargs)


def get_input():
    print('Hello, welcome to the translator. Translator supports:')
    for i, src_lan in language_dict.items():
        print(f'{i}. {src_lan.capitalize()}')
    print('Type the number of your language:')
    source_language = language_dict[int(input())]
    print("Type the number of a language you want to translate to or '0' to translate to all languages:")
    target_language = language_dict[int(input())]
    print('Type the word you want to translate:')
    word_to_translate = input()
    print('\n')
    return source_language, target_language, word_to_translate


def print_translations(src: str, trg: str, wrd: str, num: int = 1):
    url = f'https://context.reverso.net/translation/{src}-{trg}/{wrd}'
    while (response := s.get(url)).status_code != 200:
        pass

    soup = BeautifulSoup(response.content, 'html.parser')
    translations = [span.text for span in soup.find_all('span', {"class": "display-term"})]
    examples_source = [div.text.strip() for div in soup.find_all('div', class_="src")]
    examples_target = [div.text.strip() for div in soup.find_all('div', class_="trg")]

    print_v2(f'{trg.capitalize()} Translations:')
    for translation in translations[:num]:
        print_v2(translation, end='\n\n')

    print_v2(f'{trg.capitalize()} Examples:')
    for ex_source, ex_target in zip(examples_source[:num], examples_target[:num]):
        print_v2(ex_source)
        print_v2(ex_target, end='\n\n')


if __name__ == '__main__':
    stream = io.StringIO()
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0'})
    source, target, word = get_input()

    if target == 'all':
        for lan in (lan for lan in language_dict.values() if lan not in ('all', source)):
            print_translations(source, lan, word)
    else:
        print_translations(source, target, word)

    with open(f'{word}.txt', 'w', encoding="utf-8") as f:
        f.write(stream.getvalue())
