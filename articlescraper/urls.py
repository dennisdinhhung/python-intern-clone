from django.urls import path
from . import views

urlpatterns = [
    path('', views.Scraper.as_view(), name='scraper'),
    path('newsarticle/', views.ListNewsArticle.as_view(), name='get_data'),
    path('newsarticle/<int:pk>', views.ListNewsArticle.as_view(), name='CRUD'),
    path('newsarticle/search/', views.Search.as_view(), name='search'),
]
