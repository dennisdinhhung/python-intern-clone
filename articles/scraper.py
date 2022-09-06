import requests
from bs4 import BeautifulSoup
from django.conf import settings

from articles.models import Articles
from project.celery import app as celery_app


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
    
def get_url(article):
    """Return the href/link of the news"""
    h3_tag = article.find('h3', class_='title-news')
    if h3_tag:
        a_tag = h3_tag.find('a')['href']
        return str(a_tag)

def save(list_content):
    for item in list_content:
        title = item["title"]
        description = item["description"]
        url = item['url']
        if not Articles.objects.filter(url=url).exists():
            Articles.objects.create(title=title, description=description, url=url)

@celery_app.task(name='celery_scraper', bind=True)
def crawl(self, base_url):
    list_content = []
    req = requests.get(base_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    
    # Get title and description of news
    articleTags = soup.find_all('article')
    for article in articleTags:
        article_dict = {}
        article_dict['title'] = get_title(article)
        article_dict['description'] = get_desc(article)
        article_dict['url'] = get_url(article)
        if not article_dict['title']:
            continue
        if not article_dict['description']:
            continue
        list_content.append(article_dict)
    save(list_content)
    
    a_tag = soup.find('a', class_='next-page')
    if a_tag:
        next_url = settings.VNEXPRESS_URL + a_tag['href']
        # crawl(base_url=next_url)
        celery_app.send_task('celery_scraper', (next_url, ))
        

def scrape(self):
    crawl(base_url=settings.VNEXPRESS_URL + '/giao-duc')