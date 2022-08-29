from django.urls import path

from articles.views import GetDetail, Scraper, ListNewsArticle

urlpatterns = [
    path('scrape/', Scraper.as_view(), name='scraper'),
    path('', ListNewsArticle.as_view(), name='get_data'),
    path('<pk>/', ListNewsArticle.as_view(), name='CRUD'),
    path('details/<pk>/', GetDetail.as_view(), name='get_detail')
]