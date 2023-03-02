import requests
from bs4 import BeautifulSoup

colspan4 = {1: [4], 2: [2, 2], 3: [1, 1, 2], 4: [1, 1, 1, 1]}


def lehateh(soup: BeautifulSoup, id: list[list[list[str]]]) -> str:
    table = '<table>'
    for i in id:
        table += '<tr>'
        for j, k in zip(i, colspan4[len(i)]):
            table += '<th'+(f' colspan=\"{k}\"'if k-1 else'')+'>'
            # TODO: KINDS OF CONJUGATIONS
            table += '</th>'
        table += '</tr><tr>'
        #TODO: CONJUGATIONS
        table += '</tr>'
    return table+'</table>'


with open('anki-hebrew.html', 'w', encoding='u8') as f:
    for wsn in [1]:
        r = requests.get(f'https://www.pealim.com/dict/{wsn}/')
        soup = BeautifulSoup(r.text, 'html.parser')
        pos = soup.h2.find_next('p').text
        meaning = soup.find('div', {'class': 'lead'})
        f.write(str(wsn)+'<br>{{c1::'+meaning.text+'}}<br>')
        conjtab = soup.find_all('table', {'class': 'conjugation-table'})
        id = []
        if pos.startswith('Verb'):
            id = [[['AP-ms'], ['AP-fs'], ['AP-mp'], ['AP-fp']],
                  [['PERF-3ms'], ['PERF-3fs'], ['PERF-3p']],
                  [['PERF-2ms'], ['PERF-2fs'], ['PERF-2mp'], ['PERF-2fp']],
                  [['PERF-1s'], ['PERF-1p']],
                  [['IMPF-3ms'], ['IMPF-3mp'], ['IMPF-3fs', 'IMPF-2ms']],
                  [['IMPF-2fs'], ['IMPF-2mp'], ['IMPF-3fp', 'IMPF-2fp']],
                  [['IMPF-1s'], ['IMPF-1p']]]
            if len(conjtab)-1:
                id += [[['passive-'+j for j in i]for i in k]for k in id]
                soup = BeautifulSoup(
                    str(conjtab[0])+str(conjtab[1]), 'html.parser')
            else:
                soup = BeautifulSoup(str(conjtab[0]), 'html.parser')
            id.insert(0, [['INF-L']])
            f.write(lehateh(soup, id))
        elif pos.startswith('Noun'):
            id = [[['s'],  ['p']],
                  [['sc'], ['pc']]]
            soup = BeautifulSoup(str(conjtab[0]), 'html.parser')
            f.write(lehateh(soup, id))
        elif pos.startswith('Adjective'):
            id = [[['ms-a'], ['fs-a']],
                  [['mp-a'], ['fp-a']]]
            soup = BeautifulSoup(str(conjtab[0]), 'html.parser')
            f.write(lehateh(soup, id))
        elif pos.startswith('Preposition'):
            id = [[['b']],
                  [['P-1s'], ['P-1p']],
                  [['P-2ms'], ['P-2fs'], ['P-2mp'], ['P-2fp']],
                  [['P-3ms'], ['P-3fs'], ['P-3mp'], ['P-3fp']]]
            soup = BeautifulSoup(str(conjtab[0]), 'html.parser')
            f.write(lehateh(soup, id))
        elif pos.startswith('Pronoun'):
            continue
        else:
            lead = meaning.find_next('div', {'class': 'lead'})
            f.write('{{c2::'+lead.find('span', {'class': 'menukad'}).text)
            try:
                f.write(lead.find('span', {'class': 'chaser'}).text)
            except:
                pass
            transcription = ''.join(
                map(str, lead.find('div', {'class': 'transcription'}).contents))
            f.write('<br>'+transcription+'}}')
        f.write('\n')
