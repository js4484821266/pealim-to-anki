import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from time import sleep

print('--- START ---')

# Check robots.txt compliance
rp = RobotFileParser()
rp.set_url('https://www.pealim.com/robots.txt')
try:
    rp.read()
    print('robots.txt loaded successfully')
except Exception as e:
    print(f'Warning: Could not load robots.txt ({e}), proceeding with caution')

user_agent = 'pealim-to-anki-bot'

with open(f'Hebrew.txt', 'w', encoding='u8') as f:
    for wsn in range(9123,9125):
        # prepare frame-*.html
        frame = {
            'PERF-3ms': open('frame-Verb.html', encoding='u8').read(),
            's': open('frame-Noun.html', encoding='u8').read(),
            'p': open('frame-Noun.html', encoding='u8').read(),
            'ms-a': open('frame-Adjective.html', encoding='u8').read(),
            'P-1s': open('frame-Preposition.html', encoding='u8').read()
        }

        url = f'https://www.pealim.com/dict/{wsn+1}/'
        
        # Check if URL is allowed by robots.txt
        if not rp.can_fetch(user_agent, url):
            print(f'SKIPPED (robots.txt): {wsn+1}')
            continue
        
        # Add delay to be respectful to the server (1 second between requests)
        sleep(1)
        
        r = requests.get(url, headers={'User-Agent': user_agent})
        if r.status_code != 200:
            print(f'ERROR {r.status_code}: {wsn+1}')
            continue
        print(wsn+1, end='\r')
        soup = BeautifulSoup(r.text, 'html.parser')

        # get part of speech
        pos=soup.find('h2',{'class':'page-header'}).find_next('p').text

        # write header
        r = [f'{wsn+1:05d}'+'<br>'+pos+'<br>']*2

        # get & pull out meaning
        r[0] += soup.find('div', {'class': 'lead'}).extract().text

        # decide which frame to use
        for i in frame:
            if soup.find('div', {'id': i}):
                frame = BeautifulSoup(frame[i], 'html.parser')
                break
        if frame is dict:
            frame = BeautifulSoup(
                '<div class="lead"></div>',
                'html.parser'
            )

        # get conjugation table
        t = soup.find('table', {'class': 'conjugation-table'})

        if t:
            if t.find('div', {'id': '1s'}):
                print(f'Pronoun: {wsn+1}')
                continue
            w = list(map(lambda x: x.div, t.find_all(
                'td', {'class': 'conj-td'})))
            w.insert(0, soup.find('div', {'id': 'b'}))
            for i in w:
                try:
                    j = i.attrs['id']
                    frame.find('div', {'id': j}).extend(
                        [k for k in i.contents
                         if 'class' not in k.attrs])
                except (AttributeError, KeyError):
                    pass
            r[1] += str(frame).replace('\n', '')
        else:
            try:
                w = soup.find('div', {'class': 'lead'}).contents
            except AttributeError:
                w = soup.find('div', {'id': 'b'}).contents
            for i in w:
                if 'class' in i.attrs:
                    continue
                i = i.contents
                r[1] += i[0].text+'<br>' + ''.join(
                    map(str, i[1].contents))
        f.write('\t'.join(r)+'\n')

print('--- END ---')
