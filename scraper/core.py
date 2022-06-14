from re import A
import requests
from bs4 import BeautifulSoup

def getTitle(article):
    h3_tag = article.find_all('h3', class_='title-news')
    if len(h3_tag) >= 1:
        a_tag = h3_tag[0].find('a').string.strip()
        return 'Title: ' + a_tag
        
def getDesc(article):
    p_tag = article.find_all('p', class_='description')
    if len(p_tag) >= 1 and p_tag[0].find('a').string:
        p_content = p_tag[0].find('a').string.strip()
        return 'Desc: ' + p_content

def main():
    base_url = "https://vnexpress.net"
    start_url = "https://vnexpress.net/giao-duc"
    next_url = start_url
    urls = []
    
    while(True):
        req = requests.get(next_url)
        soup = BeautifulSoup(req.content, 'html.parser')
        
        a_tag = soup.find('a', class_='next-page')
        
        if a_tag is None:
            break
        
        next_url = base_url + a_tag['href']
        urls.append(next_url)

    

    with open('output.txt', 'w') as output:
        for url in urls:
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html.parser')

            # get all article
            articleTags = soup.find_all('article')
            
            for article in articleTags:
                
                title = getTitle(article)
                
                if title is not None:
                    # get the h3 tags in article
                    output.write(getTitle(article))
                    output.write('\n')
                
                desc = getDesc(article)
                
                if desc is not None:
                    # get p tag with class='description'
                    output.write(getDesc(article))
                    output.write('\n')
                else:
                    output.write('Desc: No description')
                    output.write('\n')
            
main()