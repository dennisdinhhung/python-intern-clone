from django.urls import path

from articlescraper import views

urlpatterns = [
    path('scrape/', views.Scraper.as_view(), name='scraper'),
    path('article/', views.ListNewsArticle.as_view(), name='get_data'),
    path('article/<int:pk>/', views.ListNewsArticle.as_view(), name='CRUD')
]