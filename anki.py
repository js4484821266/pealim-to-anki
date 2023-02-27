import requests
from bs4 import BeautifulSoup


def fusion(soup: BeautifulSoup, id: list) -> str:
    for i in id:
        table = '<table><tr>'
        dii = soup.find('div', {'id': i[0]})
        table += '<th>'+'<br>'.join(i)+'</th><td>'
        menukadim = list(map(str, dii.find_all(
            'span', {'class': 'menukad'})))
        chaserim = list(map(str, dii.find_all(
            'span', {'class': 'chaser'})))
        if not chaserim:
            chaserim = ['']*len(menukadim)
        transcriptions = dii.find_all(
            'div', {'class': 'transcription'})
        transcriptions = [''.join(map(str, i.contents))
                          for i in transcriptions]
        zip(menukadim, chaserim, transcriptions)
        table += '</td></tr></table>'


with open('anki-hebrew.html', 'w', encoding='u8') as f:
    for wsn in [1230]:
        r = requests.get('https://www.pealim.com/dict/{}/'
                         .format(wsn))
        soup = BeautifulSoup(r.text, 'html.parser')
        pos = soup.h2.find_next('p').text
        conjtab = soup.find_all('table', {
            'class': 'conjugation-table'
        })
        id = []
        if pos.startswith('Verb'):
            id = [['AP-ms'], ['AP-fs'], ['AP-mp'], ['AP-fp'],
                  ['PERF-3ms'], ['PERF-3fs'], ['PERF-3p'],
                  ['PERF-2ms'], ['PERF-2fs'], ['PERF-2mp'],
                  ['PERF-2fp'], ['PERF-1s'], ['PERF-1p'],
                  ['IMPF-3ms'], ['IMPF-3mp'],
                  ['IMPF-3fs', 'IMPF-2ms'], ['IMPF-2fs'],
                  ['IMPF-2mp'], ['IMPF-3fp', 'IMPF-2fp'],
                  ['IMPF-1s'], ['IMPF-1p']]
            if len(conjtab)-1:
                id += [['passive-'+j for j in i] for i in id]
                soup = BeautifulSoup(
                    str(conjtab[0])+str(conjtab[1]),
                    'html.parser')
            else:
                soup = BeautifulSoup(
                    str(conjtab[0]),
                    'html.parser')
            id.insert(0, ['INF-L'])
        elif pos.startswith('Noun'):
            id = ['s', 'p', 'sc', 'pc']
        elif pos.startswith('Adjective'):
            id = ['ms-a', 'fs-a', 'mp-a', 'fp-a']
        elif pos.startswith('Preposition'):
            id = ['P-1s', 'P-2ms', 'P-2fs', 'P-3ms', 'P-3fs',
                  'P-1p', 'P-2mp', 'P-2fp', 'P-3mp', 'P-3fp']
        elif pos.startswith('Adverb'):
            pass
        else:
            continue
