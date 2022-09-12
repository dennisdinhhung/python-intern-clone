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


def save_articles(articles):
    for article in articles:
        title = article["title"]
        description = article["description"]
        url = article['url']
        if not Articles.objects.filter(url=url).exists():
            Articles.objects.create(title=title, description=description, url=url)


def get_articles(page):
    base_url = f'{settings.VNEXPRESS_URL}/giao-duc-p{page}'
    req = requests.get(base_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    article_tags = soup.find_all('article')
    articles = []
    for article in article_tags:
        article_dict = {
            'title': get_title(article),
            'description': get_desc(article),
            'url': get_url(article)}
        if not article_dict['title']:
            continue
        if not article_dict['description']:
            continue
        articles.append(article_dict)

    if soup.find('a', class_='next-page'):
        is_next_page = True
    else:
        is_next_page = False
    return articles, is_next_page


@celery_app.task(name='tasks.article_scraper', bind=True, default_retry_delay=3, autoretry_for=(Exception,))
def crawl(self, page=1):
    articles, is_next_page = get_articles(page)
    save_articles(articles)
    if is_next_page:
        celery_app.send_task('tasks.article_scraper', (page + 1,))
