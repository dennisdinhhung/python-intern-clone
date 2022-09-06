from django.urls import path

from articles.views import ManageNewsArticle, GetListNewsArticle, Scraper

urlpatterns = [
    path('scrape/', Scraper.as_view(), name='scraper'),
    path('', GetListNewsArticle.as_view(), name='get_list_news'),
    path('<pk>/', ManageNewsArticle.as_view(), name='manage_news'),
]