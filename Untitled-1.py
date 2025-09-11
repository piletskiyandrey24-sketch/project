import requests
from bs4 import BeautifulSoup

url = "https://github.com/"
responce = requests.get(url)
code = responce.text
soup = BeautifulSoup(code, features='html.parser')



print("\n5. Изображения:")    
images = soup.find_all('img', scr=True)
for i in images[:5]:
    scr = i.get('scr')
    alt = i.get('alt', 'Без описания')
    print(f" Изображение: {scr}") 
    print(f" Описание: {alt}")
    print()