import requests
from bs4 import BeautifulSoup
print('--- START ---')
frame = None
with open(f'Hebrew.txt', 'w', encoding='u8') as f:
    for wsn in range(1000):
        r = requests.get(f'https://www.pealim.com/dict/{wsn+1}/')
        if r.status_code != 200:
            print(f'ERROR {r.status_code}: {wsn+1}')
            continue
        print(wsn+1, end='\r')
        soup = BeautifulSoup(r.text, 'html.parser')
        pos = soup.h2.find_next('p').text
        for i in ['Verb', 'Noun', 'Adjective', 'Preposition']:
            if pos .startswith(i):
                frame = BeautifulSoup(
                    open(f'frame-{i}.html', encoding='u8'),
                    'html.parser'
                )
                break
        r = [f'{wsn+1:05d}'+'<br>' + pos+'<br>']*2
        if pos in ['Adverb', 'Conjunction', 'Particle']:
            meaning, w = soup.find_all('div', {'class': 'lead'})
            r[0] += meaning.text
            w = w.contents
            for i in w:
                i = i.contents
                r[1] += i[0].text+'<br>'
                r[1] += ''.join(map(str, i[1].contents))
            f.write('\t'.join(r)+'\n')
        elif pos == 'Pronoun':
            print(f'{pos} {wsn+1}')
            continue
        else:
            meaning = soup.find('div', {'class': 'lead'})
            w = map(lambda x: x.div, soup.find_all('td', {'class': 'conj-td'}))
            for i in w:
                try:
                    j = i.attrs['id']
                    frame.find('div', {'id': j}).extend(
                        [k for k in i.contents 
                         if 'class' not in k.attrs])
                except:
                    pass
            r[0] += meaning.text
            r[1] += str(frame).replace('\n', '')
            f.write('\t'.join(r)+'\n')
print('--- END ---')
