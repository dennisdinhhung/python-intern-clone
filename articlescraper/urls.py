from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Scraper.as_view(), name='scraper'),
    path('newsarticle/', views.ListNewsArticle.as_view(), name='get_data'),
    path('newsarticle/<int:pk>', views.ListNewsArticle.as_view(), name='smth')
]