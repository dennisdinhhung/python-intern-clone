from django.urls import include, path

from articles.views import Scraper

urlpatterns = [
    path('scrape/', Scraper.as_view(), name='scraper'),
    path('article/', include('articles.urls')),
    path('auth/', include('authenticator.urls')),
]
