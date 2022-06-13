from re import A
import requests
from bs4 import BeautifulSoup

def getTitle(article):
    h3_tag = article.findAll('h3', class_='title-news')
    if len(h3_tag) >= 1:
        a_tag = h3_tag[0].find('a').string
        print('Title: ' + a_tag)
        
def getDesc(article):
    p_tag = article.findAll('p', class_='description')
    if len(p_tag) >= 1 and p_tag[0].find('a').string:
        p_content = p_tag[0].find('a').string
        print('Desc: ' + p_content)

base_url = "https://vnexpress.net"
url = "https://vnexpress.net/giao-duc"

req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

# get all article
articleTags = soup.findAll('article')

obj = {}

for article in articleTags:
    # get the h3 tags in article
    getTitle()
    
    # get p tag with class='description'
    getDesc()
        
# get title from class='title-news'
# get desc from class='description'