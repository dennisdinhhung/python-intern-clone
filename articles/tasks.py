import requests

from bs4 import BeautifulSoup
from django.conf import settings

from articles.models import Articles
from articles.serializers import ArticleCreateSerializer
from project.celery import app as celery_app


def get_title(article):
    """Return the title of the news"""
    h3_tag = article.find('h3', class_='title-news')
    if not h3_tag:
        return None
    a_tag = h3_tag.find('a').string.strip()
    return str(a_tag)


def get_desc(article):
    """Return the description of the news"""
    description = None
    p_tag = article.find('p', class_='description')
    if not p_tag:
        return None
    description = p_tag.find('a')['title']
    return str(description)


def get_url(article):
    """Return the href/link of the news"""
    h3_tag = article.find('h3', class_='title-news')
    if not h3_tag:
        return None
    a_tag = h3_tag.find('a')['href']
    return str(a_tag)


def save_articles(articles):
    for article in articles:
        title = article["title"]
        description = article["description"]
        url = article['url']
        if not Articles.objects.filter(url=url).exists():
            Articles.objects.create(title=title, description=description, url=url)


def get_articles(html_content):
    article_tags = html_content.find_all('article')
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
        serializer = ArticleCreateSerializer(data=article_dict)
        if not serializer.is_valid():
            continue
        data = Articles(**serializer.validated_data)
        articles.append(data)
    # TODO: bug: repeated articles, need to check with database
    return articles


def is_next_page(html_content):
    if html_content.find('a', class_='next-page'):
        return True
    return False


@celery_app.task(name='tasks.article_scraper', bind=True, default_retry_delay=3, autoretry_for=(Exception,),
                 retry_kwargs={'max_retries': 5})
def crawl(self, page=1):
    base_url = f'{settings.VNEXPRESS_URL}/giao-duc-p{page}'
    req = requests.get(base_url)
    html_content = BeautifulSoup(req.content, 'html.parser')
    articles = get_articles(html_content)
    Articles.objects.bulk_create(articles)
    if is_next_page(html_content):
        celery_app.send_task('tasks.article_scraper', (page + 1,))
