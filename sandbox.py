import requests
from bs4 import BeautifulSoup
with open('htmltest.html','w',encoding='u8')as f:
    r=requests.get('https://www.pealim.com/dict/1/')
    soup=BeautifulSoup(r.text,'html.parser')
    w=soup.find('table',{'class':'conjugation-table'})
    f.write(str(w))