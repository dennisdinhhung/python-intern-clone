from re import A
import requests
from bs4 import BeautifulSoup

headers = {
    
}

url = "https://vnexpress.net/giao-duc"

req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

# get all article
articleTags = soup.findAll('article')

obj = {}

for article in articleTags:
    # get the h3 tags in article
    h3_tag = article.findAll('h3', class_='title-news')
    if len(h3_tag) >= 1:
        a_tag = h3_tag[0].find('a').string
        print('Title' + a_tag)
        
# get title from class='title-news'
# get desc from class='description'