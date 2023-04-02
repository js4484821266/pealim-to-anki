import requests
from bs4 import BeautifulSoup
with open('anki-hebrew.html', 'w', encoding='u8') as f:
    for wsn in [1]:
        r = requests.get(f'https://www.pealim.com/dict/{wsn}/')
        soup = BeautifulSoup(r.text, 'html.parser')
        pos = soup.h2.find_next('p').text
        meaning = soup.find('div', {'class': 'lead'})