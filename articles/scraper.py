import re
import requests

from bs4 import BeautifulSoup
from django.conf import settings

from articles.models import Articles
from project.tasks import app as celery_app


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


def save(article_tags):
    """Save article"""
    list_articles = []
    for article in article_tags:
        article_dict = {
            'title': get_title(article),
            'description': get_desc(article),
            'url': get_url(article)}
        if not article_dict['title']:
            continue
        if not article_dict['description']:
            continue
        list_articles.append(article_dict)
    # Articles.objects.bulk_create(list_articles)

    # try bulk create here

    for item in list_articles:
        title = item["title"]
        description = item["description"]
        url = item['url']
        if not Articles.objects.filter(url=url).exists():
            Articles.objects.create(title=title, description=description, url=url)


def get_next_page(base_url):
    # try to get the next page
    req = get_next_page(base_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    next_article_tags = soup.find_all('article')
    if next_article_tags:
        return True
    return False


@celery_app.task(name='tasks.article_scraper', bind=True)
def crawl(self, page=1):
    base_url = f'{settings.VNEXPRESS_URL}/giao-duc-p{page}'
    try:
        req = requests.get(base_url)
        soup = BeautifulSoup(req.content, 'html.parser')
        article_tags = soup.find_all('article')
    except requests.exceptions.RequestException as e:
        raise self.retry(exec=e, countdown=5)
    save(article_tags)

    page = get_next_page(base_url)
    if page:
        celery_app.send_task('tasks.article_scraper', (page + 1,))
