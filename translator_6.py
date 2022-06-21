import argparse
import io

import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Stage 6/7: Faster translation')
parser.add_argument('source', type=str, help="Source language")
parser.add_argument('target', type=str, help="Target language (or all)")
parser.add_argument('word', type=str, help="Word to be translated")
args = parser.parse_args()

language_dict = {0: 'all', 1: 'arabic', 2: 'german', 3: 'english', 4: 'spanish', 5: 'french', 6: 'hebrew',
                 7: 'japanese', 8: 'dutch', 9: 'polish', 10: 'portuguese', 11: 'romanian', 12: 'russian', 13: 'turkish'}


def print_v2(*print_args, **kwargs):
    print(*print_args, **kwargs)
    print(*print_args, file=stream, **kwargs)


def print_translations(src: str, trg: str, wrd: str, num: int = 1):
    url = f'https://context.reverso.net/translation/{src}-{trg}/{wrd}'
    while (response := s.get(url)).status_code != 200:
        pass

    soup = BeautifulSoup(response.content, 'html.parser')
    translations = [span.text.strip() for span in soup.find_all('a', class_="translation")]
    examples_source = [div.text.strip() for div in soup.find_all('div', class_="src")]
    examples_source = list(filter(None, examples_source))
    examples_target = [div.text.strip() for div in soup.find_all('div', class_="trg") if len(div.text) > 0]
    examples_target = list(filter(None, examples_target))

    print_v2(f'{trg.capitalize()} Translations:')
    print_v2('\n'.join(translations[:num]), end='\n\n')
    print_v2(f'{trg.capitalize()} Examples:')
    for ex_source, ex_target in zip(examples_source[:num], examples_target[:num]):
        print_v2(ex_source)
        print_v2(ex_target, end='\n\n')


if __name__ == '__main__':
    stream = io.StringIO()
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0'})

    if args.target == 'all':
        for lan in (lan for lan in language_dict.values() if lan not in ('all', args.source)):
            print_translations(args.source, lan, args.word)
    else:
        print_translations(args.source, args.target, args.word, 5)

    with open(f'{args.word}.txt', 'w', encoding="utf-8") as f:
        f.write(stream.getvalue())
