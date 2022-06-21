import requests
from bs4 import BeautifulSoup

print('Type "en" if you want to translate from French into English,', end=' ')
print('or "fr" if you want to translate from English into French:')
language = input()
source, target = ('french', 'english') if language == 'en' else ('english', 'french')

print('Type the word you want to translate:')
word = input()

print(f'You chose "{language}" as a language to translate "{word}".')

url = f'https://context.reverso.net/translation/{source}-{target}/{word}'
headers = {'User-Agent': 'Mozilla/5.0'}
while (response := requests.get(url, headers=headers)).status_code != 200:
    pass
print('200 OK', end='\n\n')

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
