from re import A
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
    #TODO: change base url
    #TODO: optimized the requests to 1 only for faster execution time
    base_url = "https://vnexpress.net"
    start_url = "https://vnexpress.net/giao-duc"
    next_url = start_url                            #compensate for starting the loop
    
    with open('output.txt', 'w') as output:
        while(True):
            req = requests.get(next_url)
            soup = BeautifulSoup(req.content, 'html.parser')
            
            #* Get title and desc of news 
            
            articleTags = soup.find_all('article')          # get all article
            
            for article in articleTags:
                
                title = get_title(article)
                
                if title:
                    output.write(title)
                    output.write('\n')
                
                desc = get_desc(article)
                
                if desc:
                    output.write(desc)
                    output.write('\n')
                else:
                    output.write('Desc: No description')
                    output.write('\n')
                    
            #* Find and Assign the next link
            
            a_tag = soup.find('a', class_='next-page')
            
            if a_tag is None:
                break
            
            next_url = base_url + a_tag['href']