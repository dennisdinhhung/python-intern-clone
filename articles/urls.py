from django.urls import path

from articles.views import ArticleDetail, ArticleList, ArticleScraper

urlpatterns = [
    path('', ArticleList.as_view(), name='article_list'),
    path('scrape/', ArticleScraper.as_view(), name='article_scraper'),
    path('<pk>/', ArticleDetail.as_view(), name='article_detail'),
]
