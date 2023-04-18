import requests
from bs4 import BeautifulSoup
with open(f'Hebrew.txt', 'w', encoding='u8') as f:
    for wsn in range(1000,2000):
        r = requests.get(f'https://www.pealim.com/dict/{wsn+1}/')
        if r.status_code != 200:
            print(f'\nERROR {r.status_code}: {wsn+1}')
            continue
        print(f'{wsn+1}',end=' ')
        soup = BeautifulSoup(r.text, 'html.parser')
        pos = soup.h2.find_next('p').text
        h = f'{wsn+1:05d}'+'<br>' + pos
        if pos in ['Adverb', 'Conjunction', 'Particle']:
            meaning, w = soup.find_all('div', {'class': 'lead'})
            r=[h]*2
            r[0] +='<br>'+ meaning.text
            w = w.contents
            for i in w:
                i = i.contents
                r[1] += '<br>'+i[0].text+'<br>'
                r[1] += ''.join(map(str, i[1].contents))
            f.write('\t'.join(r)+'\n')
        elif pos == 'Pronoun':
            print(f'{pos} {wsn+1}')
            continue
        else:
            meaning = soup.find('div', {'class': 'lead'})
            w = soup.find_all('td', {'class': 'conj-td'})
            w = [i.div for i in w]
            for i in w:
                r=[h]*2
                r[0] +='<br>'+i.attrs['id']+'<br>' + meaning.text
                i = [d for d in i.contents if 'class'not in d.attrs]
                for j in i:
                    j = j.contents
                    r[1] +='<br>'+ j[0].text+'<br>'
                    r[1] += ''.join(map(str, j[1].contents))
                f.write('\t'.join(r)+'\n')
