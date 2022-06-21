import requests
from bs4 import BeautifulSoup

def get_title(article):
    """Return the title of the news"""
    h3_tag = article.find('h3', class_='title-news')
    if h3_tag:
        a_tag = h3_tag.find('a').string.strip()
        return str(a_tag)
        
def get_desc(article):
    """Return the description of the news"""
    p_tag = article.find('p', class_='description')
    if p_tag:
        test = p_tag.find('a').contents
        for item in test:
            if item.name == 'span':
                continue
            description = item
        return str(description)

def scrape():
    #compensate for starting the loop
    base_url = "https://vnexpress.net/giao-duc"
    list_content = []
    
    while(True):
        req = requests.get(base_url)
        soup = BeautifulSoup(req.content, 'html.parser')
        
        #* Get title and desc of news
        articleTags = soup.find_all('article')
        
        for article in articleTags:
            article_dict = {}
            article_dict['title'] = get_title(article)
            article_dict['desc'] = get_desc(article)
            
            if not article_dict['title']:
                continue
            if not article_dict['desc']:
                article_dict['desc'] = "N/A"
                
            list_content.append(article_dict)
                
        #* Find and Assign the next link
        a_tag = soup.find('a', class_='next-page')
        
        if not a_tag:
            break
        
        base_url = "https://vnexpress.net" + a_tag['href']
        
    return list_content