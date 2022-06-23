from django.shortcuts import render
from django.http import HttpResponse
from newsscraper.pagination import StandardResultSetPagination
from newsscraper.serializers import NewsSeralizer
from .scraper import scrape
from .models import News
from rest_framework import viewsets, permissions

def index(request):
    list = scrape()
    
    for item in list:
        title = item["title"]
        desc = item["desc"]
        url = item['url']
        
        News.objects.create(title=title, desc=desc, url=url)
        
    return HttpResponse(list)

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSeralizer
    pagination_class = StandardResultSetPagination
    permission_classes=[permissions.AllowAny]