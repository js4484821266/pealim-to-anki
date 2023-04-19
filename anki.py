import requests
from bs4 import BeautifulSoup
print('--- START ---')

# prepare frame-*.html
frame = {
    'INF-L': open('frame-Verb.html', encoding='u8').read(),
    'sc': open('frame-Noun.html', encoding='u8').read(),
    'ms-a': open('frame-Adjective.html', encoding='u8').read(),
    'b': open('frame-Preposition.html', encoding='u8').read(),
    'lead': '<div class="lead"></div>'
}

with open(f'Hebrew.txt', 'w', encoding='u8') as f:
    for wsn in [2682-1]:
        r = requests.get(f'https://www.pealim.com/dict/{wsn+1}/')
        if r.status_code != 200:
            print(f'ERROR {r.status_code}: {wsn+1}')
            continue
        print(wsn+1, end='\r')
        soup = BeautifulSoup(r.text, 'html.parser')

        # write header
        r = [f'{wsn+1:05d}'+'<br>']*2

        # get & pull out meaning
        r[0] += soup.find('div', {'class': 'lead'}).extract().text

        # decide which frame to use
        for i in frame:
            if soup.find('div', {'id': i}):
                frame = BeautifulSoup(frame[i], 'html.parser')
                break

        # get conjugation table
        t = soup.find('div', {'id': 'conjugation-table'})

        if t:
            if t.find('div', {'id': '1s'}):
                continue
            w = list(map(lambda x: x.div, t.find_all(
                'td', {'class': 'conj-td'})))
            w.insert(0,soup.find('div', {'id': 'b'}))
            for i in w:
                try:
                    j = i.attrs['id']
                    frame.find('div', {'id': j}).extend(
                        [k for k in i.contents
                         if 'class' not in k.attrs])
                except:
                    pass
            r[1] += str(frame).replace('\n', '')
        else:
            w = soup.find('div', {'class': 'lead'}).contents
            for i in w:
                i = i.contents
                r[1] += i[0].text+'<br>'
                r[1] += ''.join(map(str, i[1].contents))
        f.write('\t'.join(r)+'\n')

print('--- END ---')
