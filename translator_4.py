import requests
from bs4 import BeautifulSoup

language_dict = {1: 'arabic', 2: 'german', 3: 'english', 4: 'spanish', 5: 'french', 6: 'hebrew', 7: 'japanese',
                 8: 'dutch', 9: 'polish', 10: 'portuguese', 11: 'romanian', 12: 'russian', 13: 'turkish'}


def get_input():
    print('Hello, welcome to the translator. Translator supports:')
    for i, lan in language_dict.items():
        print(f'{i}. {lan.capitalize()}')
    print('Type the number of your language:')
    source_language = language_dict[int(input())]
    print('Type the number of language you want to translate to:')
    target_language = language_dict[int(input())]
    print('Type the word you want to translate:')
    word_to_translate = input()
    print('\n')
    return source_language, target_language, word_to_translate


def get_translations():
    source, target, word = get_input()
    url = f'https://context.reverso.net/translation/{source}-{target}/{word}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    while (response := requests.get(url, headers=headers)).status_code != 200:
        pass

    soup = BeautifulSoup(response.content, 'html.parser')
    translations = [span.text for span in soup.find_all('span', {"class": "display-term"})]
    examples_source = [div.text.strip() for div in soup.find_all('div', {"class": "src ltr"})]
    examples_target = [div.text.strip() for div in soup.find_all('div', {"class": "trg ltr"})]

    print(f'{target.capitalize()} Translations:')
    print(*translations, end='\n\n', sep='\n')

    print(f'{target.capitalize()} Examples:')
    for ex_source, ex_target in zip(examples_source[:5], examples_target[:5]):
        print(ex_source)
        print(ex_target, end='\n\n')


if __name__ == '__main__':
    get_translations()
