import requests
from bs4 import BeautifulSoup

def get_title(article):
    """Return the title of the news"""
    h3_tag = article.find_all('h3', class_='title-news')
    if len(h3_tag) >= 1:
        a_tag = h3_tag[0].find('a').string.strip()
        return 'Title: ' + a_tag
        
def get_desc(article):
    """Return the description of the news"""
    p_tag = article.find_all('p', class_='description')
    if len(p_tag) >= 1 and p_tag[0].find('a').string:
        p_content = p_tag[0].find('a').string.strip()
        return 'Desc: ' + p_content

if __name__ == "__main__":
    #compensate for starting the loop
    base_url = "https://vnexpress.net/giao-duc"
    
    while(True):
        req = requests.get(base_url)
        soup = BeautifulSoup(req.content, 'html.parser')
        
        #* Get title and desc of news
        articleTags = soup.find_all('article')
        
        for article in articleTags:
            title = get_title(article)
            desc = get_desc(article)
                
        #* Find and Assign the next link
        a_tag = soup.find('a', class_='next-page')
        
        if not a_tag:
            break
        
        base_url = "https://vnexpress.net" + a_tag['href']