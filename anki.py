import requests
from bs4 import BeautifulSoup
with open(f'Hebrew.txt', 'w', encoding='u8') as f:
    for wsn in range(10,100):
        r = requests.get(f'https://www.pealim.com/dict/{wsn+1}/')
        if r.status_code != 200:
            print(f'Error: {wsn+1} {r.status_code}')
            continue
        print(f'Processing: {wsn+1}')
        soup = BeautifulSoup(r.text, 'html.parser')
        pos = soup.h2.find_next('p').text
        r = [pos]*2
        if pos in ['Adverb', 'Conjunction', 'Particle']:
            meaning, w = soup.find_all('div', {'class': 'lead'})
            r[0] += '<br>' + meaning.text
            w = w.contents
            for i in w:
                i = i.find_all('div')
                r[1] += '<br>'+i[0].text+'<br>'
                r[1] += ''.join(map(str, i[1].contents))
            f.write('\t'.join(r)+'\n')
        elif pos == 'Pronoun':
            continue
        else:
            meaning = soup.find('div', {'class': 'lead'})
            w = soup.find_all('td', {'class': 'conj-td'})
            w = [i.div for i in w]
            for i in w:
                r[1] = pos+'<br>'
                r[0] = r[1]+i.attrs['id']+'<br>'
                r[0] += meaning.text
                i = [d for d in i.contents if 'class'not in d.attrs]
                for j in i:
                    j = j.contents
                    r[1] += j[0].text+'<br>'+''.join(map(str, j[1].contents))
                f.write('\t'.join(r)+'\n')
