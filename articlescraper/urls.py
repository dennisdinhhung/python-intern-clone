from django.urls import path

from articlescraper.views import Scraper, ListNewsArticle

urlpatterns = [
    path('scrape/', Scraper.as_view(), name='scraper'),
    path('article/', ListNewsArticle.as_view(), name='get_data'),
    path('article/<int:pk>/', ListNewsArticle.as_view(), name='CRUD')
]