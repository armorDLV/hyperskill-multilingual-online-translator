import requests
from bs4 import BeautifulSoup

print('Type "en" if you want to translate from French into English,'
      'or "fr" if you want to translate from English into French:')

language = input()

print('Type the word you want to translate:')

word = input()

print(f'You chose "{language}" as a language to translate "{word}".')

from_to = 'english-french' if language == 'fr' else 'french-english'
url = f'https://context.reverso.net/translation/{from_to}/{word}'

response = None
while True:
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code == 200:
        print('200 OK')
        break

print('Translations')

soup = BeautifulSoup(response.content, 'html.parser')
spans = [span.text for span in soup.find_all('span', {"class": "display-term"})]

examples_1 = [div.text.strip() for div in soup.find_all('div', {"class": "src ltr"})]
examples_2 = [div.text.strip() for div in soup.find_all('div', {"class": "trg ltr"})]

examples = []
for a, b in zip(examples_1, examples_2):
    examples.append(a)
    examples.append(b)

print(spans)
print(examples)
